# Generated by Django 4.1.3 on 2023-01-05 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_item_depth_alter_item_height_alter_item_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='banner_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='category',
            name='banner_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='collection',
            name='banner_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
