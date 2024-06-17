# Generated by Django 5.0.2 on 2024-02-18 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0006_alter_student_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='abstract',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='support_doc',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
