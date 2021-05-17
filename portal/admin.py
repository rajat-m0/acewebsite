from django.contrib import admin
from .models import Category, Task, Submission
from review.models import Review
from ace.linkify import linkify
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
#from django_imgur.storage import ImgurStorage

admin.site.site_title = 'ACE - Selection Portal'
admin.site.site_header = 'ACE - Selection Portal'

class ReviewedListFilter(admin.SimpleListFilter):
    title = _('Is Reviewed')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_reviewed'

    def lookups(self, request, model_admin):
        return (
            ('y', _('Yes')),
            ('n', _('No')),
        )

    def queryset(self, request, queryset):
        # print("QS called", self.value())
        if self.value() == 'y':
            # reviewed_objects = list(Review.objects.all().values("id"))
            qs = queryset.exclude(review=None)
            # print(qs.query.__str__());
            return qs
        if self.value() == 'n':
            return queryset.filter(review=None)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'category','id', 'difficulty_value')
    list_filter = ('category', 'difficulty_value',  )
    search_fields = ('task_name', 'category__name', )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', linkify('user'), linkify('task'), 'submission_link', 'date_updated', 'review_link')
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__email_id', 'task__task_name', ]
    list_filter = ('task__category', 'task_submitted', ReviewedListFilter )
    readonly_fields = ('review_link', )

    def review_link(self, instance):
        # print(self.review)
        url = reverse('admin:review_review_add') + "?submission_id={}".format(instance.id)
        try:
            if self._user:
                self.review = None
                try:
                    self.review = Review.objects.get(user__user=self._user, submission=instance)
                except ObjectDoesNotExist:
                    if Review.objects.filter(submission=instance).exists():
                        return format_html("<a href='{}' >Already Reviewed</a>".format(url))

            if self.review:
                model_name = self.review._meta.model_name
                app_label = self.review._meta.app_label
                url = reverse(f"admin:{app_label}_{model_name}_change", args=[self.review.id])
                return format_html("<a href='{}' >Already Reviewed by you</a>".format(url))
        except Exception as e:
            print(str(e))
        
        return format_html("<a href='{}' >Review This</a>".format(url))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self._user = None
        try:
            review = Review.objects.get(submission_id=object_id, user__user=request.user)
            self.review = review
        except ObjectDoesNotExist:
            self.review = None
        
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def changelist_view(self, request, extra_context=None):
        self._user = request.user

        return super().changelist_view(request, extra_context)

    def submission_link(self, obj):
        if not obj.submission_url:
            return ''
        
        return format_html('<a href="{}">{}</a>', obj.submission_url, obj.submission_url)
admin.site.register(Category)

