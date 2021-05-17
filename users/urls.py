from django.urls import path, include
from django.conf.urls import url
from . import views

# app_name = 'social'

urlpatterns = [
    url(r'login/$', views.login, name='user_login'),
    url(r'signup/$', views.signup, name='user_signup'),
    url(r'logout/$', views.logout, name='user_logout'),
    # path('', include('social_django.urls', namespace='social')),

]
