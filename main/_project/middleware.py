# from django.contrib.sites.models import Site
# from django.urls import resolve
# from django.http import HttpResponse
# from django.conf import settings
#
# class DomainRoutingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         host = request.get_host()
#
#         # Сохраняем стандартный urlconf Django
#         default_urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
#
#         try:
#             # Получаем текущий сайт на основе домена запроса
#             current_site = Site.objects.get(domain=host)
#             site_id = current_site.id
#
#             print(f"Current domain: {host}")
#             print(f"Current site ID: {site_id}")
#
#             # Загружаем основные URL из project.urls
#             resolver_match = resolve(request.path_info, urlconf=default_urlconf)
#             if resolver_match:
#                 response = resolver_match.func(request, *resolver_match.args, **resolver_match.kwargs)
#                 return self.render_response(response)
#
#             # Подключаем дополнительные URL в зависимости от site_id
#             if site_id == 1:
#                 print("Routing through webmain.urls")
#                 resolver_match = resolve(request.path_info, urlconf='project.dynamic_urls.urlpatterns_webmain')
#             elif site_id == 2:
#                 print("Routing through useraccount.urls")
#                 resolver_match = resolve(request.path_info, urlconf='project.dynamic_urls.urlpatterns_useraccount')
#             elif site_id == 3:
#                 print("Routing through moderation.urls")
#                 resolver_match = resolve(request.path_info, urlconf='project.dynamic_urls.urlpatterns_moderation')
#             if resolver_match:
#                 response = resolver_match.func(request, *resolver_match.args, **resolver_match.kwargs)
#                 return self.render_response(response)
#
#         except Site.DoesNotExist:
#             pass  # Обработка случая, когда сайт не найден по указанному домену
#
#         # Передаем запрос дальше по стандартному механизму URLConf Django
#         return self.get_response(request)
#
#     def render_response(self, response):
#         if isinstance(response, HttpResponse):
#             # Убедимся, что ответ полностью рендерен
#             response.render()
#         return response
