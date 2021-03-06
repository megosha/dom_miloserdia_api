# Generated by Django 2.2.12 on 2020-04-17 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_auto_20200416_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover',
            field=models.ImageField(blank=True, upload_to='images/covers/', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='images/articles/', verbose_name='Фотографии (одна или несколько)'),
        ),
    ]
