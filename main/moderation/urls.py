from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'moderation'

urlpatterns = [
    #path('', views.HomeView.as_view(), name='home'),
]