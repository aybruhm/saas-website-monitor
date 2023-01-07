# Generated by Django 4.1.5 on 2023-01-07 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="People",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("email_address", models.EmailField(max_length=254, unique=True)),
            ],
            options={
                "verbose_name_plural": "People",
                "db_table": "people",
            },
        ),
        migrations.CreateModel(
            name="Websites",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("site", models.URLField(unique=True)),
            ],
            options={
                "verbose_name_plural": "Websites",
                "db_table": "websites",
            },
        ),
        migrations.CreateModel(
            name="NotifyGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=30, unique=True)),
                (
                    "emails",
                    models.ManyToManyField(
                        related_name="people_notify_group", to="monitor.people"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Notify Group",
                "db_table": "Notify Group",
            },
        ),
        migrations.CreateModel(
            name="HistoricalStats",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("up_counts", models.PositiveBigIntegerField(default=0)),
                ("down_counts", models.PositiveBigIntegerField(default=0)),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="monitor.websites",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Historial Stats",
                "db_table": "historical_stats",
            },
        ),
    ]
