# Generated by Django 5.1.5 on 2025-05-12 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_wallet_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='chat',
            constraint=models.UniqueConstraint(condition=models.Q(('status', 'open')), fields=('user', 'plan'), name='unique_open_chat_per_user_plan'),
        ),
    ]
