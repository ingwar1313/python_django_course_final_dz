from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime as dt

# Create your models here.


roles = [("1","Начальник"), ("2", "Исполнитель")]
depts = [("1", "Ордапобедит"), ("2", "Нужнопостроитьзиккурат"), ("3","Очемшумятдеревья")]

class Users(AbstractUser):
    """Пользователи"""
    # name = models.CharField(help_text='ФИО', max_length=255)
    email = models.EmailField(help_text='e-mail')
    role = models.CharField(help_text="Роль пользователя", choices=roles, max_length=255, verbose_name="Роль")
    dept = models.CharField(help_text="Отдел", choices=depts, max_length=255,  verbose_name="Отдел")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Projects(models.Model):
    """Проекты"""
    name = models.CharField(help_text='Название', max_length=255)
    description = models.TextField(help_text='Описание')

    def __str__(self):
        return f"{self.pk} - {self.name}"

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Sprints(models.Model):
    """Спринты"""
    project_id = models.ForeignKey(Projects, help_text='ИД Проекта',on_delete=models.CASCADE)
    dept = models.CharField(help_text="Отдел", choices=depts, max_length=255,  verbose_name="Отдел", default="1")
    date_start = models.DateField(help_text='Дата начала спринта')
    date_end = models.DateField(help_text='Дата окончания спринта')

    def save(self, *args, **kwargs) -> None: 
        if self.date_start > self.date_end:
            return None
        if self.date_end < dt.datetime.now().date():
            return None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Проект {self.project_id.name}, отдел {self.get_dept_display()} , {self.date_start}-{self.date_end}"
    
    class Meta:
        verbose_name = 'Спринт'
        verbose_name_plural = 'Спринты'

statuses = ((0,"Не назначено"),
(1, "Назначено"),
(2, "В работе"),
(3, "Подтверждение выполнения"),
(4, "Вернулось в работу"),
(5, "Выполнено"),
(6, "Отменено"))

class Tasks(models.Model):
    title = models.CharField(help_text='Название задачи', max_length=255)
    task = models.TextField(help_text="Описание задачи")
    creator = models.CharField(help_text='ИД Создателя', max_length=255)
    assignee = models.ForeignKey(Users, help_text="ИД Исполнителя", on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(help_text="Статус задачи", choices=statuses, max_length=255)
    sprint = models.ForeignKey(Sprints, help_text="Спринт, когда нужно сделать", on_delete=models.SET_NULL, blank=True, null=True)
    change_history = models.TextField(help_text="История изменения задачи", blank=True, null=True)

    def __str__(self):
        return f"{self.id}:{self.title} - {self.status}"
    
    def save(self, *args, **kwargs) -> None: 
        # Если нет исполнителя, то не назначено
        if not self.assignee:
            self.status = "Не назначено"
        # Если не назначено и есть исполнитель, то назначено
        if not self.status and self.assignee:
            self.status = "Назначено"
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


