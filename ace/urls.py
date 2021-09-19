from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path

# , handler403, handler500




def validate(request):
    return HttpResponse(
        "02A551B8E5A5A9061680F066C72F3FF2EE013A18D83597CE44BE61AB8659C553 comodoca.com 5d626d0c84f31"
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("portal/", include("portal.urls")),
    path("users/", include("users.urls")),
    path("review/", include("review.urls")),
    path("", include("website.urls")),
    path("", include("social_django.urls", namespace="social")),
    path("botapi/", include("whatsappbot.urls")),
    path(".well-known/pki-validation/491FC00A2F8B617C3566F7133D017F5D.txt", validate),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()

# handler404 = 'portal.views.error_404_view'
