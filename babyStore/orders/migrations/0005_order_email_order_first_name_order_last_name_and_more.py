# Generated by Django 5.1.4 on 2025-01-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pincode',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
