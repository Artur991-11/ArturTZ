from django.db import models
from django.conf import settings
import uuid
import os
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Personal(models.Model):
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь",on_delete=models.CASCADE)
    address = models.CharField("Адрес", max_length=550)
    longitude = models.CharField("Долгота", max_length=550)
    latitude = models.CharField("Широта", max_length=550)
    range = models.CharField("Диапазон", max_length=550)

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персоналы"
        ordering = ['date']

class PersonalViews(models.Model):
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "История персонала"
        verbose_name_plural = "Истории персоналов"
        ordering = ['date']

class WorkDone(models.Model):
    """Уведомление"""
    STATUS_CHOICES = [
        (0, 'Выполненое'),
        (1, 'Не выполненое'),
    ]
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Пользователь', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField('Время отправки',auto_now_add=True)
    message = models.TextField()
    slug = models.TextField(editable=False)

    class Meta:
        verbose_name = "Проделанная работа"
        verbose_name_plural = "Проделаннае работы"

class Ticket(models.Model):
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    STATUS_CHOICES = [
        (0, 'Новое'),
        (1, 'Обратная связь'),
        (2, 'В процессе'),
        (3, 'Решенный'),
        (4, 'Закрытый'),

    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Автор",on_delete=models.CASCADE)
    themas = models.TextField("Тема")

    class Meta:
        verbose_name = "Тикет"
        verbose_name_plural = "Тикеты"
        ordering = ['date']


class TicketComment(models.Model):
    STATUS_CHOICES = [
        (0, 'Заказчик'),
        (1, 'Поддержка'),
    ]
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1,  editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket", related_name='comments')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    content = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True)

    class Meta:
        verbose_name = "Комментарий тикета"
        verbose_name_plural = "Комментарии тикета"
        ordering = ['-date']

class TicketCommentMedia(models.Model):
    comment = models.ForeignKey('TicketComment', on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='ticket/%Y/%m/%d/tiket_file/')

    def get_file_name(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name = "Файл комментария тикета"
        verbose_name_plural = "Файлы комментариев тикета"
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class GroupsAccess(models.Model):
    """Доступ группы"""
    name = models.CharField(max_length=150, verbose_name='Название')
    link = models.CharField(max_length=150, verbose_name='Ссылка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Доступ группы"
        verbose_name_plural = "Доступы группы"

class Groups(models.Model):
    """Группы"""
    access = models.ManyToManyField(GroupsAccess, verbose_name='Доступ группы', blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.TextField(editable=False)
    name = models.CharField(max_length=150, verbose_name='Название')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Пользователи', blank=True, related_name='groupuser')

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"