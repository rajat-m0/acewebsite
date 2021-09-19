from django.contrib import admin

from .models import Alumni, Mentor, Profile

# Register your models here.


@admin.register(Profile)
class ACEUserAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = (
        "user",
        "enrollment_number",
        "course",
        "email_id",
        "is_core",
        "is_member",
        "date_updated",
    )
    search_fields = [
        "user__username",
        "enrollment_number",
        "course",
        "email_id",
        "user__first_name",
        "user__last_name",
    ]
    list_filter = (
        "is_core",
        "is_member",
        "is_council",
    )


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = (
        "profile",
        "designation",
    )
    search_fields = [
        "profile__user__first_name",
        "designation",
        "profile__course",
        "profile__email_id",
    ]


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = (
        "profile",
        "acd_year",
    )
    search_fields = [
        "profile__user__first_name",
        "acd_year",
        "profile__course",
        "profile__email_id",
    ]
