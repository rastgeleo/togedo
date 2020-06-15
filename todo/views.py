from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView,\
    DeleteView

from .models import Task
from .forms import TaskForm, TaskUpdateForm


class TaskMain(View):
    template_name = 'todo/task_main.html'
    form_class = TaskForm
    model = Task

    def get(self, request):
        queryset = self.model.objects.filter(completed=False)
        context = {'form': self.form_class(), 'task_list': queryset}
        return render(request, self.template_name, context=context)

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('task_main')
        else:
            queryset = self.model.objects.filter(completed=False)
            context = {'form': bound_form, 'task_list': queryset}
            return render(request, self.template_name, context=context)


class TaskList(ListView):
    queryset = Task.objects.filter(completed=False)


class TaskCompletedList(ListView):
    queryset = Task.objects.filter(completed=True)
    template_name = 'todo/task_completed_list.html'


class TaskDetail(DetailView):
    model = Task


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm


class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('todo:task_list')
