from django.urls import path, include
from django.contrib import admin


urlpatterns_webmain = [
    path('', include('webmain.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("_nested_admin/", include("nested_admin.urls")),
    path('developer_management/', admin.site.urls),

    # Добавьте другие URL, если нужно
]
urlpatterns_useraccount = [
    path('', include('useraccount.urls')),
    # Добавьте другие URL, если нужно
]
urlpatterns_moderation = [
    path('', include('moderation.urls')),
    # Добавьте другие URL, если нужно
]
