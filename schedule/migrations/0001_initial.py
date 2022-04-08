# Generated by Django 4.0.3 on 2022-03-14 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Scheduling",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_time", models.DateTimeField()),
                ("client_name", models.CharField(max_length=200)),
                ("client_email", models.EmailField(max_length=254)),
                ("client_phone", models.CharField(max_length=20)),
            ],
        ),
    ]
