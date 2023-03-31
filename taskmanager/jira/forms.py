from .models import Tasks, Sprints, Projects, Users

from django.forms import ModelForm, TextInput, Textarea, SelectDateWidget, ModelChoiceField
from django.forms.widgets import Select

class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "task", "assignee", "sprint"] # из models
        widgets =   {"title": TextInput(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите название" # аттрибуты, которые изначально в create.html прописывали
                        }),
                    "task": Textarea(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите описание"}),
                    "assignee": Select(attrs={'class': 'form-control',
                        'placeholder':"Выберите,на кого назначить"}),
                    "sprint": Select(attrs={'class': 'form-control',
                        'placeholder':"Выберите спринт, к концу которого должно быть сделано"})
        }

class SprintForm(ModelForm):
    project_id = ModelChoiceField(queryset=Projects.objects.all())
    class Meta:
        model = Sprints
        fields = ["date_start", "date_end", "project_id"] # из models
        widgets =   {"date_start": SelectDateWidget(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите дату начала спринта" 
                        }),
                    "date_end": SelectDateWidget(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите дату окончания спринта"}),
                    "project_id": Select(attrs={'class': 'form-control'})
        }

class ProjectForm(ModelForm):
    class Meta:
        model=Projects
        fields = ["name", "description"]
        widgets = {
            "name": TextInput(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите название" # аттрибуты, которые изначально в create.html прописывали
                        }),
            "description": Textarea(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите описание"})
        }

class TaskChangeForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ["title",
              "task",
              "creator",
              "assignee",
              "status",
              "sprint",
              "change_history"] # из models
        widgets =   {"title": TextInput(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите название" 
                        }),
                    "task": Textarea(attrs={
                        'class': 'form-control',
                        'placeholder':"Введите описание"}),
                    "assignee": Select(attrs={'class': 'form-control',
                        'placeholder':"Выберите,на кого назначить"}),
                    "sprint": Select(attrs={'class': 'form-control',
                        'placeholder':"Выберите спринт, к концу которого должно быть сделано"})
        }