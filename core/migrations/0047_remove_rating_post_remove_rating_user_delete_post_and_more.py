# Generated by Django 4.1.3 on 2023-01-14 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_post_remove_rating_item_rating_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='post',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
