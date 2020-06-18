from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Task, TaskList


class TaskMainTest(TestCase):

    def setUp(self):
        self.tasklist = TaskList.objects.create(name='my list')

    def test_uses_main_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'todo/task_main.html')

    def test_displays_uncompleted_items_only(self):
        Task.objects.create(
            name='item1', slug='item1', text='item1', completed=False,
            tasklist=self.tasklist)
        Task.objects.create(
           name='item2', slug='item2', text='item2', completed=True,
           tasklist=self.tasklist)

        response = self.client.get('/')
        self.assertIn('item1', response.content.decode())
        self.assertNotIn('item2', response.content.decode())

    def test_can_save_a_POST_request(self):
        some_time = timezone.now() + timedelta(days=30)
        time_str = some_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'name': 'item',
            'text': 'item text',
            'due': time_str,
            'tasklist': self.tasklist
            }
        self.client.post('/', data=data)
        self.assertEqual(Task.objects.count(), 1)
        new_item = Task.objects.first()
        self.assertEqual(new_item.text, 'item text')

        # Django stores datetime as UTC in database
        self.assertEqual(
            timezone.localtime(new_item.due).strftime('%Y-%m-%d %H:%M:%S'),
            time_str
            )

    def test_redirects_after_POST(self):
        data = {
            'name': 'item',
            'text': 'item text',
            'tasklist': self.tasklist
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_POST(self):
        self.client.get('/')
        self.assertEqual(Task.objects.count(), 0)


class TaskListDeleteTest(TestCase):

    def test_uses_delete_template(self):
        response = self.client.get('todo:tasklist_delete')
        self.assertTemplateUsed(response, 'todo/tasklist_confirm_delete.html')