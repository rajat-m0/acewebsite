from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    picture = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.name)


class Achievement(models.Model):
    id = models.BigAutoField(primary_key=True)

    team = models.CharField(max_length=150)
    event_name = models.CharField(max_length=500, blank=True)
    position = models.CharField(max_length=5)
    college_name = models.CharField(max_length=10)
    fest_name = models.CharField(max_length=100, blank=True)
    event_month = models.DateField(max_length=20, null=True, blank=True)

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.team)



class Event(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    event_type = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    images = models.ManyToManyField(Image)
    registration_url = models.URLField(null=True, blank=True)

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)


class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    image = models.ManyToManyField(Image)

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.name)