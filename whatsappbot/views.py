from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from users.models import Profile

from .models import ProfileStatus

API_KEY = "ANH$()U%$()EJRIJEWENITOIWORJWIEOUR()$URJWEJRIERKLEWNRJBEWR$"
# Create your views here.


def get_profiles():
    return (
        Profile.objects.filter(
            Q(profilestatus__isnull=True) | Q(profilestatus__contact_added=False)
        )
        .filter(id__gte=50)
        .order_by("id")
    )


def get_contacts(request):
    key = request.GET.get("api_key", None)

    if key != API_KEY:
        return HttpResponse("404 Not Found")

    profiles = get_profiles()

    # print(profiles.query)

    contacts = []

    for profile in profiles:
        contacts.append(
            {
                "phone_number": profile.phone_number,
                "name": "SEL_{}-{}".format(profile.id, profile.name()),
                "email": profile.email_id,
                "id": profile.id,
            }
        )

    return JsonResponse({"profiles": contacts}, safe=False)


@csrf_exempt
def mark_added(request):

    key = request.GET.get("api_key", None)

    if key != API_KEY:
        return HttpResponse("404 Not Found")

    profiles = get_profiles()

    profile_ids = request.POST.getlist("profile_id[]")

    profiles = profiles.filter(id__in=profile_ids)

    profilestatuses = []

    for profile in profiles:
        profilestatuses.append(ProfileStatus(profile=profile, contact_added=True))

    ProfileStatus.objects.bulk_create(profilestatuses)

    return JsonResponse({"success": True}, safe=False)
