# Generated by Django 4.1.3 on 2022-12-24 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_brand_image_alter_category_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='homepromotion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_1',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_2',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_3',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_main',
            field=models.ImageField(upload_to=''),
        ),
    ]
