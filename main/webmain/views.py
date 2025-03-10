from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView, CreateView, TemplateView, FormView
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.db.models import Q
from django.http import Http404
from django.contrib.sites.models import Site
from webmain.models import HomePage, Faq, Review, GalleryItem, Gallery, SMTPPage, SettingGlobal, Seo, Pages,SocialLink,Contact,Blog,BlogCategory,About
from .forms import ContactUsForm
from service.models import Service ,ServiceCategory, Tariff, TariffParameter


class FirstSiteMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            current_site = Site.objects.get(domain=request.get_host())
            site_id = current_site.id
        except Site.DoesNotExist:
            raise Http404("Страница не найдена")

        # Проверяем, что site_id равен 1
        if site_id != 1:
            raise Http404("Страница не найдена")

        return super().dispatch(request, *args, **kwargs)


class HomeView(ListView):
    model = HomePage
    template_name = 'site/home.html'
    context_object_name = 'homepage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homepage = HomePage.objects.first()
        if homepage:
            context['tariffs'] = homepage.tariff.all()
            context['reviews'] = homepage.reviews.all()
            context['blogs'] = homepage.blogs.all()
            context['faqs'] = homepage.faqs.all()
            context['form'] = ContactUsForm()
            context['galleries'] = homepage.gallery.all()
            context['services'] = homepage.choose_us_services.all()
            context['sociallinks'] = homepage.first_banner_sociallinks.all()

        try:
            seo_data = Seo.objects.get(pagetype=1)
            context['seo_previev'] = seo_data.previev
            context['seo_title'] = seo_data.title
            context['seo_description'] = seo_data.description
            context['seo_propertytitle'] = seo_data.propertytitle
            context['seo_propertydescription'] = seo_data.propertydescription
        except Seo.DoesNotExist:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None

        return context

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Спасибо! Ваше сообщение отправлено.'})
            return redirect(reverse_lazy('webmain:home') + '?submitted=True')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ContactView(FormView):
    model = Contact
    template_name = 'site/contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('webmain:contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contact.objects.all()
        context['contacts'] = contacts
        context['departaments'] = [contact.departaments.split(',') for contact in contacts]

        try:
            seo_data = Seo.objects.get(pagetype=13)  # Фильтруем по домену
            context['seo_previev'] = seo_data.previev
            context['seo_title'] = seo_data.title
            context['seo_description'] = seo_data.description
            context['seo_propertytitle'] = seo_data.propertytitle
            context['seo_propertydescription'] = seo_data.propertydescription
        except Seo.DoesNotExist:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user if self.request.user.is_authenticated else None
        form.save()
        return super().form_valid(form)

class AboutView(TemplateView):
    template_name = 'site/about.html'
    model = About
    context_object_name = 'aboutus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aboutus = About.objects.first()
        context['homepages'] = HomePage.objects.all()
        context['services'] = Service.objects.all()
        if aboutus:
            context['pageinformation'] = aboutus.description
            context['seo_previev'] = aboutus.preview
            context['seo_title'] = aboutus.title
            context['seo_description'] = aboutus.content
            context['seo_propertytitle'] = aboutus.propertytitle
            context['seo_propertydescription'] = aboutus.propertydescription
        else:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None
        return context



class TariffsView(ListView):
    model = Tariff
    template_name = 'site/tariffs.html'  # No .html extension
    context_object_name = 'tariffs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seo_data = Seo.objects.get(pagetype=2)
            context['seo_previev'] = seo_data.previev
            context['seo_title'] = seo_data.title
            context['seo_description'] = seo_data.description
            context['seo_propertytitle'] = seo_data.propertytitle
            context['seo_propertydescription'] = seo_data.propertydescription
        except Seo.DoesNotExist:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None

        return context


class FaqsView(ListView):
    model = Faq
    template_name = 'site/faqs.html'  # No .html extension
    context_object_name = 'faqs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seo_data = Seo.objects.get(pagetype=2)
            context['seo_previev'] = seo_data.previev
            context['seo_title'] = seo_data.title
            context['seo_description'] = seo_data.description
            context['seo_propertytitle'] = seo_data.propertytitle
            context['seo_propertydescription'] = seo_data.propertydescription
        except Seo.DoesNotExist:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None

        return context
class GalleryView(ListView):
    model = Gallery
    template_name = 'site/gallery.html'  # No .html extension
    context_object_name = 'galleries'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepages'] = HomePage.objects.all()
        try:
            seo_data = Gallery.objects.first()
            context['seo_previev'] = seo_data.preview
            context['seo_title'] = seo_data.name
            context['seo_description'] = seo_data.description
            context['seo_propertytitle'] = seo_data.propertytitle
            context['seo_propertydescription'] = seo_data.propertydescription
        except Seo.DoesNotExist:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None

        return context

class BlogView(ListView):
    model = Blog
    template_name = 'site/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Вызов `super()` сохраняет функциональность `ListView`

        try:
            seo_data = Seo.objects.get(pagetype=2)  # Фильтруем по домену
            context['seo_previev'] = seo_data.previev
            context['seo_title'] = seo_data.title
            context['seo_description'] = seo_data.description
            context['seo_propertytitle'] = seo_data.propertytitle
            context['seo_propertydescription'] = seo_data.propertydescription
        except Seo.DoesNotExist:
            context['seo_previev'] = None
            context['seo_title'] = None
            context['seo_description'] = None
            context['seo_propertytitle'] = None
            context['seo_propertydescription'] = None

        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'site/blog_detail.html'
    context_object_name = 'blog'
    slug_field = "slug"

    def get_queryset(self):
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        queryset = Blog.objects.all().order_by('-created_at')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = context['blog']
        if blog:
            context['pageinformation'] = blog.description
            context['seo_previev'] = blog.preview
            context['seo_title'] = blog.title
            context['seo_description'] = blog.content
            context['seo_propertytitle'] = blog.title
            context['seo_propertydescription'] = blog.description

            # Получение предыдущего и следующего постов
            previous_blog = Blog.objects.filter(created_at__lt=blog.created_at).order_by('-created_at').first()
            next_blog = Blog.objects.filter(created_at__gt=blog.created_at).order_by('created_at').first()
            context['categories'] = BlogCategory.objects.all()
            context['previous_blog'] = previous_blog
            context['next_blog'] = next_blog
        else:
            context['pageinformation'] = None
        return context


"""Сотрудничества"""

class PageDetailView(DetailView):
    """Страницы"""
    model = Pages
    template_name = 'site/page_detail.html'
    context_object_name = 'page'
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page']
        if page:
            context['pageinformation'] = page.description
            context['seo_previev'] = page.previev
            context['seo_title'] = page.title
            context['seo_description'] = page.content
            context['seo_propertytitle'] = page.propertytitle
            context['seo_propertydescription'] = page.propertydescription
        else:
            context['pageinformation'] = None
        return context


