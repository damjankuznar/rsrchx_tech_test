# Generated by Django 2.1.5 on 2019-01-28 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OPEN", "Open"),
                            ("PENDING", "Pending"),
                            ("COMPLETED", "Completed"),
                            ("REJECTED", "Rejected"),
                        ],
                        default="OPEN",
                        max_length=9,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="CartItems",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, default=1, max_digits=18)),
                ("cart", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="backend.Cart")),
            ],
        ),
        migrations.CreateModel(
            name="Food",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=18)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name="cartitems",
            name="food",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="backend.Food"),
        ),
    ]
