# Generated by Django 4.1.5 on 2023-01-09 20:14

import apps.monitor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0005_rename_down_counts_historicalstats_downtime_counts_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthenticationSchema",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "basic_auth",
                    models.JSONField(
                        blank=True,
                        default="",
                        null=True,
                    ),
                ),
                (
                    "bearer_auth",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
            ],
            options={
                "verbose_name_plural": "Authentication Schemas",
                "db_table": "authentication_schemas",
            },
        ),
        migrations.AddField(
            model_name="websites",
            name="has_authentication",
            field=models.BooleanField(default=False),
        ),
    ]
