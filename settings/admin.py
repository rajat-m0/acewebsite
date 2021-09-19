from django.contrib import admin

from .models import Setting

# Register your models here.


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    # form = PhotoUnsignedDirectForm
    list_display = ("id", "key_name", "key_val", "created_at", "updated_at")
    search_fields = ["key_name", "key_val"]
    list_filter = ("id", "key_name", "created_at", "updated_at")
