from django.contrib import admin
from service.models import Service, Tariff, TariffParameter


# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(TariffParameter)
class TariffParameterAdmin(admin.ModelAdmin):
    list_display = ('name', )