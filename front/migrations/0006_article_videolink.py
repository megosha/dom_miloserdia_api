# Generated by Django 2.2.12 on 2020-04-17 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_auto_20200417_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='videolink',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео (одно)'),
        ),
    ]
