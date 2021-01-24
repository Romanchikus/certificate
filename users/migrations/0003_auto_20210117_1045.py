# Generated by Django 3.1.5 on 2021-01-17 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210116_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='api_key',
            field=models.CharField(editable=False, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='hashed_key',
            field=models.CharField(editable=False, max_length=255, unique=True),
        ),
    ]