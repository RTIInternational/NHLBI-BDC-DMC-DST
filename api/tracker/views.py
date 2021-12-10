from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from datetime import datetime, timezone
from .models import Ticket, STATUS_TYPES


class IndexView(TemplateView):
    template_name = "tracker/index.html"


class UserDocsView(TemplateView):
    template_name = "tracker/user_docs.html"


class CustodianInfoView(TemplateView):
    template_name = "tracker/custodian_instructions.html"


class TicketCreate(CreateView):
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

    def form_valid(self, form):
        ticket_obj = form.save(commit=True)
        # FIXME - add checks here
        return super().form_valid(form)


# FIXME - see https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-editing/ for adding auth
class TicketUpdate(UpdateView):
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


class TicketDelete(DeleteView):
    model = Ticket
    success_url = reverse_lazy("tracker:tickets-list")


class TicketsList(ListView):
    model = Ticket
    context_object_name = "tickets"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        queryset = self.object_list

        # generate a list of status types
        context["awaiting_review"] = []
        context["awaiting_bucket_creation"] = []
        context["awaiting_data_upload"] = []
        context["data_upload_in_progress"] = []
        context["awaiting_gen3_approval"] = []
        context["gen3_accepted"] = []
        context["rejected"] = []

        # iterate through all tickets and sort accordingly
        for object in queryset:
            # calculate last updated and set colors
            object.last_updated = (
                datetime.now(timezone.utc) - object.get_ticket_status[0]
            ).days
            object.status_color = object.get_ticket_status[2]
            if object.last_updated > 14:
                object.last_updated_color = "text-red"
            elif object.last_updated > 7:
                object.last_updated_color = "text-yellow"

            # filter tickets by status
            status = object.get_ticket_status[1]
            if status == STATUS_TYPES[1]:
                # Awaiting Review
                context["awaiting_review"].append(object)
            elif status == STATUS_TYPES[2]:
                # Awaiting Bucket Creation
                context["awaiting_bucket_creation"].append(object)
            elif status == STATUS_TYPES[3]:
                # Awaiting Data Upload
                context["awaiting_data_upload"].append(object)
            elif status == STATUS_TYPES[4]:
                # Data Upload in Progress
                context["data_upload_in_progress"].append(object)
            elif status == STATUS_TYPES[5]:
                # Awaiting Gen3 Approval
                context["awaiting_gen3_approval"].append(object)
            elif status == STATUS_TYPES[6]:
                # Gen3 Accepted
                context["gen3_accepted"].append(object)
            else:
                # Data Intake Form Rejected
                context["rejected"].append(object)

        return context


class RejectedTicketsList(ListView):
    model = Ticket
    template_name = "tracker/ticket_rejected_list.html"
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


class TicketDetail(DetailView):
    model = Ticket
    context_object_name = "ticket"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        return context