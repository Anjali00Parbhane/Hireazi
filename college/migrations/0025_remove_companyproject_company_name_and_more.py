# Generated by Django 5.0.2 on 2024-02-28 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0024_department_remove_student_current_year_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="companyproject",
            name="company_name",
        ),
        migrations.RemoveField(
            model_name="companyproject",
            name="project_title",
        ),
        migrations.DeleteModel(
            name="Company",
        ),
        migrations.DeleteModel(
            name="CompanyProject",
        ),
    ]
