# Generated by Django 3.0.3 on 2020-02-20 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20200219_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='date_edited',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]