# Generated by Django 4.2.10 on 2024-02-10 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_orderitem_price_menucategory_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='handle',
        ),
    ]