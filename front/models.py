from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django_better_admin_arrayfield.models.fields import ArrayField


# Create your models here.
#todo класс Settings для настроек meta, почты, обратной связи, логгирования и тд
class ArticleKind(models.Model):
    kind = models.CharField(max_length=100, verbose_name="Тип статьи")

    class Meta:
        verbose_name = "Тип статьи"
        verbose_name_plural = "Типы статей"

    def __str__(self):
        return self.kind


class Article(models.Model):
    kind = models.ForeignKey('ArticleKind', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT,
                             verbose_name="Тип статьи")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания статьи")
    title = models.CharField(max_length=250, verbose_name="Заголовок статьи")
    content = models.TextField(verbose_name="Содержание (текст) статьи")
    video = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name="Видео (одно)")

    class Meta:
        ordering = ["-date_create"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return f'{self.kind} -  {self.title} - {self.date_create}'

class Photo(models.Model):
    article = models.ForeignKey('Article', null=True, blank=True, default=None, on_delete=models.CASCADE,
                             verbose_name="Статья")
    photo = models.ImageField(verbose_name="Фотографии (одна или несколько)")

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
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return f'{self.title}'
