from django.db import models
from users.models import Profile
# Create your models here.


class ProfileStatus(models.Model):
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    contact_added = models.BooleanField(default=False)
    whatsapp_added = models.BooleanField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)