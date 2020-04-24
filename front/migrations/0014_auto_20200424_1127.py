# Generated by Django 2.2.12 on 2020-04-24 04:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0013_article_date_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_create',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания статьи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_publish',
            field=models.DateField(default=datetime.datetime(2020, 4, 24, 4, 27, 2, 600427, tzinfo=utc), verbose_name='Дата публикации статьи'),
        ),
    ]
