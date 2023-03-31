# Generated by Django 4.1.5 on 2023-02-28 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jira", "0002_rename_task_tasks_alter_users_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="users", name="name",),
        migrations.AlterField(
            model_name="users",
            name="dept",
            field=models.CharField(
                choices=[
                    (1, "Ордапобедит"),
                    (2, "Нужнопостроитьзиккурат"),
                    (3, "Очемшумятдеревья"),
                ],
                help_text="Отдел",
                max_length=255,
                verbose_name="Отдел",
            ),
        ),
        migrations.AlterField(
            model_name="users",
            name="role",
            field=models.CharField(
                choices=[(1, "Начальник"), (2, "Исполнитель")],
                help_text="Роль пользователя",
                max_length=255,
                verbose_name="Роль",
            ),
        ),
    ]