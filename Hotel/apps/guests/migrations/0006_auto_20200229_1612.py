# Generated by Django 3.0.2 on 2020-02-29 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0005_auto_20200219_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guestvisitor',
            options={'managed': False, 'verbose_name': '访客申请记录', 'verbose_name_plural': '访客申请记录'},
        ),
    ]
