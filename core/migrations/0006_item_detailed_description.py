# Generated by Django 4.1.3 on 2022-11-18 08:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_item_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='detailed_description',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
