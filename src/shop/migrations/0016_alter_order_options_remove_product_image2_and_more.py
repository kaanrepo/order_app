# Generated by Django 4.2.9 on 2024-03-07 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_menucategory_image_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='product',
            name='image2',
        ),
        migrations.AlterUniqueTogether(
            name='table',
            unique_together={('name', 'section')},
        ),
    ]
