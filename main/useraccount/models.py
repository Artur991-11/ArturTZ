from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import (FileExtensionValidator)
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
import uuid
import os
from uuid import uuid4
from django.contrib.sites.models import Site
from service.models import Service, Tariff, Products


def get_user_dir(instance, filename) -> str:
    extension = filename.split(".")[-1]
    return f"users/user_{instance.id}.{extension}"

class Profile(AbstractUser):
    """Профиль"""
    GENDER_CHOICE = [
        (1, 'Мужской'),
        (2, 'Женский'),
    ]
    TYPE = [
        (1, 'Пользователь'),
        (2, 'Сотрудник'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(blank=True, verbose_name='Телефон', max_length=500, null=True)
    avatar = models.FileField(upload_to=get_user_dir, blank=True, verbose_name='Аватар', default='default/user-nophoto.png', validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])])
    type = models.PositiveSmallIntegerField('Тип', choices=TYPE, blank=False, default=1)
    gender = models.PositiveSmallIntegerField('Пол', choices=GENDER_CHOICE, blank=False, default=1)
    balance = models.PositiveSmallIntegerField('Баланс', blank=False, default=0)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    active_subscription = models.BooleanField(default=False, verbose_name="Активная подписка")
    subscription = models.DateField(verbose_name='Дата окончания подписки', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, verbose_name='Город', null=True)
    description = RichTextField(blank=True, null=True, verbose_name='Описание')
    online = models.BooleanField(default=False, verbose_name="Онлайн")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class History(models.Model):
    """Профиль"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create = models.DateField(verbose_name='Дата', blank=True, null=True)
    amount = models.PositiveSmallIntegerField('Сумма', blank=False, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "История пополнения"
        verbose_name_plural = "Истории пополнения"

class HistorySubscription(models.Model):
    """Профиль"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create = models.DateField(verbose_name='Дата', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Пользователь', on_delete=models.CASCADE)
    tarife = models.ForeignKey(Tariff, verbose_name='Тариф', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "История подписок"
        verbose_name_plural = "Истории подписок"

class Equipment(models.Model):
    """Профиль"""
    TYPE = [
        (1, 'Аренда'),
        (2, 'Выкуплено'),
        (3, 'Личное'),
    ]
    type = models.PositiveSmallIntegerField('Тип', choices=TYPE, blank=False, default=1)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create = models.DateField(verbose_name='Дата', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Тариф', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудования"



class Notification(models.Model):
    """Уведомление"""
    TYPE = [
        (1, 'Регистрация'),
        (2, 'Покупка'),
        (3, 'Сбросить пароль'),
    ]
    type = models.PositiveSmallIntegerField('Тип', unique=True, choices=TYPE, blank=False, default=1)
    STATUS = [
        (1, 'Не прочитан'),
        (2, 'Прочитан'),
    ]
    status = models.PositiveSmallIntegerField("Статус", choices=STATUS, blank=False, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Пользователь', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField('Время отправки',auto_now_add=True)
    message = models.TextField()
    slug = models.TextField(editable=False)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"





def chat_message_media_upload_to(instance, filename):
    # Получаем ID чата из связанного объекта ChatMessage
    chat_id = instance.comment.chat.id
    # Создаем уникальное имя файла, чтобы избежать конфликтов
    unique_filename = f"{uuid4()}_{filename}"
    # Возвращаем кастомный путь
    return os.path.join('chat', str(chat_id), unique_filename)

class Chat(models.Model):
    TYPE = [
        (1, 'Групповой'),
        (2, 'Личные'),
    ]
    type = models.PositiveSmallIntegerField('Тип', choices=TYPE, blank=False, default=1)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Владелец',on_delete=models.CASCADE, related_name='chatowner')
    administrators = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name='Администраторы', related_name='chatadministrators')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Пользователи', related_name='chatusers')
    name = models.CharField(max_length=150, verbose_name='Название', blank=True, null=True)

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

class ChatMessage(models.Model):
    STATUS_CHOICES = [
        (0, 'Отправлено'),
        (1, 'Прочитано'),
    ]
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1,  editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="Чат", related_name='chatmessage')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    content = models.TextField(verbose_name="Сообщение")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True)
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Пользователи', related_name='viewsmessage')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-date']

class ChatMessageMedia(models.Model):
    comment = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='chatmessagemedia')
    file = models.FileField(upload_to='chat_message_media_upload_to/%Y/%m/%d/')
    filename = models.CharField("Имя", max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Файл сообщений чата"
        verbose_name_plural = "Файлы сообщений чата"