# Generated by Django 4.1.3 on 2022-12-05 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_alter_category_options_alter_product_status_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qnt', models.IntegerField()),
                ('gp_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gp_by', to='products.globalprice')),
                ('sales_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slist_by', to='products.salelist')),
            ],
        ),
    ]