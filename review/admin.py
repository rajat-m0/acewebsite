from django.contrib import admin

from ace.linkify import linkify
from users.models import Profile

from .models import Review, SelectionResult

# Register your models here.

admin.site.register(SelectionResult)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("admin/css/vendor/select2/select2.css",),
        }
        js = ("admin/js/vendor/select2/select2.full.js",)

    # form = PhotoUnsignedDirectForm
    list_display = (
        "id",
        linkify("user"),
        linkify("submission"),
        "feedback",
        "rating",
        "is_selected",
    )
    search_fields = [
        "submission__user__user__first_name",
        "submission__user__user__last_name",
        "submission__user__email_id",
        "submission__task__task_name",
        "feedback",
    ]
    list_filter = ("submission__task__category",)
    # autocomplete_fields = ('submission', )

    fieldsets = (
        (
            None,
            {
                "description": """
<script>
django.jQuery(function () {
    let m;
    if(m = location.search.match(/^\?submission_id=(\d+)/i)) {
        django.jQuery("#id_submission").val(m[1]);
    }
    django.jQuery("#id_submission").select2();
});
</script>
            """,
                "fields": ("user", "submission", "feedback", "rating", "is_selected"),
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # print(kwargs)
            kwargs["queryset"] = Profile.objects.filter(user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            # print(Profile, obj)
            return (
                request.user.username == "chirgjin"
                or Profile.objects.filter(user=request.user, pk=obj.user.id).exists()
            )

        return super().has_change_permission(request=request, obj=obj)
