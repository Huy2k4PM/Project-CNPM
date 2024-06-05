# Generated by Django 5.0.3 on 2024-04-16 13:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0008_alter_payment_method_delete_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='class.product'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='class.shoppingcart'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='shopping_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='class.shoppingcart'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='total_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
