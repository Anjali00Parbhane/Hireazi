# Generated by Django 5.0.3 on 2024-03-08 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0042_rename_stundet_no_pendingprojectstudentrequest_stundent_no"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pendingprojectstudentrequest",
            old_name="stundent_no",
            new_name="student_no",
        ),
    ]
