from django.db import models
from users.models import User
from cloudinary.models import CloudinaryField
# Create your models here.

class Project(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Project Name", max_length=250)
    tools = models.CharField("Tools Used", max_length=500)
    description = models.TextField("Project Description")
    contributors = models.ManyToManyField(User, related_name='contributors')
    picture = CloudinaryField('image', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    