# Generated by Django 3.1.4 on 2021-01-15 19:54

import cert_app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                ("internal_num", models.CharField(default=uuid.uuid4, max_length=50)),
                ("public_num", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("qr_code", models.ImageField(blank=True, upload_to="qr_codes")),
                ("is_published", models.BooleanField(default=False)),
                (
                    "pdf",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=cert_app.models.user_directory_path,
                    ),
                ),
                ("views_count", models.IntegerField(default=0)),
                (
                    "emitter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="certificate",
            constraint=models.UniqueConstraint(
                fields=("emitter", "internal_num"), name="unique emitter"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="certificate",
            unique_together={("emitter", "internal_num")},
        ),
    ]
