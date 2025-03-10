from django.contrib import admin
from .models import *
# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', )
    search_fields = ('name', 'phone',)

admin.site.register(ContactUs, ContactUsAdmin)
