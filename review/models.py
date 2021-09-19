from django.db import models

from portal.models import Submission
from users.models import Profile

# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Reviewed By"
    )
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    is_selected = models.TextField(blank=True)

    class Meta:
        unique_together = (
            "user",
            "submission",
        )


class SelectionResult(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email_id

    # preferred_timings = models.CharField(max_length=100, null=True, blank=True)
    # day_assigned = models.CharField(max_length=100, null=True, blank=True)
