# Generated by Django 4.1.3 on 2023-01-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_item_depth_item_height_item_weight_item_width'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='depth',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='height',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='width',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
