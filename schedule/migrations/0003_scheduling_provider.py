# Generated by Django 4.0.3 on 2022-03-23 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0002_scheduling_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduling',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='scheduling', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
