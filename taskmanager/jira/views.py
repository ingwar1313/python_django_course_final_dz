from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, SprintForm, ProjectForm
from django.template import RequestContext
from django.views.generic import DetailView, CreateView, ListView, View, UpdateView
from .models import Tasks, Users
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime as dt
from django.urls import reverse_lazy

# Create your views here.


def index(request):
    # return HttpResponse("<h4>About</h4>")
    # tasks = Task.objects.order_by('-id') #[:1] - только одну запись
    # return render(request, 'jira/index.html', {'title':"Главная страница сайта", "tasks": tasks})
    return render(request, 'jira/about.html')

def about(request):
    return render(request, 'jira/about.html')


@login_required
def create_task(request):
    error = ""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            this_task = form.save(commit=False)
            if request.user.get_role_display() != "Начальник":
                error = "У Вас недостаточно прав,чтобы создать задачу!"
            elif this_task.sprint.date_end < dt.datetime.now().date():
                error = "Нельзя назначить задачу на прошедший спринт"
            else:
                # автоназначение создателя задачи
                this_task.creator = request.user
                this_task.save()
                context = {
                    'form': TaskForm(),
                    'error': f"Задача {this_task.__str__()} создана"
                        }
                return render(request, 'jira/create_task.html', context)
        else:
            error = "Форма неверно заполнена"
        
    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'jira/create_task.html', context)

@login_required
def create_sprint(request):
    error = ""
    if request.method == "POST":
        form = SprintForm(request.POST)
        if form.is_valid():
            this_sprint = form.save(commit=False)
            if request.user.get_role_display() != "Начальник":
                error = "У Вас недостаточно прав,чтобы создать спринт!"
            elif this_sprint.date_start > this_sprint.date_end:
                error = "Дата окончания спринта не может быть раньше даты начала"
            elif this_sprint.date_end < dt.datetime.now().date():
                error = "Нельзя создать прошедший спринт"
            if error == "":
                # автоназначение отдела спринта
                this_sprint.dept = request.user.dept
                this_sprint.save()
                context = {
                    'form': SprintForm(),
                    'error': f"Спринт {this_sprint.__str__()} создан"
                        }
                return render(request, 'jira/create_sprint.html', context)
            else:
                form = SprintForm()
                context = {
                    'form': form,
                    'error': error
                }
                return render(request, 'jira/create_sprint.html', context)
        else:
            error = "Форма неверно заполнена"
        
    form = SprintForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'jira/create_sprint.html', context)

@login_required
def create_project(request):
    error = ""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            if request.user.get_role_display() != "Начальник":
                error = "У Вас недостаточно прав,чтобы создать проект!"
            else:
                form.save()
                return redirect("create_project")
        else:
            error = "Форма неверно заполнена"
        
    form = ProjectForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'jira/create_project.html', context)


# class TaskListView(ListView):
#     """Представление для отображения множества задач.

#     .._ https://docs.djangoproject.com/en/4.1/ref/class-based-views/generic-display/#listview
#     """

#     context_object_name = "tasks_"
#     queryset = Tasks.objects.filter()
#     template_name = "jira/task_list.html"

class TaskList(LoginRequiredMixin, ListView):
    context_object_name = "tasks_"
    template_name = "jira/task_list.html"
    def get_queryset(self):
        # [("1","Начальник"), ("2", "Исполнитель")]
        if self.request.user.get_role_display() == "Начальник":
            # Начальник смотрит задачи, назначенные на свой отдел или неназначенные
            my_dept_query = Users.objects.filter(dept = self.request.user.dept).values('pk')
            my_dept_tasks = Tasks.objects.filter(assignee__in=my_dept_query)
            return my_dept_tasks # Tasks.objects.filter(Q(assignee in self.request.user.dept) | Q(assignee__isnull=True))
        elif self.request.user.get_role_display() == "Исполнитель":
            # Исполнитель смотрит только назначенные на него задачи
            return Tasks.objects.filter(assignee=self.request.user)


class TaskFormView(UpdateView, DetailView):
    """Представление для редактирования одной задачи"""

    context_object_name = "task"
    queryset = Tasks.objects.filter()
    template_name = "task_edit.html"
    model = Tasks
    fields = ["title",
              "task",
              "creator",
              "assignee",
              "status",
              "sprint",
              "change_history"]
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        return super().form_valid(form)