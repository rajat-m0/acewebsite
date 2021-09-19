# Generated by Django 2.2.4 on 2019-08-19 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_auto_20190818_2010"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="course",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "BCA"), (2, "MCA"), (3, "Other")],
                default=None,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="section",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "1A"),
                    (2, "1B"),
                    (3, "1C"),
                    (4, "1D"),
                    (5, "1EA"),
                    (6, "1EB"),
                    (7, "3A"),
                    (8, "3B"),
                    (9, "3C"),
                    (10, "3D"),
                    (11, "3EA"),
                    (12, "3EB"),
                    (13, "5A"),
                    (14, "5B"),
                    (15, "5C"),
                    (16, "5D"),
                    (17, "5EA"),
                    (18, "5EB"),
                    (19, "Other"),
                ],
                default=None,
                null=True,
            ),
        ),
    ]
