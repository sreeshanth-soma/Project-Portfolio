# Generated by Django 5.1.5 on 2025-04-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0007_project_name_alter_project_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('Personal Project', 'Personal Project'), ('Real-Time Project', 'Real-Time Project'), ('Minor Project', 'Minor Project'), ('Major Project', 'Major Project'), ('Research Project', 'Research Project'), ('Coursework Project', 'Coursework Project')], default='Personal Project', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
