from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'webmain'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contact'),

    path('about/', views.AboutView.as_view(), name='about'),

    path("tariffs/", views.TariffsView.as_view(), name="tariffs"),
    path("faqs/", views.FaqsView.as_view(), name="faqs"),
    path("blogs/", views.BlogView.as_view(), name="blogs"),
    path("blog/<slug:slug>/", views.BlogDetailView.as_view(), name="blog"),
    path("page/<slug:slug>/", views.PageDetailView.as_view(), name="page"),
    path("gallery/", views.GalleryView.as_view(), name="galleries"),
]