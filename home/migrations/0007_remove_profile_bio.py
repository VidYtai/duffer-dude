# Generated by Django 3.2.13 on 2023-11-18 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]
