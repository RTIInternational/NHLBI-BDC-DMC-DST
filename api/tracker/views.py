import json

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.forms.utils import ErrorList
from django.urls import reverse_lazy
from datetime import datetime, timezone
from .models import Ticket, User, STATUS_TYPES
from .jira_agent import JiraAgent
import logging

logger = logging.getLogger("django")


class IndexView(TemplateView):
    template_name = "tracker/index.html"


class DocumentationView(TemplateView):
    template_name = "tracker/user_docs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AboutView(TemplateView):
    template_name = "tracker/about.html"


class CustodianInfoView(TemplateView):
    template_name = "tracker/custodian_instructions.html"


class TicketCreate(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = [
        "email",
        "name",
        "organization",
        "study_name",
        "dataset_description",
        "is_test_data",
        "google_email",
        "aws_iam",
        "data_size",
        "study_id",
        "consent_code",
    ]

    # send email if form is valid
    def form_valid(self, form):
        ticket_obj = form.save(commit=False)
        ticket_obj.created_by = self.request.user
        ticket_obj.save()
        # NOTE: Development: Mail
        # Commented out until we get mail/SendGrid working
        # Mail(ticket_obj, "Created").send()
        return super().form_valid(form)


class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = [
        "name",
        "email",
        "organization",
        "study_name",
        "dataset_description",
        "is_test_data",
        "google_email",
        "aws_iam",
        "data_size",
        "study_id",
        "consent_code",
        "ticket_review_comment",
    ]

    # add status to context
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["status"] = self.object.get_ticket_status
        context["staff"] = self.request.user.is_staff

        return context

    # handle ticket status logic
    def form_valid(self, form):
        status_update = self.request.POST.get("status_update")
        ticket = form.save(commit=False)

        # extract user data
        user = self.request.user
        email = user.email
        staff = user.is_staff

        if staff:
            if status_update == "Approve Ticket":
                # set status to "Awaiting NHLBI Cloud Bucket Creation"
                ticket.ticket_approved_dt = datetime.now(timezone.utc)
                ticket.ticket_approved_by = email
            elif status_update == "Reject Ticket":
                # add rejected timestamp
                ticket.ticket_rejected_dt = datetime.now(timezone.utc)
                ticket.ticket_rejected_by = email
            elif status_update == "Mark as Bucket Created":
                # set status to "Awaiting Data Custodian Upload Start"
                ticket.bucket_created_dt = datetime.now(timezone.utc)
                ticket.bucket_created_by = email
            elif status_update == "Mark as Data Upload Started":
                # set status to "Awaiting Data Custodian Upload Complete"
                ticket.data_uploaded_started_dt = datetime.now(timezone.utc)
                ticket.data_uploaded_started_by = email
            elif status_update == "Mark as Data Upload Completed":
                # set status to "Awaiting Gen3 Acceptance"
                ticket.data_uploaded_completed_dt = datetime.now(timezone.utc)
                ticket.data_uploaded_completed_by = email
            elif status_update == "Mark as Gen3 Approved":
                # set status to "Gen3 Accepted"
                ticket.data_accepted_dt = datetime.now(timezone.utc)
                ticket.data_accepted_by = email
            elif status_update == "Revive Ticket":
                # remove rejected timestamp
                ticket.ticket_rejected_dt = None
                ticket.ticket_rejected_by = email
            elif status_update == None:
                # if staff edits ticket
                logger.info("Ticket Updated by " + email)
            else:
                form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
                    ["Only Staff are allowed to perform this action"]
                )
        else:
            if status_update == "Mark as Data Upload Started":
                # set status to "Awaiting Data Custodian Upload Complete"
                ticket.data_uploaded_started_dt = datetime.now(timezone.utc)
                ticket.data_uploaded_started_by = email
            elif status_update == "Mark as Data Upload Completed":
                # set status to "Awaiting Gen3 Acceptance"
                ticket.data_uploaded_completed_dt = datetime.now(timezone.utc)
                ticket.data_uploaded_completed_by = email
            elif (
                    status_update == None and ticket.get_ticket_status[1] == STATUS_TYPES[1]
            ):
                # if user edits ticket
                logger.info("Ticket Updated by " + email)
            else:
                form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
                    ["Only Data Custodians are allowed to perform this action"]
                )

        ticket.save()
        self.object = ticket

        # send email with status update
        # NOTE: Development: Mail
        # Commented out until we get mail/SendGrid working
        # Mail(ticket, ticket.get_ticket_status[1]).send()
        return super().form_valid(form)


class TicketDelete(PermissionRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy("tracker:tickets-list")

    def has_permission(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        ticket = self.get_object()

        # send email notification
        # NOTE: Development: Mail
        # Commented out until we get mail/SendGrid working
        # Mail(ticket, "Deleted").send()
        return super().form_valid(form)


class TicketsList(LoginRequiredMixin, ListView):
    model = Ticket
    context_object_name = "tickets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jira_agent = JiraAgent()
        jira_board_config = jira_agent.get_board_config()
        jira_issues = jira_agent.get_board_issues()

        statuses = {}
        for idx, column in enumerate(jira_board_config["columnConfig"]["columns"]):
            if column["name"] == "Backlog":
                continue
            statuses[idx] = {}
            statuses[idx]["name"] = column["name"]
            statuses[idx]["ids"] = [status['id'] for status in column["statuses"]]
            statuses[idx]["issues"] = []
            for issue in jira_issues['issues']:
                if issue['fields']['status']['id'] in statuses[idx]["ids"]:
                    statuses[idx]["issues"].append(issue)
            statuses[idx]["issues_count"] = len(statuses[idx]["issues"])

        context["statuses"] = statuses

        return context


class RejectedTicketsList(PermissionRequiredMixin, ListView):
    permission_required = "is_staff"
    template_name = "tracker/ticket_rejected_list.html"
    model = Ticket

    context_object_name = "tickets"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        queryset = self.object_list

        # generate a list of status types
        context["rejected"] = []

        # iterate through all tickets and sort rejected tickets
        for object in queryset:
            # Data Intake Form Rejected
            status = object.get_ticket_status[1]
            if status == STATUS_TYPES[0]:
                object.last_updated = (
                        datetime.now(timezone.utc) - object.get_ticket_status[0]
                ).days
                object.status_color = object.get_ticket_status[2]

                # filter tickets by status
                context["rejected"].append(object)

        return context


class UserProfile(TemplateView):
    template_name = "tracker/profile.html"
    model = User
