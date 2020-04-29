# Generated by Django 2.2.12 on 2020-04-29 04:26

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0017_auto_20200429_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date_publish'], 'verbose_name': 'Статья', 'verbose_name_plural': '2 - Статьи'},
        ),
        migrations.AlterModelOptions(
            name='articlekind',
            options={'verbose_name': 'Тип статьи', 'verbose_name_plural': '3 - Типы статей'},
        ),
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['title'], 'verbose_name': 'Партнёр', 'verbose_name_plural': '1 - Партнёры'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'Отчёт', 'verbose_name_plural': '4 - Отчеты'},
        ),
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Настройки', 'verbose_name_plural': '5 - Настройки'},
        ),
    ]
