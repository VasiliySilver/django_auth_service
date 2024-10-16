from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from faker import Faker
import random
import jwt

fake = Faker()


def generate_phone_number():
    return f"+7{random.randint(9000000000, 9999999999)}"


class AuthenticationTests(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("user_registration")
        self.verify_otp_url = reverse("otp_verification")
        self.token_url = reverse("token_obtain_pair")
        self.token_verify_url = reverse("token_verify")
        self.protected_url = reverse("protected")
        self.phone_number = generate_phone_number()
        self.password = fake.password(length=12)
        self.otp = "1234"  # Фиксированный OTP для тестов

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_user_registration(self):
        # Delete existing user if exists
        CustomUser.objects.filter(phone_number=self.phone_number).delete()

        data = {"phone_number": self.phone_number}
        response = self.client.post(self.register_url, data)
        print(f"Registration response: {response.content}")
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Registration failed. Errors: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(
            response.data["message"],
            "User registered successfully. Use OTP '1234' to verify.",
        )

        # Check if the user was created
        user = CustomUser.objects.get(phone_number=self.phone_number)
        self.assertFalse(user.is_active)
        self.assertEqual(user.otp, "1234")

    def test_otp_verification(self):
        self.test_user_registration()

        data = {"phone_number": self.phone_number, "otp": self.otp}
        response = self.client.post(self.verify_otp_url, data)
        print(f"OTP verification response: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Check if the user is actually activated
        user = CustomUser.objects.get(phone_number=self.phone_number)
        print(f"User active status after OTP verification: {user.is_active}")
        self.assertTrue(user.is_active)

    def test_token_obtain(self):
        self.test_otp_verification()  # Это должно активировать пользователя

        data = {
            "phone_number": self.phone_number,
        }
        response = self.client.post(self.token_url, data)
        print(f"Token obtain response: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_inactive_user(self):
        # Регистрируем пользователя, но не активируем его
        self.test_user_registration()

        data = {
            "phone_number": self.phone_number,
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No active account found with the given credentials", str(response.content))

    # def test_token_verify(self):
    #     self.test_user_registration()
    #     self.test_otp_verification()

    #     response = self.client.post(
    #         self.token_url,
    #         {"phone_number": self.phone_number, "password": self.password},
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     token = response.data["access"]

    #     # Выводим содержимое токена для отладки
    #     decoded_token = jwt.decode(token, options={"verify_signature": False})
    #     print(f"Decoded token: {decoded_token}")

    #     data = {"token": token}
    #     response = self.client.post(self.token_verify_url, data)
    #     if response.status_code != status.HTTP_200_OK:
    #         print(
    #             f"Token verify failed. Status: {response.status_code}, Data: {response.data}"
    #         )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["detail"], "Token is valid.")

    def test_protected_view(self):
        self.test_token_obtain()

        response = self.client.post(
            self.token_url,
            {"phone_number": self.phone_number, "password": self.password},
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "This is a protected resource.")

    def test_register_with_existing_phone_number(self):
        self.test_user_registration()

        data = {"phone_number": self.phone_number, "password": fake.password(length=12)}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
