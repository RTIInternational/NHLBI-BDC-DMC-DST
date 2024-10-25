from django.urls import path
from . import views

app_name = "tracker"
urlpatterns = [
    path("", views.TicketsList.as_view(), name="tickets-list"),
    path("profile/", views.UserProfile.as_view(), name="profile"),
    path("<str:pk>/detail/", views.TicketDetail.as_view(), name="ticket-detail"),
    path("create_submission/", views.CreateSubmission.as_view(), name="create-submission"),
    path("new_ticket_freshdesk/", views.CreateFreshdeskTicket.as_view(), name="new-ticket-freshdesk"),
    path("user_docs/", views.DocumentationView.as_view(), name="documentation"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("health/", views.health_check, name="health-check"),
]
