from django.contrib import admin


from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import *
from django import forms


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('first_banner_title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', )

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address','email',)

@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('item_type', )

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_description = ('description',)



@admin.register(SettingGlobal)
class SettingGlobalAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('link', )