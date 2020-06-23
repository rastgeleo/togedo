from django.test import TestCase
from django.urls import reverse

from .models import Task, TaskList


class TaskListCreateTest(TestCase):

    def test_uses_task_create_template(self):
        response = self.client.get('/list/create/')
        self.assertTemplateUsed(response, 'todo/tasklist_form.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/list/create/', data={'name': 'new list'})

        self.assertEqual(TaskList.objects.count(), 1)
        new_list = TaskList.objects.first()
        self.assertEqual(new_list.name, 'new list')

    def test_redirects_after_POST(self):
        response = self.client.post('/list/create/', data={'name': 'new list'})
        new_list = TaskList.objects.first()
        self.assertRedirects(response, f'/list/{new_list.slug}/')


class TaskListUpdateTest(TestCase):
    def setUp(self):
        self.tasklist = TaskList.objects.create(
            name='new list', slug='new-list'
        )

    def test_can_save_a_POST_request(self):
        data = {
            'name': 'updated list',
            'slug': 'updated-list'
        }
        self.client.post(
            reverse(
                'todo:tasklist_update',
                kwargs={'slug': self.tasklist.slug}), data)
        self.assertEqual(TaskList.objects.count(), 1)
        self.assertEqual(TaskList.objects.first().name, data['name'])

    def test_redirects_after_POST_request(self):
        data = {
            'name': 'updated list',
            'slug': 'updated-list'
        }
        response = self.client.post(
            reverse(
                'todo:tasklist_update',
                kwargs={'slug': self.tasklist.slug}), data)

        self.assertRedirects(
            response, reverse(
                'todo:tasklist_detail', kwargs={'slug': data['slug']}))


class TestListDeleteTest(TestCase):

    def test_can_delete_a_POST_request(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        self.client.post(f'/list/{new_list.slug}/delete/')
        self.assertEqual(TaskList.objects.count(), 0)

    def test_redirects_after_POST(self):
        new_list = TaskList.objects.create(name='new list', slug='new-list')
        response = self.client.post(f'/list/{new_list.slug}/delete/')
        self.assertRedirects(response, reverse('todo:tasklist_list'))


class TaskListViewTest(TestCase):

    def setUp(self):
        lists = []
        for i in range(5):
            tasklist = TaskList(name=f'list{i}', slug=f'list-{i}')
            lists.append(tasklist)
        TaskList.objects.bulk_create(lists)

    def test_uses_task_list_template(self):
        response = self.client.get('/list/')
        self.assertTemplateUsed(response, 'todo/tasklist_list.html')

    def test_displays_task_lists(self):
        lists = TaskList.objects.all()
        response = self.client.get('/list/')

        for list_ in lists:
            self.assertContains(response, list_.name)

    def test_not_displays_deleted_lists(self):
        list_ = TaskList.objects.first()
        list_.delete()
        response = self.client.get('/list/')

        self.assertNotContains(response, list_.name)


class TaskListDetailTest(TestCase):

    def test_uses_tasklist_detail_template(self):
        tasklist = TaskList.objects.create(name="new list", slug="new-list")
        response = self.client.get(f'/list/{tasklist.slug}/')
        self.assertTemplateUsed(response, 'todo/tasklist_detail.html')

    def test_display_task_in_tasklist(self):
        tasklist = TaskList.objects.create(name="new list", slug="new-list")
        task = Task.objects.create(
            name="new task", slug="new-task", tasklist=tasklist)
        response = self.client.get(f'/list/{tasklist.slug}/')
        self.assertContains(response, task.name)


class TaskCreateTest(TestCase):

    def setUp(self):
        self.tasklist = TaskList.objects.create(
            name="new list", slug="new-list")

    def test_uses_task_form_template(self):
        response = self.client.get(f'/list/{self.tasklist.slug}/create/')
        self.assertTemplateUsed(response, 'todo/task_form.html')

    def test_can_save_post_request(self):
        data = {
            'name': 'new task',
            'slug': 'new-task',
            'tasklist': self.tasklist.pk
        }
        self.client.post(f'/list/{self.tasklist.slug}/create/', data)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().name, data['name'])

    def test_redirects_after_post(self):
        data = {
            'name': 'new task',
            'slug': 'new-task',
            'tasklist': self.tasklist.pk
        }
        response = self.client.post(
            f'/list/{self.tasklist.slug}/create/', data)
        self.assertRedirects(response, f'/list/{self.tasklist.slug}/')


class TaskUpdateTest(TestCase):
    def setUp(self):
        self.tasklist = TaskList.objects.create(
            name="new list", slug="new-list")
        self.task = Task.objects.create(
            name="new task", slug="new-task", tasklist=self.tasklist)

    def test_can_save_post_request(self):
        data = {
            'name': 'updated task',
            'slug': 'updated-task',
            'tasklist': self.tasklist.pk
        }
        self.client.post(
            f'/list/{self.tasklist.slug}/{self.task.slug}/update/', data)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().name, data['name'])

    def test_redirects_after_post(self):
        data = {
            'name': 'new task',
            'slug': 'new-task',
            'tasklist': self.tasklist.pk
        }
        response = self.client.post(
            f'/list/{self.tasklist.slug}/{self.task.slug}/update/', data)
        self.assertRedirects(response, f'/list/{self.tasklist.slug}/')


class TaskDeleteTest(TestCase):
    def setUp(self):
        self.tasklist = TaskList.objects.create(
            name="new list", slug="new-list")
        self.task = Task.objects.create(
            name="new task", slug="new-task", tasklist=self.tasklist)

    def test_can_save_post_request(self):
        self.client.post(
            f'/list/{self.tasklist.slug}/{self.task.slug}/delete/')
        self.assertEqual(Task.objects.count(), 0)

    def test_redirects_after_post(self):
        response = self.client.post(
            f'/list/{self.tasklist.slug}/{self.task.slug}/delete/')
        self.assertRedirects(response, f'/list/{self.tasklist.slug}/')


class TaskListModelTest(TestCase):
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
