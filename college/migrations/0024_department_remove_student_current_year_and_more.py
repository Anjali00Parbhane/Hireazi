# Generated by Django 5.0.2 on 2024-02-28 13:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0023_remove_task_college"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name="student",
            name="current_year",
        ),
        migrations.AddField(
            model_name="college",
            name="website",
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="domain",
            name="logo_image",
            field=models.ImageField(default=1, upload_to="images/"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="creative_score",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="current_yr",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="image_1",
            field=models.ImageField(default=1, upload_to="images/"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="image_2",
            field=models.ImageField(default=1, upload_to="images/"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="innovative_score",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="performance_score",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="societal_score",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="userfriendly_score",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projecttask",
            name="score",
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projecttask",
            name="total_score",
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[
                    (1, "COORDINATOR"),
                    (2, "STUDENT"),
                    (3, "MENTOR"),
                    (4, "COMPANY"),
                ],
                default=1,
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="projecttask",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Completed", "Completed"),
                    ("InProgress", "In Progress"),
                    ("Submitted", "Submitted"),
                    ("Reassigned", "Re Assigned"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.TextField()),
                ("name", models.CharField(max_length=200)),
                ("website", models.CharField(max_length=25)),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyProject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="college.company",
                    ),
                ),
                (
                    "project_title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="college.project",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="mentor",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="college.department"
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="college.department"
            ),
        ),
    ]
