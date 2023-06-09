# Generated by Django 4.2 on 2023-05-17 18:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type_Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('text', models.TextField(validators=[django.core.validators.MinLengthValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store', to='bmdSite.store')),
                ('type_arttcle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_article', to='bmdSite.type_article')),
            ],
        ),
    ]
