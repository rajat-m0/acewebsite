from django.contrib import admin

from ace.linkify import linkify
from users.models import Profile

from .models import Project


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("admin/css/vendor/select2/select2.css",),
        }
        js = ("admin/js/vendor/select2/select2.full.js",)

    list_display = (
        "id",
        linkify("submitted_by"),
        "name",
        "tools",
    )
    search_fields = (
        "submitted_by__email",
        "submitted_by__first_name",
        "submitted_by__last_name",
        "name",
        "tools",
        "description",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "submitted_by":
            # print(kwargs)
            kwargs["queryset"] = Profile.objects.filter(is_member=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "contributors":
            # print(kwargs)
            kwargs["queryset"] = Profile.objects.filter(is_member=True)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets = (
        (
            None,
            {
                "description": """
<script>
django.jQuery(function () {
    let m;
    // if(m = location.search.match(/^\?submitted_by=(\d+)/i)) {
    //     django.jQuery("#id_submitted_by").val(m[1]);
    // }
    django.jQuery("#id_submitted_by").select2();
});
</script>
            """,
                "fields": (
                    "submitted_by",
                    "name",
                    "tools",
                    "description",
                    "contributors",
                    "picture",
                ),
            },
        ),
    )
