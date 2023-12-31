# Generated by Django 4.1.3 on 2022-11-24 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_item_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(default='uncategorized', on_delete=django.db.models.deletion.CASCADE, to='core.category'),
        ),
    ]
