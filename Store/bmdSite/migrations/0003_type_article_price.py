# Generated by Django 4.2 on 2023-05-17 19:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmdSite', '0002_store_image_alter_article_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='type_article',
            name='price',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.1)]),
        ),
    ]
