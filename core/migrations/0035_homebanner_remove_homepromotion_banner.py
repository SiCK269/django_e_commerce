# Generated by Django 4.1.3 on 2023-01-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_homepromotion_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='homepromotion',
            name='banner',
        ),
    ]
