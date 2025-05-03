from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

user = get_user_model()


class TaskListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task_list_url = reverse('task-list')
        user1 = user.objects.create_user(username='test',
                                         email='test@gmail.com',
                                         password='test')
        self.token = RefreshToken.for_user(user=user1)
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token.access_token}'

    def test_task_list(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
