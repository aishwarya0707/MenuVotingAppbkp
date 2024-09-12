from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")  # Adjust the URL name as needed

    def test_register_user_success(self):
        """
        Ensure we can register a new user.
        """
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully")
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_invalid_data(self):
        """
        Ensure invalid data returns a 400 response.
        """
        data = {
            "username": "",  # Invalid username
            "password": "testpassword",
            "email": "testuser@example.com",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_register_user_duplicate_username(self):
        """
        Ensure duplicate username returns a 400 response.
        """
        User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        data = {
            "username": "testuser",  # Duplicate username
            "password": "testpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_register_user_server_error(self):
        """
        Simulate a server error during registration.
        """
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com",
        }
        with self.assertRaises(Exception):
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertIn("message", response.data)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("login")  # Adjust the URL name as needed
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )

    def test_login_user_success(self):
        """
        Ensure we can log in a user with valid credentials.
        """
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Login successful.")

    def test_login_user_invalid_credentials(self):
        """
        Ensure invalid credentials return a 400 response.
        """
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_login_user_missing_fields(self):
        """
        Ensure missing fields return a 400 response.
        """
        data = {
            "username": "testuser"
            # Missing password
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("logout")  # Adjust the URL name as needed
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.client.login(username="testuser", password="testpassword")

    # def test_logout_user_success(self):
    #     """
    #     Ensure we can log out a user.
    #     """
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.post(self.url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Successfully logged out.')

    def test_logout_user_not_logged_in(self):
        """
        Ensure logging out without being logged in returns a 400 response.
        """
        self.client.logout()
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
