from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import F
from django.shortcuts import redirect, render

from portal.models import Submission
from review.models import Review
from users.models import Profile

# Create your views here.


@login_required(login_url="user_login")
def review(request):
    user = request.user
    if Profile.objects.filter(user=user, is_council=True).exists():
        submission = request.POST.get("task")
        feedback = request.POST.get("feedback")
        rating = request.POST.get("rating")
        review = Review(
            user=Profile.objects.get(user=user),
            submission_id=submission,
            feedback=feedback,
            rating=rating,
        )
        review.save()
        return redirect("/portal/home?success=True")

    return redirect("/portal/home")
