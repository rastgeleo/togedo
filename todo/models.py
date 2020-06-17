from django.db import models
from django.urls import reverse
from django.utils import timezone


class TaskList(models.Model):
    name = models.CharField(
        'list name',
        max_length=63,
        unique=True
    )
    slug = models.SlugField(
        'slug for list',
        max_length=63,
        unique=True
    )
    createdat = models.DateTimeField(
        'list created time',
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'todo:tasklist_detail',
            kwargs={'slug': self.slug}
            )

    def get_task_create_url(self):
        return reverse('todo:task_create', kwargs={'list_slug': self.slug})


class Task(models.Model):
    name = models.CharField(max_length=63)
    slug = models.SlugField(
        max_length=63,
        unique=True
    )
    text = models.TextField(
        'description',
        blank=True
    )
    createdat = models.DateTimeField(
        'date created',
        auto_now_add=True
    )
    due = models.DateTimeField(
        'date due',
        null=True,
        blank=True
    )
    completed = models.BooleanField(
        'completed',
        default=False
    )
    tasklist = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}: {}".format(
            self.name,
            self.due.strftime('%Y-%m-%d %H:%M')
            )

    def get_absolute_url(self):
        return reverse(
            'todo:task_detail',
            kwargs={'list_slug': self.tasklist.slug, 'task_slug': self.slug}
            )

    # def get_create_url(self):
    #     return reverse('todo:task_create')

    # def get_update_url(self):
    #     return reverse('todo:task_update', kwargs={'slug': self.slug})

    # def get_delete_url(self):
    #     return reverse('todo:task_delete', kwargs={'slug': self.slug})

    # def isoverdue(self):
    #     return (not self.completed) and (self.due < timezone.now())

