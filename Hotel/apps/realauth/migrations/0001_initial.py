# Generated by Django 3.0.2 on 2020-01-26 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RealAuth',
            fields=[
                ('id_type', models.CharField(choices=[('sfz', '中国大陆身份证'), ('other', '其他')], default='sfz', max_length=10, verbose_name='证件类型')),
                ('ID', models.CharField(max_length=18, primary_key=True, serialize=False, verbose_name='证件号')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('male', '先生'), ('female', '女士')], max_length=6, verbose_name='性别')),
                ('nation', models.CharField(blank=True, max_length=10, null=True, verbose_name='民族')),
                ('birthday', models.DateField(verbose_name='出生年月')),
                ('address', models.TextField(max_length=100, null=True, verbose_name='住址')),
                ('organization', models.CharField(max_length=30, verbose_name='签发机关')),
                ('date_start', models.DateField(verbose_name='有效期_始')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='有效期_末')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '实名认证库',
                'verbose_name_plural': '实名认证库',
                'db_table': 'realauth',
            },
        ),
    ]
