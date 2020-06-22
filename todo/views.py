from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView,\
    DeleteView

from .models import Task, TaskList
from .forms import TaskForm, TaskUpdateForm, TaskListForm
from .utils import TaskGetObjectMixin, TaskListContextMixin


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


class TaskListUpdate(UpdateView):
    model = TaskList
    form_class = TaskListForm
    template_name = 'todo/tasklist_update_form.html'


class TaskListDelete(DeleteView):
    model = TaskList
    success_url = reverse_lazy('todo:tasklist_list')


class TaskCreate(TaskListContextMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('todo:tasklist_list', )
    tasklist_slug_url_kwarg = 'list_slug'

    def get_initial(self):
        """
        set initial tasklist from url kwargs.
        """
        list_slug = self.kwargs.get(self.tasklist_slug_url_kwarg)
        self.tasklist = get_object_or_404(TaskList, slug__iexact=list_slug)
        initial = {'tasklist': self.tasklist}
        initial.update(self.initial)
        return initial

    def get_success_url(self):
        try:
            url = self.object.tasklist.get_absolute_url()
        except AttributeError:
            raise ImproperlyConfigured(
                "No URL to redirect to.  Either provide a url or define"
                " a get_absolute_url method on the Model.")
        return url


class TaskDetail(TaskGetObjectMixin, DetailView):
    model = Task


class TaskUpdate(TaskGetObjectMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        try:
            url = self.object.tasklist.get_absolute_url()
        except AttributeError:
            raise ImproperlyConfigured(
                "No URL to redirect to.  Either provide a url or define"
                " a get_absolute_url method on the Model.")
        return url


class TaskDelete(TaskGetObjectMixin, DeleteView):
    model = Task

    def get_success_url(self):
        redirect_url = self.object.tasklist.get_absolute_url()
        return redirect_url
