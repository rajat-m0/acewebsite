from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout, name="logout"),
    path("members/", views.member, name="members"),
    path("events/", views.event, name="events"),
    path("projects/", views.project, name="projects"),
    path("achievements/", views.achievement, name="achievements"),
    path("archive/", views.archive, name="archive"),
    path("calendar/", views.agenda, name="calendar"),
    path("mentors/", views.mentor, name="mentors"),
    path("alumnus/", views.alumni, name="alumnus"),
    path("code-of-conduct/", views.codeofconduct, name="code_of_conduct"),
    path("selection-procedure/", views.selection, name="selection_procedure"),
    path("magazine", views.magazine2020, name="magazine"),
    path("magazine2020", views.magazine2020, name="magazine2020"),
    path("magazine2019", views.magazine2019, name="magazine2019"),
    path("magazine2018", views.magazine2018, name="magazine2018"),
    path("magazine2017", views.magazine2017, name="magazine2017"),
]
