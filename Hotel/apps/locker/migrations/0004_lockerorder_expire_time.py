# Generated by Django 3.0.2 on 2020-03-10 20:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locker', '0003_auto_20200310_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='lockerorder',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='过期时间'),
        ),
    ]
