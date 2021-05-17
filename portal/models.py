from django.db import models
from users.models import Profile

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



class Category(models.Model):
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    image = CloudinaryField('image', null=True, blank=True)
    icon = CloudinaryField('icon', null=True, blank=True)
    theme = models.BooleanField(blank=True)
    bg_color = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Task(models.Model):
    DIFFICULTY_CHOICES = ((1, 'Easy'), (2, 'Medium'), (3, 'Hard'), (4, '-'))

    # task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=30)
    difficulty_value = models.IntegerField(choices=DIFFICULTY_CHOICES)
    task_description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.category.name, self.task_name)


class Submission(models.Model):
    class Meta:
        unique_together = (('user', 'task'),)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    task_submitted = models.BooleanField(default=False)
    submission_url = models.TextField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#{} {} : {}".format(self.id, self.user.name(), self.task.__str__())
