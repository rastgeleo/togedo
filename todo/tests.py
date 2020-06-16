from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Task


class TaskMainTest(TestCase):

    def test_uses_main_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'todo/task_main.html')

    def test_displays_uncompleted_items_only(self):
        Task.objects.create(
            name='item1', slug='item1', text='item1', completed=False)
        Task.objects.create(
           name='item2', slug='item2', text='item2', completed=True)

        response = self.client.get('/')
        self.assertIn('item1', response.content.decode())
        self.assertNotIn('item2', response.content.decode())

    def test_can_save_a_POST_request(self):
        some_time = timezone.now() + timedelta(days=30)
        time_str = some_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'name': 'item',
            'text': 'item text',
            'due': time_str
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
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_POST(self):
        self.client.get('/')
        self.assertEqual(Task.objects.count(), 0)


class TaskOverdueTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/todo/overdue/')
        self.assertTemplateUsed(response, 'todo/task_list.html')

    def test_display_overdue_task(self):
        Task.objects.create(
            name='overdue item',
            text='a bit late',
            slug='overdue-item',
            due=timezone.now() - timedelta(days=3),
            completed=False
        )
        Task.objects.create(
            name='non overdue item',
            text='a bit late',
            slug='non-overdue-item',
            due=timezone.now() + timedelta(days=3),
            completed=False
        )
        response = self.client.get('/todo/overdue/')
        self.assertIn('overdue item', response.content.decode())
        self.assertNotIn('non overdue item', response.content.decode())


class TaskModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        Task.objects.create(
            name='First item',
            slug='first-item',
            text='First item text'
        )

        Task.objects.create(
            name='Second item',
            slug='second-item',
            text='Second item text'
        )

        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 2)

        first_saved_item = tasks[0]
        second_saved_item = tasks[1]
        self.assertEqual(first_saved_item.name, 'First item')
        self.assertEqual(second_saved_item.name, 'Second item')
