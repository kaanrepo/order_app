# Generated by Django 4.2.9 on 2024-02-16 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_section_handle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='handle',
        ),
    ]
