# Generated by Django 5.0.2 on 2024-03-07 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0037_rename_current_year_panel_current_y_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectreview',
            name='panel',
        ),
        migrations.AlterField(
            model_name='panel',
            name='current_y',
            field=models.IntegerField(default=1),
        ),
    ]
