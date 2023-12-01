from django.db import models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, unique=True, verbose_name='Ссылка')
    content = models.TextField(verbose_name='Содержимое', **NULLABLE)
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение', **NULLABLE)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}, {self.slug}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
