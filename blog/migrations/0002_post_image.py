# Generated by Django 4.1.3 on 2022-12-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, default='', null=True, upload_to='uploads/'),
        ),
    ]
