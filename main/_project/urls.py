from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from .dynamic_urls import urlpatterns_webmain, urlpatterns_useraccount, urlpatterns_moderation
from django.contrib.sites.models import Site


urlpatterns = [
    path('developer_management/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("_nested_admin/", include("nested_admin.urls")),
    path('', include('webmain.urls')),
    path('', include('useraccount.urls')),
    path('', include('moderation.urls')),

]

# # Добавляем URL-паттерны в зависимости от site_id
# if Site.objects.filter(id=1).exists():
#     urlpatterns += urlpatterns_webmain
#
# if Site.objects.filter(id=2).exists():
#     urlpatterns += urlpatterns_useraccount
#
# if Site.objects.filter(id=3).exists():
#     urlpatterns += urlpatterns_moderation



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

