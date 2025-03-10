from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, get_user_model
from django.db.models import Max, Subquery, OuterRef
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden, JsonResponse, Http404
from django.db import transaction
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.contrib import messages
from django.contrib.sites.models import Site
from moderation.models import Ticket, TicketComment, TicketCommentMedia
from moderation.forms import TicketCommentForm
from useraccount.models import Notification, Profile, Chat, ChatMessage, ChatMessageMedia
from useraccount.forms import SignUpForm, UserProfileForm, PasswordResetEmailForm, SetPasswordFormCustom, ChatForm, ChatMessageForm
from webmain.models import Seo



def custom_logout(request):
    logout(request)
    return redirect('useraccount:edit_profile')


"""Регистрация/Авторизация"""
class CustomLoginView( auth_views.LoginView):
    template_name = 'lk/login.html'

    def get_success_url(self):
        success_url = reverse('useraccount:edit_profile')
        return f"{success_url}#edit"

    def dispatch(self, request, *args, **kwargs):
        try:
            current_site = Site.objects.get(domain=request.get_host())
            self.site_id = current_site.id
        except Site.DoesNotExist:
            raise Http404("Страница не найдена")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Получаем пользователя, который пытается войти
        user = form.get_user()

        # Проверяем, что у пользователя есть профиль и сайт профиля совпадает с сайтом компании
        if user.site_id:
            try:
                company = Companys.objects.get(owner=user)
                if self.site_id == company.site_id:
                    return super().form_valid(form)
                else:
                    messages.error(self.request, 'Вы не принадлежите к этой компании.')
                    return self.render_to_response(self.get_context_data(form=form))
            except Companys.DoesNotExist:
                messages.error(self.request, 'У вас нет компании.')
                return self.render_to_response(self.get_context_data(form=form))

        # Если у пользователя нет профиля или его сайт не соответствует компании, выдаем ошибку
        messages.error(self.request, 'Вы не принадлежите к этой компании.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            seo_data = Seo.objects.get(pagetype=9)
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

class SignUpView( CreateView):
    form_class = SignUpForm
    template_name = 'lk/register.html'
    success_url = reverse_lazy('useraccount:user_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'companyowner'):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden('Только владельцы компаний могут регистрировать новых пользователей.')
        else:
            return redirect('useraccount:login')  # Перенаправление на страницу входа, если пользователь не авторизован

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Создаем пользователя, но не сохраняем его полностью пока
        user = form.save(commit=False)

        # Получаем компанию текущего пользователя
        company = self.request.user.companyowner

        # Устанавливаем компанию и сайт новому пользователю
        user.company = company
        user.site = company.site  # Предполагаем, что компания имеет связь с сайтом

        # Сохраняем пользователя
        user.save()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seo_data = Seo.objects.get(pagetype=8)
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

class CustomPasswordResetView(PasswordResetView):
    template_name = 'lk/restore_access.html'
    email_template_name = 'email/password_reset_email.html'
    subject_template_name = 'email/password_reset_subject.txt'
    form_class = PasswordResetEmailForm
    success_url = reverse_lazy('useraccount:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'lk/email/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'lk/restore_access_user.html'
    form_class = SetPasswordFormCustom
    success_url = reverse_lazy('useraccount:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'email/password_reset_complete.html'

"""Личный кабинет"""
class EditMyProfileView(TemplateView):
    template_name = 'lk/profile_edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, Profile):
            initial_data = {'birthday': user.birthday.strftime('%Y-%m-%d') if user.birthday else None}
        else:
            initial_data = {}

        form = UserProfileForm(instance=user, initial=initial_data)
        context = self.get_context_data(form=form, title='Личные данные')
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('useraccount:edit_profile')
        else:
            print("Form errors:", form.errors)

        context = self.get_context_data(form=form, title='Личные данные')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seo_data = Seo.objects.get(pagetype=6)
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
class NotificationView(ListView):
    model = Notification
    template_name = 'lk/notification_list.html'
    context_object_name = 'notificationes'
    paginate_by = 10

    def get_queryset(self):
        # Добавляем отладочный вывод
        queryset = Notification.objects.filter(user=self.request.user)
        print(f"Notifications for user {self.request.user}: {queryset}")  # Выводим queryset для отладки
        return queryset

    def get(self, request, *args, **kwargs):
        # Обновляем статус уведомлений перед отображением страницы
        with transaction.atomic():
            updated_rows = Notification.objects.filter(
                user=self.request.user,
                status=1  # Статус "Не прочитан"
            ).update(status=2)  # Меняем на "Прочитан"
        print(f"Updated {updated_rows} notifications to read status.")  # Выводим количество обновленных строк для отладки
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seo_data = Seo.objects.get(pagetype=13)
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

        print(f"Context data: {context}")  # Выводим контекст для отладки

        return context

class EditProfileView(TemplateView):
    template_name = 'lk/profile_edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('pk')  # Получаем ID профиля из URL
        profile = get_object_or_404(Profile, id=profile_id)

        # Проверяем доступ текущего пользователя к редактированию профиля
        if request.user.is_superuser or request.user == profile.user:
            initial_data = {'birthday': profile.birthday.strftime('%Y-%m-%d') if profile.birthday else None}
            form = UserProfileForm(instance=profile, initial=initial_data)
            context = self.get_context_data(form=form, title='Личные данные', profile=profile)
            return self.render_to_response(context)
        else:
            # Возвращаем ошибку доступа или другую страницу
            return HttpResponseForbidden("У вас нет прав для редактирования этого профиля.")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        profile_id = kwargs.get('pk')  # Получаем ID профиля из URL
        profile = get_object_or_404(Profile, id=profile_id)

        # Проверяем доступ текущего пользователя к редактированию профиля
        if not (request.user.is_superuser or request.user == profile.user):
            return HttpResponseForbidden("У вас нет прав для редактирования этого профиля.")

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('useraccount:edit_profiles', pk=profile_id)
        else:
            print("Form errors:", form.errors)

        context = self.get_context_data(form=form, title='Личные данные', profile=profile)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = kwargs.get('profile')
        if profile:
            try:
                seo_data = Seo.objects.get(pagetype=6)
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


"""Тикеты"""
class TicketsView(ListView):
    model = Ticket
    template_name = 'lk/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 10
    def get_queryset(self):
        # Фильтрация тикетов текущего пользователя
        return Ticket.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Вызов `super()` сохраняет функциональность `ListView`
        try:
            seo_data = Seo.objects.get(pagetype=6)
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

class TicketMessageView(DetailView):
    model = Ticket
    template_name = 'lk/tickets_messages.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        return Ticket.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object

        # Get all comments related to the ticket
        comments = TicketComment.objects.filter(ticket=ticket).prefetch_related('media').all()

        # Setup pagination
        paginator = Paginator(comments, 10)  # Show 10 comments per page
        page = self.request.GET.get('page')

        try:
            comments_paginated = paginator.page(page)
        except PageNotAnInteger:
            comments_paginated = paginator.page(1)
        except EmptyPage:
            comments_paginated = paginator.page(paginator.num_pages)

        context['ticket_comments'] = comments_paginated
        context['form'] = TicketCommentForm()
        context['ticket'] = ticket
        context['paginator'] = paginator
        context['page_obj'] = comments_paginated

        try:
            seo_data = Seo.objects.get(pagetype=6)
            context.update({
                'seo_previev': seo_data.previev,
                'seo_title': seo_data.title,
                'seo_description': seo_data.description,
                'seo_propertytitle': seo_data.propertytitle,
                'seo_propertydescription': seo_data.propertydescription,
            })
        except Seo.DoesNotExist:
            context.update({
                'seo_previev': None,
                'seo_title': None,
                'seo_description': None,
                'seo_propertytitle': None,
                'seo_propertydescription': None,
            })

        return context

class TicketDeleteView(View):
    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        ticket.delete()
        return redirect('useraccount:tickets')

class TicketCommentCreateView(CreateView):
    model = TicketComment
    form_class = TicketCommentForm

    @transaction.atomic
    def form_valid(self, form):
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, id=ticket_id)
        comment = form.save(commit=False)
        comment.ticket = ticket
        comment.author = self.request.user
        comment.save()

        files = self.request.FILES.getlist('files')
        for file in files:
            TicketCommentMedia.objects.create(comment=comment, file=file)

        return JsonResponse({
            'status': 'success',
            'comment': {
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                'files': [{'name': media.file.name, 'url': media.file.url} for media in comment.media.all()]
            }
        })

    def form_invalid(self, form):
        print(form.errors)  # Для отладки
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

"""Чаты"""
class ChatsListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'lk/chat/chat.html'
    context_object_name = 'chats'
    paginate_by = 20

    def get_queryset(self):
        return Chat.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Аннотируем каждый объект Chat временем и содержимым последнего сообщения
        group_chats = Chat.objects.filter(type=1).annotate(
            last_message_time=Max('chatmessage__date'),
            last_message_content=Subquery(
                ChatMessage.objects.filter(chat_id=OuterRef('pk')).order_by('-date').values('content')[:1]
            )
        )

        personal_chats = Chat.objects.filter(type=2).annotate(
            last_message_time=Max('chatmessage__date'),
            last_message_content=Subquery(
                ChatMessage.objects.filter(chat_id=OuterRef('pk')).order_by('-date').values('content')[:1]
            )
        )

        # Проверяем для каждого чата, есть ли непрочитанные сообщения
        group_chats_with_unread = []
        for chat in group_chats:
            last_message = ChatMessage.objects.filter(chat=chat).order_by('-date').first()
            chat.has_unread_messages = False
            if last_message and not last_message.views.filter(id=user.id).exists():
                chat.has_unread_messages = True
            group_chats_with_unread.append(chat)

        personal_chats_with_unread = []
        for chat in personal_chats:
            last_message = ChatMessage.objects.filter(chat=chat).order_by('-date').first()
            chat.has_unread_messages = False
            if last_message and not last_message.views.filter(id=user.id).exists():
                chat.has_unread_messages = True
            personal_chats_with_unread.append(chat)

        context['group_chats'] = group_chats_with_unread
        context['personal_chats'] = personal_chats_with_unread

        return context

class ChatsDetailView(DetailView):
    model = Chat
    template_name = 'lk/chat/message.html'
    context_object_name = 'chat'

    def get_queryset(self):
        return Chat.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.object  # Получаем текущий чат из контекста
        user = self.request.user

        # Помечаем все сообщения чата как просмотренные текущим пользователем
        if self.request.user.is_authenticated:
            for message in chat.chatmessage.exclude(views=self.request.user):
                message.views.add(self.request.user)

        context['form'] = ChatMessageForm()
        # Аннотируем каждый объект Chat временем и содержимым последнего сообщения
        group_chats = Chat.objects.filter(type=1).annotate(
            last_message_time=Max('chatmessage__date'),
            last_message_content=Subquery(
                ChatMessage.objects.filter(chat_id=OuterRef('pk')).order_by('-date').values('content')[:1]
            )
        )

        personal_chats = Chat.objects.filter(type=2).annotate(
            last_message_time=Max('chatmessage__date'),
            last_message_content=Subquery(
                ChatMessage.objects.filter(chat_id=OuterRef('pk')).order_by('-date').values('content')[:1]
            )
        )
        # Проверяем для каждого чата, есть ли непрочитанные сообщения
        group_chats_with_unread = []
        for chat in group_chats:
            last_message = ChatMessage.objects.filter(chat=chat).order_by('-date').first()
            chat.has_unread_messages = False
            if last_message and not last_message.views.filter(id=user.id).exists():
                chat.has_unread_messages = True
            group_chats_with_unread.append(chat)

        personal_chats_with_unread = []
        for chat in personal_chats:
            last_message = ChatMessage.objects.filter(chat=chat).order_by('-date').first()
            chat.has_unread_messages = False
            if last_message and not last_message.views.filter(id=user.id).exists():
                chat.has_unread_messages = True
            personal_chats_with_unread.append(chat)

        context['group_chats'] = group_chats_with_unread
        context['personal_chats'] = personal_chats_with_unread

        # Аннотируем каждый объект Chat последним сообщением
        context['chat_messages'] = ChatMessage.objects.filter(chat=self.object).order_by('-date')

        # Получаем последнее сообщение для текущего чата
        last_message = chat.chatmessage.order_by('-date').first()
        if last_message:
            context['last_message_time'] = last_message.date

        return context

class ChatsMessageCreateView(CreateView):
    model = ChatMessage
    form_class = ChatMessageForm

    @transaction.atomic
    def form_valid(self, form):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)

        message = form.save(commit=False)
        message.chat = chat
        message.author = self.request.user
        message.save()

        # Сохранение медиафайлов
        files = self.request.FILES.getlist('files')
        for file in files:
            ChatMessageMedia.objects.create(comment=message, file=file)

        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.id,
                'author': message.author.username,
                'content': message.content,
                'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'media': [{'name': media.filename, 'url': media.file.url} for media in message.chatmessagemedia.all()]
            }
        })

    def form_invalid(self, form):
        print(form.errors)  # Для отладки
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

class ChatDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk')
        chat = get_object_or_404(Chat, id=chat_id)

        if request.user == chat.owner or request.user in chat.administrators.all():
            chat.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'У вас нет прав на удаление этого чата'}, status=403)

@method_decorator(login_required, name='dispatch')
class ChatGroupCreateView(CreateView):
    model = Chat
    form_class = ChatForm
    template_name = 'lk/chat/chat_form_add.html'
    success_url = reverse_lazy('useraccount:chats_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['users_queryset'] = Profile.objects.filter(site__domain=self.request.get_host())
        return kwargs

    def form_valid(self, form):
        chat = form.save(commit=False)
        chat.owner = self.request.user
        chat.save()
        form.save_m2m()
        return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
class ChatUpdateView(UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = 'lk/chat/chat_form_edit.html'
    success_url = reverse_lazy('useraccount:chats_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['users_queryset'] = Profile.objects.filter(site__domain=self.request.get_host())
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        context['selected_users'] = chat.users.all()
        context['not_selected_users'] = Profile.objects.filter(site__domain=self.request.get_host()).exclude(pk__in=chat.users.values_list('pk', flat=True))
        context['selected_administrators'] = chat.administrators.all()
        context['not_selected_administrators'] = Profile.objects.filter(site__domain=self.request.get_host()).exclude(pk__in=chat.administrators.values_list('pk', flat=True))
        context['update'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return response

class CreateChatView(View):
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)

        # Проверяет, есть ли уже личный чат с этим пользователем
        personal_chat = Chat.objects.filter(type=2, users=user).first()

        if personal_chat:
            # Перенаправление в существующий личный чат
            return redirect('useraccount:chats', pk=personal_chat.pk)
        else:
            # Создайте новый личный чат
            chat = Chat.objects.create(owner=request.user, type=2)
            chat.users.add(request.user, user)
            chat.save()
            # Перенаправление на созданный чат
            return redirect('useraccount:chats', pk=chat.pk)
