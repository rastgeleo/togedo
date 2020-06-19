from django.test import TestCase

from .models import Task, TaskList


class TaskMainTest(TestCase):

    def test_displays_task(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        Task.objects.create(
            name='new task',
            slug='new-task',
            tasklist=new_list)

        response = self.client.get('/')
        self.assertContains(response, 'new task')

    def test_can_save_a_POST_request(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        data = {
            'name': 'item',
            'text': 'item text',
            'tasklist': new_list.pk
            }
        self.client.post('/', data=data)

        new_item = Task.objects.first()
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(new_item.text, 'item text')

    def test_redirects_after_POST(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        data = {
            'name': 'item',
            'text': 'item text',
            'tasklist': new_list.pk
            }
        response = self.client.post('/', data=data)

        self.assertRedirects(response, '/')

    def test_only_saves_items_when_POST(self):
        self.client.get('/')
        self.assertEqual(Task.objects.count(), 0)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/list/create/', data={'name': 'new list'})

        self.assertEqual(TaskList.objects.count(), 1)
        new_list = TaskList.objects.first()
        self.assertEqual(new_list.name, 'new list')

    def test_redirects_after_POST(self):
        response = self.client.post('/list/create/', data={'name': 'new list'})
        new_list = TaskList.objects.first()
        self.assertRedirects(response, f'/list/{new_list.slug}/')


class TaskListTest(TestCase):
    def test_saving_and_retrieving_tasklist(self):
        new_list = TaskList()
        new_list.name = 'new list'
        new_list.slug = 'new-list'
        new_list.save()

        saved_list = TaskList.objects.first()
        self.assertEqual(saved_list, new_list)

    def test_saving_and_retrieving_task(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        new_task = Task()
        new_task.name = 'new task'
        new_task.slug = 'new-task'
        new_task.test = 'new task description'
        new_task.tasklist = new_list
        new_task.save()

        saved_task = Task.objects.first()
        self.assertEqual(saved_task, new_task)

    def test_saving_and_retrieving_multiple_task(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        task_one = Task()
        task_one.name = 'new task'
        task_one.slug = 'new-task'
        task_one.test = 'new task description'
        task_one.tasklist = new_list
        task_one.save()

        task_two = Task()
        task_two.name = 'new task 2'
        task_two.slug = 'new-task-two'
        task_two.test = 'new task description'
        task_two.tasklist = new_list
        task_two.save()

        task_count = Task.objects.count()
        first_saved_task = Task.objects.all()[1]
        second_saved_task = Task.objects.all()[0]

        self.assertEqual(task_count, 2)
        self.assertEqual(first_saved_task.name, 'new task')
        self.assertEqual(second_saved_task.name, 'new task 2')
