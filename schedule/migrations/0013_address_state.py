# Generated by Django 4.0.3 on 2022-04-01 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default='', max_length=2, verbose_name='Estado'),
            preserve_default=False,
        ),
    ]
