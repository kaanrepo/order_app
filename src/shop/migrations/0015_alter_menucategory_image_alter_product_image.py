# Generated by Django 4.2.10 on 2024-02-29 07:57

from django.db import migrations, models
import shop.models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_section_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.category_image_upload_path, validators=[shop.validators.validate_file_extension, shop.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.product_image_upload_path, validators=[shop.validators.validate_file_extension, shop.validators.validate_file_size]),
        ),
    ]
