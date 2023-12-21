# Generated by Django 4.2.7 on 2023-12-05 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заявки', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.RemoveField(
            model_name='service',
            name='status',
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 5, 20, 25, 6, 306576, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(null=True, to='it_app.service', verbose_name='Работы'),
        ),
    ]