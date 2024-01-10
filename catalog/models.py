
from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Продавец', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.CharField(max_length=150, verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    is_active_version = models.BooleanField(default=False, verbose_name='Активная версия')

    def __str__(self):
        return f'{self.name} - {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


