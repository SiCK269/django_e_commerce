# Generated by Django 4.1.3 on 2022-12-26 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0032_remove_item_seller_item_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='seller',
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL),
        ),
    ]
