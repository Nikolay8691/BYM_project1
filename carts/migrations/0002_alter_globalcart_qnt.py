# Generated by Django 4.1.3 on 2022-12-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalcart',
            name='qnt',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
