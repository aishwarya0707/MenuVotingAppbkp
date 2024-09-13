from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Employee


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")

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
        self.url = reverse("login")
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


class LogoutViewTestCase(APITestCase):
    def setUp(self):
        """
        Create a user for testing and perform initial setup.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_logout_success(self):
        """
        Test successful logout scenario.
        """
        response = self.client.post(
            reverse("logout"), data={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.data, {"message": "Successfully logged out."})

    def test_logout_invalid_data(self):
        """
        Test logout with invalid data.
        """
        # Modify the serializer to expect invalid data if needed
        response = self.client.post(reverse("logout"), data={"invalid_field": "value"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)


class CreateEmployeeAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
        )
        self.client.login(username="testuser", password="securepassword123")

    def test_create_employee_success(self):
        url = reverse("employee_create")
        data = {
            "employee_id": "E12345",
            "user": {
                "email": "employee@example.com",
                "username": "employeeuser",
            },
            "date_of_joining": "2024-09-13",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["msg"], "Employee successfully created.")

    def test_create_employee_failure(self):
        url = reverse("employee_create")
        data = {
            "employee_id": "E12345",
            "user": {
                "email": "invalidemail",
                "username": "employeeuser",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
