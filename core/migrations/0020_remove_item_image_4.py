# Generated by Django 4.1.3 on 2022-12-17 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_seller_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image_4',
        ),
    ]
