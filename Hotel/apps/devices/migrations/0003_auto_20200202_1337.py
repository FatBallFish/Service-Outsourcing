# Generated by Django 3.0.2 on 2020-02-02 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20200126_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_content',
            field=models.TextField(blank=True, null=True, verbose_name='设备描述'),
        ),
    ]
