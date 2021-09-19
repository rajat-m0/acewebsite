from django.urls import path

from portal import views

urlpatterns = [
    # path('', views.login, name='login'),
    path("home/", views.home, name="portal_home"),
    path("submission/", views.submit_task, name="submit_task"),
    path("", views.landing, name="portal_landing"),
    # path('tasks/', views.tasks, name='tasks_page'),
    path("categories/<int:id>/tasks", views.serve_tasks, name="tasks_list"),
    path("results/", views.selection_results, name="selection_results"),
    path("refresh-gdrive-token", views.refresh_token_view, name="refresh_token_view")
    # path('form/', views.ace_profile_form, name='ace_profile_form'),
    # path('success/', views.create_ace_profile, name='create_ace_profile'),
    # path('logout/', views.logout, name='logout'),
]
