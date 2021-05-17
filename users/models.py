from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Profile(models.Model):
    COURSE_BCA = 1
    COURSE_MCA = 2
    COURSE_OTHER = 3
    COURSES = (
        (COURSE_BCA, 'BCA'),
        (COURSE_MCA, 'MCA'),
        (COURSE_OTHER, 'Other'),
    )

    SECTIONS = (
        (1, "1A"),
        (2, "1B"),
        (3, "1C"),
        (4, "1D"),
        (5, "1EA"),
        (6, "1EB"),
        (7, "3A"),
        (8, "3B"),
        (9, "3C"),
        (10, "3D"),
        (11, "3EA"),
        (12, "3EB"),
        (13, "5A"),
        (14, "5B"),
        (15, "5C"),
        (16, "5D"),
        (17, "5EA"),
        (18, "5EB"),
        (19, "Other"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=11, blank=True, null=True)
    course = models.IntegerField(default=None, null=True, blank=True, choices=COURSES)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=20)  # validators should be a list
    section = models.IntegerField(default=None, blank=True, null=True, choices=SECTIONS)

    is_member = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)
    is_council = models.BooleanField(default=False)

    position = models.TextField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    
    dob = models.DateField(null=True, blank=True)
    
    submission_folder = models.CharField(null=True, blank=True, max_length=100)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    github = models.CharField('github username', null=True, blank=True, max_length=50)
    website = models.URLField(null=True, blank=True)
    behance = models.URLField(null=True, blank=True)
    linkedin = models.CharField('linkedin id', null=True, blank=True, max_length=150)
    facebook = models.CharField('facebook username', null=True, blank=True, max_length=50)
    insta = models.CharField('insta handle', null=True, blank=True, max_length=50)

    picture = CloudinaryField('image', null=True, blank=True)

    def get_membership(self):
        if self.is_council:
            return 'Council Member'
        elif self.is_core:
            return 'Core Member'
        elif self.is_member:
            return 'Member'
        else:
            return ''

    def name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)
        
    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)



class Alumni(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True, null=True)
    acd_year = models.CharField(max_length=50)

    def __str__(self):
        return str(self.profile)


class Mentor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True, null=True)
    designation  = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.profile)