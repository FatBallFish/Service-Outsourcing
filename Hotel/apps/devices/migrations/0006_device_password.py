# Generated by Django 3.0.2 on 2020-02-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_device_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='password',
            field=models.CharField(default='', max_length=64, verbose_name='登录密码'),
        ),
    ]
