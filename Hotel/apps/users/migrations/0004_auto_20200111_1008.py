# Generated by Django 3.0.2 on 2020-01-11 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200110_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facedata',
            name='sign',
            field=models.CharField(max_length=2048, verbose_name='用户特征'),
        ),
    ]
