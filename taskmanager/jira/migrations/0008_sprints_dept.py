# Generated by Django 4.1.5 on 2023-03-12 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jira", "0007_alter_tasks_creator"),
    ]

    operations = [
        migrations.AddField(
            model_name="sprints",
            name="dept",
            field=models.CharField(
                default="Ордапобедит",
                help_text="Отдел",
                max_length=255,
                verbose_name="Отдел",
            ),
        ),
    ]