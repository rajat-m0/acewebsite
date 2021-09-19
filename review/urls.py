from django.conf.urls import url

from review import views

urlpatterns = [
    url(r"submission$", views.review, name="review"),
]
