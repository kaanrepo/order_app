# Generated by Django 4.2.9 on 2024-02-01 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_menucategory_handle_menuitem_handle_product_handle_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'unit', 'size')},
        ),
    ]
