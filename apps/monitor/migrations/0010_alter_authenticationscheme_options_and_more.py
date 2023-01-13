# Generated by Django 4.1.5 on 2023-01-13 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0009_remove_authenticationscheme_basic_auth_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="authenticationscheme",
            options={
                "ordering": ["-date_created"],
                "verbose_name_plural": "Authentication Schemes",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalstats",
            options={
                "ordering": ["-date_created"],
                "verbose_name_plural": "Historial Stats",
            },
        ),
        migrations.AlterModelOptions(
            name="notifygroup",
            options={
                "ordering": ["-date_created"],
                "verbose_name_plural": "Notify Group",
            },
        ),
        migrations.AlterModelOptions(
            name="people",
            options={"ordering": ["-date_created"], "verbose_name_plural": "People"},
        ),
        migrations.AlterModelOptions(
            name="websites",
            options={"ordering": ["-date_created"], "verbose_name_plural": "Websites"},
        ),
    ]