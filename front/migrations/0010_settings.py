# Generated by Django 2.2.12 on 2020-04-21 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailto', models.EmailField(max_length=254, verbose_name='Почта, для уведомлений обратной связи')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]