from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('slug', 'completed')

    def save(self, commit=True):
        task = super().save(commit=True)
        # createdat field is created after task is saved on database.
        date_str = task.createdat.strftime('%y%m%d')
        task.slug = "{}-{}".format(slugify(task.name)[:56], date_str)
        task.save()
        return task


class TaskUpdateForm(TaskForm):
    class Meta(TaskForm.Meta):
        exclude = ('slug',)

