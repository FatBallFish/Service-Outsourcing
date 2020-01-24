# Generated by Django 3.0.2 on 2020-01-23 19:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
                ('content', models.TextField(verbose_name='内容')),
            ],
            options={
                'verbose_name': '客服',
                'verbose_name_plural': '客服',
                'db_table': 'customer_server',
            },
        ),
    ]
