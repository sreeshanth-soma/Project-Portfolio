# Generated by Django 5.1.5 on 2025-02-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='linkedin_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
