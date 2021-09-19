from django.urls import path

from . import views

urlpatterns = [
    path("contacts", views.get_contacts, name="contacts_api"),
    path("contacts/stored", views.mark_added, name="mark_added_contacts"),
]
