from django.db import models
from django.urls import reverse


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=63)
    slug = models.SlugField(
        max_length=63,
        unique=True
    )
    text = models.TextField()
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

    def __str__(self):
        return "{}: {}".format(self.name, self.due.strftime('%Y-%m-%d %H:%M'))

    def get_absolute_url(self):
        return reverse('todo:task_detail', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('todo:task_create')

    def get_update_url(self):
        return reverse('todo:task_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('todo:task_delete', kwargs={'slug': self.slug})
