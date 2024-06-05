# Generated by Django 5.0.6 on 2024-05-18 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0012_remove_orderdetail_payment_orderdetail_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='total_price',
            field=models.FloatField(blank=True),
        ),
    ]