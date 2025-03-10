from django import template
from webmain.models import Blog, Pages, SettingGlobal, HomePage, Contact, About



register = template.Library()

@register.filter(name='range')
def range_filter(number, value):
    return range(value)


@register.inclusion_tag('site/include/recentpost.html')
def get_recent_posts():
    recentposts = Blog.objects.all().order_by('-created_at')[:5]
    return {'recentpost': recentposts}

@register.simple_tag()
def get_pages_footer():
    try:
        return Pages.objects.filter(viewtype=1)[:4]
    except:
        return None

@register.simple_tag
def get_settings_first():
    return SettingGlobal.objects.first()

@register.simple_tag()
def get_homepage_item():
    return HomePage.objects.all()

@register.simple_tag()
def get_contacts_item():
    return Contact.objects.first()

