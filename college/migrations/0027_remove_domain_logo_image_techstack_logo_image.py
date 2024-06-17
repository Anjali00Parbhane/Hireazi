# Generated by Django 5.0.2 on 2024-02-28 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0026_company_companyproject"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="domain",
            name="logo_image",
        ),
        migrations.AddField(
            model_name="techstack",
            name="logo_image",
            field=models.ImageField(default=1, upload_to="images/"),
            preserve_default=False,
        ),
    ]
