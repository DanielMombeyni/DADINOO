# Generated by Django 5.1.5 on 2025-04-30 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_coinpricing_plan_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='postman',
        ),
        migrations.AddField(
            model_name='chat',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.plan'),
        ),
    ]
