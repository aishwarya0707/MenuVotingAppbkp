# Generated by Django 5.1.1 on 2024-09-13 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0012_rename_votes_menu_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="points",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
