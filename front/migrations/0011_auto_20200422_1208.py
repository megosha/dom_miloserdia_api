# Generated by Django 2.2.12 on 2020-04-22 05:08

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0010_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='mailto',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.EmailField(max_length=254), size=None, verbose_name='Почта, для уведомлений обратной связи'),
        ),
    ]