# Generated by Django 2.2.4 on 2019-08-22 17:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0004_auto_20190822_2258"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="icon"
            ),
        ),
    ]
