# Generated by Django 5.1.4 on 2024-12-11 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_like_unique_together_remove_like_post_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MissingPetReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('last_seen', models.CharField(max_length=255)),
                ('date_last_seen', models.DateField()),
                ('contact_info', models.CharField(max_length=255)),
                ('pet_picture', models.ImageField(upload_to='missing_pets/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missing_pet_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
