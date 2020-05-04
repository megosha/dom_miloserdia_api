from datetime import datetime

from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.models.fields import ArrayField


# Create your models here.
class ArticleKind(models.Model):
    kind = models.CharField(max_length=100, verbose_name="Тип статьи")

    class Meta:
        verbose_name = "Тип статьи"
        verbose_name_plural = "3 - Типы статей"

    def __str__(self):
        return self.kind


class Article(models.Model):
    kind = models.ForeignKey('ArticleKind', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT,
                             verbose_name="Тип статьи")
    instagram_id = models.CharField(max_length=100, default=None, blank=True, null=True,
                                    verbose_name="id статьи в instagram")
    date_create = models.DateField(auto_now_add=True, verbose_name="Дата создания статьи")
    date_publish = models.DateTimeField(verbose_name="Дата публикации статьи")
    title = models.CharField(max_length=250, verbose_name="Заголовок статьи")
    cover = models.FileField(upload_to='images/covers/', blank=True, verbose_name="Обложка статьи")
    content = models.TextField(verbose_name="Содержание (текст) статьи")
    videolink = models.TextField(null=True, blank=True, verbose_name="Ссылка на видео (одно)")
    videocover = models.FileField(upload_to='images/covers/', blank=True, verbose_name="Обложка видео")

    class Meta:
        ordering = ["-date_publish"]
        verbose_name = "Статья"
        verbose_name_plural = "2 - Статьи"

    def __str__(self):
        return f'{self.kind} -  {self.title} - {self.date_create}'

class Photo(models.Model):
    article = models.ForeignKey('Article', null=True, blank=True, default=None, on_delete=models.CASCADE,
                             verbose_name="Статья")
    photo = models.ImageField(upload_to='images/articles/', verbose_name="Фотографии (одна или несколько)")

    def __str__(self):
        return f'{self.photo.name}'

class Partner(models.Model):
    # если есть сайт, то по нажатию на лого - на сайт, иначе на страницу партнера на сайте
    title = models.CharField(max_length=100, verbose_name="Наименование партнёра")
    logo = models.ImageField(upload_to='images/logos/', blank=True, verbose_name="Логотип")
    important = models.BooleanField(default=False, verbose_name="Отобразить в блоке важных")
    site = models.CharField(max_length=100, blank=True, verbose_name="Сайт")
    description = models.TextField(null=True, blank=True, verbose_name="Краткое описание")
    activity = models.CharField(max_length=250, blank=True, verbose_name="Сфера деятельности")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.CharField(max_length=250, blank=True, verbose_name="Адрес")
    phones = ArrayField(models.CharField(max_length=25, null=True, blank=True), null=True, blank=True, verbose_name="Телефон/телефоны")

    class Meta:
        ordering = ["title"]
        verbose_name = "Партнёр"
        verbose_name_plural = "1 - Партнёры"

    def __str__(self):
        return f'{self.title}'


class Report(models.Model):
    period = models.CharField(max_length=100, verbose_name="Период/год")
    title = models.CharField(max_length=100, verbose_name="Наименование файла")
    file = models.FileField(upload_to='files/', blank=True, verbose_name="Файл с отчетом")

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "4 - Отчеты"

    def __str__(self):
        return f'{self.title}'

class Settings(models.Model):
    instagram_id = models.CharField(max_length=20, default='', blank=True, null=True, verbose_name="User id аккаунта в instagram")
    rapidapi_url = models.URLField(default='', blank=True, null=True, verbose_name="Адрес запроса к rapidapi")
    rapidapi_header = JSONField(default=dict, blank=True, verbose_name="Заголовок запроса к rapidapi")
    mailto = ArrayField(models.EmailField(), verbose_name="Почта, для уведомлений обратной связи")
    metadescr = models.TextField(default='', blank=True, null=True, verbose_name="Meta Description")
    metakeywords = models.TextField(default='', blank=True, null=True, verbose_name="Meta Keyword")
    default_cover = models.ImageField(upload_to='images/covers/', blank=True, verbose_name="Обложка статьи по умолчанию")
    default_videocover = models.ImageField(upload_to='images/covers/', blank=True, verbose_name="Обложка видео по умолчанию")

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "5 - Настройки"

    def __str__(self):
        return f'{self.mailto}'