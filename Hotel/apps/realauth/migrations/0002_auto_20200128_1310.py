# Generated by Django 3.0.2 on 2020-01-28 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realauth',
            name='address',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='住址'),
        ),
        migrations.AlterField(
            model_name='realauth',
            name='date_start',
            field=models.DateField(blank=True, null=True, verbose_name='有效期_始'),
        ),
    ]