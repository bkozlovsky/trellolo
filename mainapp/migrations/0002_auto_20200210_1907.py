# Generated by Django 3.0.3 on 2020-02-10 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('NW', 'New'), ('INP', 'In Progress'), ('INQ', 'In QA'), ('RD', 'Ready'), ('DN', 'Done')], max_length=12),
        ),
    ]