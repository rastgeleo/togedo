from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Task, TaskList


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('slug', 'completed')
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'id_name', 'placeholder': 'Add a task'}),
            'text': forms.Textarea(attrs={
                'id': 'id_text', 'placeholder': 'Add a description'}),
            'due': forms.DateTimeInput(attrs={
                'id': 'id_due', 'placeholder': 'YYYY-MM-DD HH:MM:SS'})
        }

    def save(self, commit=True):
        task = super().save(commit=False)
        if not task.pk:
            date_str = timezone.now().strftime('%y%m%d')
            task.slug = "{}-{}".format(slugify(task.name)[:56], date_str)
        task.save()
        self.save_m2m()
        return task


class TaskUpdateForm(TaskForm):
    class Meta(TaskForm.Meta):
        exclude = ('slug',)


class TaskListForm(forms.ModelForm):

    class Meta:
        model = TaskList
        exclude = ('slug',)

    def clean_name(self):
        new_name = self.cleaned_data['name']
        if new_name == 'create':
            raise ValidationError('list name can not be "create".')
        return new_name

    def save(self, commit=True):
        tasklist = super().save(commit=False)
        if not tasklist.pk:
            tasklist.slug = slugify(tasklist.name)
        tasklist.save()
        self.save_m2m()
        return tasklist
