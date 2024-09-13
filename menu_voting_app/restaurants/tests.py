from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Employee

from .models import Menu, Restaurant, Vote
from .serializers import MenuSerializer


class RestaurantCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("restaurant-create")

    def test_create_restaurant_success(self):
        """
        Ensure we can create a new restaurant.
        """
        data = {
            "name": "Test Restaurant",
            "address": "123 Test Street",
            "phone_number": "123-456-7890",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Restaurant created successfully.")
        self.assertTrue(Restaurant.objects.filter(name="Test Restaurant").exists())

    def test_create_restaurant_invalid_data(self):
        """
        Ensure invalid data returns a 400 response.
        """
        data = {
            "name": "",  # Invalid name
            "address": "123 Test Street",
            "phone_number": "123-456-7890",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_create_restaurant_duplicate_name(self):
        """
        Ensure duplicate restaurant name returns a 400 response.
        """
        Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            phone_number="123-456-7890",
        )
        data = {
            "name": "Test Restaurant",  # Duplicate name
            "address": "456 Another Street",
            "phone_number": "987-654-3210",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_create_restaurant_server_error(self):
        """
        Simulate a server error during restaurant creation.
        """
        data = {
            "name": "Test Restaurant",
            "address": "123 Test Street",
            "phone_number": "123-456-7890",
        }
        with self.assertRaises(Exception):
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertIn("message", response.data)


class MenuCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("menu-create")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            phone_number="123-456-7890",
        )

    def test_create_menu_item_success(self):
        """
        Ensure we can create a new menu item.
        """
        data = {
            "restaurant": self.restaurant.id,
            "date": "2024-09-12",
            "items": "Test Item 1, Test Item 2",
            "votes": 0,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Menu item created successfully.")
        self.assertTrue(
            Menu.objects.filter(restaurant=self.restaurant, date="2024-09-12").exists()
        )

    def test_create_menu_item_invalid_data(self):
        """
        Ensure invalid data returns a 400 response.
        """
        data = {
            "restaurant": self.restaurant.id,
            "date": "",  # Invalid date
            "items": "Test Item 1, Test Item 2",
            "votes": 0,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_create_menu_item_duplicate(self):
        """
        Ensure duplicate menu item returns a 400 response.
        """
        Menu.objects.create(
            restaurant=self.restaurant,
            date="2024-09-12",
            items="Test Item 1, Test Item 2",
            votes=0,
        )
        data = {
            "restaurant": self.restaurant.id,
            "date": "2024-09-12",  # Duplicate date for the same restaurant
            "items": "Test Item 3, Test Item 4",
            "votes": 0,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_create_menu_item_server_error(self):
        """
        Simulate a server error during menu item creation.
        """
        data = {
            "restaurant": self.restaurant.id,
            "date": "2024-09-12",
            "items": "Test Item 1, Test Item 2",
            "votes": 0,
        }
        with self.assertRaises(Exception):
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertIn("message", response.data)


class VoteMenuAPIViewTestCase(APITestCase):
    def setUp(self):
        # Create sample data
        self.restaurant = Restaurant.objects.create(
            name="Sample Restaurant",
            address="123 Main St",
            phone_number="123-456-7890",
            cuisine_type="Italian",
        )
        self.employee = Employee.objects.create(
            employee_id="E001",
            user=self._create_test_user(username="john_doe", password="password123"),
            job_title="Chef",
            date_of_joining=timezone.now().date(),
            department="Kitchen",
        )
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant, date="2024-09-10", items="Pizza", votes=0
        )
        self.menu2 = Menu.objects.create(
            restaurant=self.restaurant, date="2024-09-11", items="Burger", votes=0
        )
        self.menu3 = Menu.objects.create(
            restaurant=self.restaurant, date="2024-09-12", items="Sushi", votes=0
        )
        self.vote_url = reverse("vote-caste")  # Ensure this matches your URL name

    def _create_test_user(self, username, password):
        """
        Helper method to create a test user.
        """
        user = User.objects.create_user(username=username, password=password)
        return user

    def test_vote_single_menu_old_version(self):
        self.client.credentials(HTTP_BUILD_VERSION="old")
        data = {
            "menu": self.menu1.id,
            "employee": self.employee.id,
            "points": 5,
            "voted_date": timezone.now().date(),
        }
        response = self.client.post(self.vote_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Vote recorded successfully")

    def test_vote_multiple_menus_new_version(self):
        self.client.credentials(HTTP_BUILD_VERSION="new")
        data = {
            "employee_id": self.employee.id,
            "voted_date": timezone.now().date(),
            "menu_1": self.menu1.id,
            "menu_2": self.menu2.id,
            "menu_3": self.menu3.id,
        }
        response = self.client.post(self.vote_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Votes recorded successfully")

    def test_invalid_data(self):
        self.client.credentials(HTTP_BUILD_VERSION="new")
        data = {
            "employee_id": self.employee.id,
            "voted_date": timezone.now().date(),
            # Missing menu fields
        }
        response = self.client.post(self.vote_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("details", response.data)
