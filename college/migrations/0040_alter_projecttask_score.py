# Generated by Django 5.0.3 on 2024-03-07 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0039_college_college_type_college_registration_no_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projecttask",
            name="score",
            field=models.IntegerField(default=0),
        ),
    ]
