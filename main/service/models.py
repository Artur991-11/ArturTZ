from django.db import models
from django.urls import reverse
import uuid
from ckeditor.fields import RichTextField
from django.core.validators import (FileExtensionValidator)

# Create your models here.

class Tariff(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    price = models.IntegerField("Цена", null=True, blank=True)
    days = models.IntegerField("Дни", null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    title = models.CharField("Заголовок", max_length=255, null=True, blank=True)
    content = models.TextField("Содержимое", null=True, blank=True)
    parameters = models.ManyToManyField('TariffParameter', verbose_name="Параметры", null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, null=True, blank=True)
    image = models.ImageField("Изображение", upload_to='tariffs/', null=True, blank=True)
    preview = models.ImageField("Превью", upload_to='tariffs/previews/', null=True, blank=True  )
    huge_description = RichTextField("Описание")
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

class TariffParameter(models.Model):
    name = models.CharField("Название",max_length=255, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    count = models.IntegerField("Количество", null=True, blank=True)

    class Meta:
        verbose_name = "Параметр тарифа"
        verbose_name_plural = "Параметры тарифов"

class ServiceCategory(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержимое")
    image = models.ImageField("Изображение", upload_to='services_categories/')
    preview = models.ImageField("Превью", upload_to='services_categories/previews/')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Родительская категория")

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"

class Service(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    price = models.IntegerField("Цена", null=True, blank=True)
    days = models.IntegerField("Дни", null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    title = models.CharField("Заголовок", max_length=255, null=True, blank=True)
    content = models.TextField("Содержимое", null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, verbose_name="Категория", null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, null=True, blank=True)
    image = models.FileField("Изображение", upload_to='services/', null=True, blank=True)
    preview = models.ImageField("Превью", upload_to='services/previews/', null=True, blank=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


"""Оборудония"""
class Categories(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True,verbose_name='Описание')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Родитель')

    def get_absolute_url(self):
        return reverse('categories', kwargs={"slug": self.slug})

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Manufacturers(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.FileField(upload_to='manufacturers/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение', validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])],)
    cover = models.FileField(upload_to='manufacturers/%Y/%m/%d/', blank=True, null=True, verbose_name='Обложка', validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])],)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    def get_absolute_url(self):
        return reverse('manufacturers', kwargs={"slug": self.slug})

    class Meta:
        db_table = 'manufacturers'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name

class ProductsGallery(models.Model):
    """Изображения продуктов"""
    create = models.DateTimeField(auto_now=True,blank=True,null=True)
    image = models.FileField("Изображение", upload_to="product/%Y/%m/%d/", blank=True, null=True, default='default/blogs/cover.png', validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])],)
    products = models.ForeignKey(to='Products', on_delete=models.CASCADE, verbose_name='Образец Продукта')

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

class Variable(models.Model):
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True,  verbose_name='URL')
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    content = models.TextField(blank=True, null=True, verbose_name='Контент')

    class Meta:
        db_table = 'variable'
        verbose_name = 'Вариация'
        verbose_name_plural = 'Вариации'

    def __str__(self):
        return self.name

class Atribute(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    variable = models.ForeignKey(to=Variable, on_delete=models.CASCADE, verbose_name='Вариация')
    slug = models.SlugField(max_length=500,  blank=True, null=True,  verbose_name='URL')
    content = models.TextField(blank=True, null=True, verbose_name='Контент')
    image = models.FileField("Изображение", upload_to="product/%Y/%m/%d/", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])],)

    class Meta:
        db_table = 'atribute'
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return f'{self.variable} - {self.name}'

class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True, verbose_name='URL')
    price = models.DecimalField(default=0.00, max_digits=11, decimal_places=0, verbose_name='Цена')
    wholesale_price = models.DecimalField(default=0.00, max_digits=11, decimal_places=0, verbose_name='Оптовая цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.FileField("Изображение", upload_to="product/%Y/%m/%d/", blank=True, null=True, default='default/blogs/cover.png', validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'jpeg', 'jpg', 'svg'])])
    name = models.CharField(max_length=500, verbose_name='Название')
    fragment = RichTextField(max_length=250, blank=True, null=True, verbose_name='отрывок')
    description = RichTextField(blank=True, null=True, verbose_name='Описание')
    title = models.CharField(max_length=150, blank=True, null=True, verbose_name='Заголовок')
    content = models.TextField(blank=True, null=True, verbose_name='Мета-описание')
    category = models.ManyToManyField(to=Categories, verbose_name='Категория')
    brand = models.ForeignKey(to=Manufacturers, on_delete=models.CASCADE, verbose_name='Производитель')
    atribute = models.ManyToManyField(Atribute, blank=True, verbose_name='Атрибуты')
    order = models.BooleanField("Под заказ", default=False)
    create = models.DateTimeField(auto_now=True, blank=True, null=True)
    #
    #Габариты

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)

    def __str__(self):
        # Ensure that all components are convertible to strings
        return f'{self.name or "No Name"} - В наличии: {self.quantity}'

    def get_absolute_url(self):
        return reverse("products", kwargs={"slug": self.slug})

class Storage(models.Model):
    """Страницы"""
    name = models.CharField("Название", help_text="Название", max_length=550)
    address = models.CharField("Адрес", max_length=550)
    zip_index = models.CharField("Почтовый индекс", max_length=550)
    longitude = models.CharField("Долгота", max_length=550)
    latitude = models.CharField("Широта", max_length=550)
    content = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'Номер -{self.id} адрес - {self.address}'

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

class StockAvailability(models.Model):
    """Изображения продуктов"""
    create = models.DateTimeField(auto_now=True, blank=True, null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Образец Продукта')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name='Склад')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{self.products} Количество - {self.quantity}'

    class Meta:
        verbose_name = "Наличие на складе"
        verbose_name_plural = "Наличия на складах"