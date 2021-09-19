from django.contrib import admin

from .models import Achievement, Event, Gallery, Image

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = (
        "id",
        "name",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = ("name", "description", "event_type", "start_date")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = ("team", "college_name", "event_name", "position")


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = (
        "name",
        "description",
    )
