# Generated by Django 5.1.5 on 2025-05-08 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_chat_postman_chat_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL),
        ),
    ]
