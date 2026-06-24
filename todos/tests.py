from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_string_representation_is_title(self):
        task = Task.objects.create(title="Buy milk")
        self.assertEqual(str(task), "Buy milk")

    def test_new_task_defaults_to_not_completed(self):
        task = Task.objects.create(title="Walk dog")
        self.assertFalse(task.completed)


class TaskViewTests(TestCase):
    def test_task_list_page_loads(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)

    def test_posting_a_title_creates_a_task(self):
        self.client.post(reverse('task_list'), {'title': 'Read a book'})
        self.assertTrue(Task.objects.filter(title='Read a book').exists())

    def test_toggle_flips_completed_status(self):
        task = Task.objects.create(title="Test toggle")
        self.client.post(reverse('task_toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_delete_removes_the_task(self):
        task = Task.objects.create(title="Delete me")
        self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
