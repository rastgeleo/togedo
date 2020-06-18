from django.shortcuts import get_object_or_404

from .models import Task, TaskList


class TaskGetObjectMixin:

    slug_url_kwarg = 'task_slug'
    tasklist_slug_url_kwarg = 'list_slug'

    def get_object(self, queryset=None):
        task_slug = self.kwargs.get(self.slug_url_kwarg)
        tasklist_slug = self.kwargs.get(self.tasklist_slug_url_kwarg)

        return get_object_or_404(
            Task,
            slug=task_slug,
            tasklist__slug=tasklist_slug
        )


class TaskListContextMixin:
    tasklist_context_object_name = 'tasklist'

    def get_context_data(self, **kwargs):
        """
        Add tasklist object to the context
        """
        if hasattr(self, 'tasklist'):
            tasklist = self.tasklist
        else:
            tasklist_slug = self.kwargs.get(self.tasklist_slug_url_kwarg)
            tasklist = get_object_or_404(TaskList, slug__iexact=tasklist_slug)
        context = {
            self.tasklist_context_object_name: tasklist
        }
        context.update(kwargs)
        return super().get_context_data(**context)
