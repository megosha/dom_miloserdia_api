# Generated by Django 2.2.12 on 2020-04-28 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0015_auto_20200424_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_publish',
            field=models.DateTimeField(verbose_name='Дата публикации статьи'),
        ),
    ]