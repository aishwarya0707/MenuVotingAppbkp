# Generated by Django 5.1.1 on 2024-09-13 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0011_remove_restaurant_opening_hours_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="menu",
            old_name="votes",
            new_name="points",
        ),
    ]
