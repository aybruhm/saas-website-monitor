# Generated by Django 4.1.5 on 2023-01-08 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0003_notifygroup_notify"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="notifygroup",
            table="notify_group",
        ),
    ]
