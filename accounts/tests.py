from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from accounts.serializers import UserCreateSerializers

user = get_user_model()


# UnitTests
class UserCreateSerializersIsValidTests(TestCase):
    def setUp(self):
        self.validate_data = {
            'email': 'test0@gmail.com',
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test',
            're_password': 'test'
        }

        # self.not_valid_data = self.validate_data.copy()
        # self.gmail_not_valid_data['email'] = 'test@gmail'
        # self.not_valid_data['password'] = 'test2'

    def test_user_serializers_is_valid(self):
        serializers = UserCreateSerializers(data=self.validate_data)
        self.assertTrue(serializers.is_valid())
        self.assertEqual(serializers.errors, {})

    def test_user_create_serializers(self):
        serializers = UserCreateSerializers(data=self.validate_data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        self.assertEqual(user.email, 'test0@gmail.com')
        self.assertEqual(user.first_name, 'test')
        self.assertTrue(user.check_password('test'))

    def test_user_serializer_gmail_not_valid(self):
        self.gmail_not_valid_data = self.validate_data.copy()
        self.gmail_not_valid_data['email'] = 'test@gmail'
        serializers = UserCreateSerializers(data=self.gmail_not_valid_data)
        self.assertFalse(serializers.is_valid())
        self.assertEqual(serializers.errors,
                         {'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]})

    def test_user_serializer_password_not_valid(self):
        self.not_valid_data = self.validate_data.copy()
        self.not_valid_data['password'] = 'test2'
        serializers = UserCreateSerializers(data=self.not_valid_data)
        self.assertFalse(serializers.is_valid())
        self.assertEqual(serializers.errors,
                         {'non_field_errors': [ErrorDetail(string='password not equal re password', code='invalid')]}
                         )


# IntegrationTests
class UserRegisterSerializersTests(TestCase):
    def setUp(self):
        self.register_data = {
            'email': 'test0@gmail.com',
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test',
            're_password': 'test'
        }
        self.client = Client()
        self.register_url = reverse('register')

    def test_user_register_serializers(self):
        response = self.client.post(
            self.register_url,
            data=self.register_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'test')


class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('token_obtain_pair')
        get_user_model().objects.create_user(username='test',
                                             email='test@gmail.com',
                                             password='test')

        self.login_data = {
            'email': 'test@gmail.com',
            'password': 'test'
        }

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            data=self.login_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data.keys())
        self.assertIn('refresh', response.data.keys())
