# Generated by Django 4.2.2 on 2024-02-20 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("strategy", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="strategy",
            name="owner",
        ),
        migrations.AddField(
            model_name="strategy",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
