# Generated by Django 4.1.3 on 2023-03-05 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_analysis_options_remove_analysis_visited_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='anonymous',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
