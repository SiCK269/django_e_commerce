# Generated by Django 4.1.3 on 2022-12-26 12:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0031_alter_item_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='seller',
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ManyToManyField(related_name='items', to=settings.AUTH_USER_MODEL),
        ),
    ]
