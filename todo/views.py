from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView,\
    DeleteView

from .models import Task, TaskList
from .forms import TaskForm, TaskUpdateForm, TaskListForm


class TaskMain(View):
    template_name = 'todo/task_main.html'
    form_class = TaskForm
    model = Task

    def get(self, request):
        queryset = self.model.objects.filter(completed=False).order_by('due')
        context = {'form': self.form_class(), 'task_list': queryset}
        return render(request, self.template_name, context=context)

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('task_main')
        else:
            queryset = (self.model.objects.filter(completed=False)
                        .order_by('due'))
            context = {'form': bound_form, 'task_list': queryset}
            return render(request, self.template_name, context=context)


class TaskListList(ListView):
    model = TaskList


class TaskListDetail(DetailView):
    model = TaskList


class TaskListCreate(CreateView):
    model = TaskList
    form_class = TaskListForm


class TaskDetail(DetailView):
    model = Task
    slug_url_kwarg = 'task_slug'


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    tasklist_context_object_name = 'tasklist'
    tasklist_slug_url_kwarg = 'list_slug'

    def get_initial(self):
        list_slug = self.kwargs.get('list_slug')
        tasklist = get_object_or_404(TaskList, slug__iexact=list_slug)
        initial = {'tasklist': tasklist}
        initial.update(self.initial)
        return initial

    def get_context_data(self, **kwargs):
        """
        Add tasklist to context to get access to tasklist model methods.
        """
        tasklist_slug = self.kwargs.get(self.tasklist_slug_url_kwarg)
        tasklist = get_object_or_404(TaskList, slug__iexact=tasklist_slug)
        context = {
            self.tasklist_context_object_name: tasklist
        }
        context.update(kwargs)
        return super().get_context_data(**context)



# class TaskUpdate(UpdateView):
#     model = Task
#     form_class = TaskUpdateForm
#     template_name_suffix = '_update_form'


# class TaskDelete(DeleteView):
#     model = Task
#     success_url = reverse_lazy('todo:task_list')
