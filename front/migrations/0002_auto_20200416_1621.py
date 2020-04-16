# Generated by Django 2.2.12 on 2020-04-16 09:21

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='phones',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=25, null=True), blank=True, null=True, size=None, verbose_name='Телефон/телефоны'),
        ),
    ]