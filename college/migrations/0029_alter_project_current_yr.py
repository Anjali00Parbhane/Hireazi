# Generated by Django 5.0.2 on 2024-02-29 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0028_alter_project_creative_score_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="current_yr",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
