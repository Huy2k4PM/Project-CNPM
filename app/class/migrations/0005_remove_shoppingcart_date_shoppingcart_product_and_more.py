# Generated by Django 5.0.4 on 2024-04-13 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0004_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='date',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='class.product'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='quantity',
            field=models.IntegerField(default=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='total_price',
            field=models.IntegerField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='total_price',
            field=models.IntegerField(default=True),
        ),
    ]