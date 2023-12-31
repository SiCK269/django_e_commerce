# Generated by Django 4.1.3 on 2023-01-14 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='Header', max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='rating',
            name='item',
        ),
        migrations.AddField(
            model_name='rating',
            name='post',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.post'),
            preserve_default=False,
        ),
    ]
