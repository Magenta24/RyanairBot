# Generated by Django 4.2.4 on 2023-09-02 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Airport",
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
                ("country", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("code", models.CharField(max_length=4)),
                ("currency", models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name="Flight",
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
                ("date", models.DateField()),
                ("price", models.IntegerField()),
                ("currency", models.CharField(max_length=3)),
                ("search_date", models.DateTimeField()),
                (
                    "destination_airport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dest_city",
                        to="ryanair_webapp.airport",
                    ),
                ),
                (
                    "origin_airport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="origin_city",
                        to="ryanair_webapp.airport",
                    ),
                ),
            ],
        ),
    ]