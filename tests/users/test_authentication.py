from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from faker import Faker

fake = Faker()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.verify_otp_url = reverse('verify-otp')
        self.token_url = reverse('token_obtain_pair')
        self.phone_number = fake.phone_number()
        self.password = fake.password(length=12)

    def test_user_registration(self):
        data = {
            'phone_number': self.phone_number,
            'password': self.password
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(phone_number=self.phone_number).exists())

    def test_otp_verification(self):
        user = CustomUser.objects.create_user(phone_number=self.phone_number, password=self.password)
        
        data = {
            'phone_number': self.phone_number,
            'otp': '1234'  # Предполагаем, что это правильный OTP
        }
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

    def test_token_obtain(self):
        user = CustomUser.objects.create_user(phone_number=self.phone_number, password=self.password)
        user.is_verified = True
        user.save()

        data = {
            'phone_number': self.phone_number,
            'password': self.password
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_unverified_user_cannot_obtain_token(self):
        CustomUser.objects.create_user(phone_number=self.phone_number, password=self.password)

        data = {
            'phone_number': self.phone_number,
            'password': self.password
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_otp(self):
        CustomUser.objects.create_user(phone_number=self.phone_number, password=self.password)
        
        data = {
            'phone_number': self.phone_number,
            'otp': '9999'  # Неправильный OTP
        }
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_phone_number(self):
        CustomUser.objects.create_user(phone_number=self.phone_number, password=self.password)

        new_password = fake.password(length=12)
        data = {
            'phone_number': self.phone_number,
            'password': new_password
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

