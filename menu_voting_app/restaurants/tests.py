from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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


class VoteMenuViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Create test data
        self.user = User.objects.create(username="tester@example.com")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.menu = Menu.objects.create(
            restaurant=self.restaurant, votes=0, date="2024-09-09"
        )

        self.employee = Employee.objects.create(
            employee_id="tester", user=self.user, date_of_joining=date.today()
        )

    def test_vote_single_menu(self):
        url = reverse("vote-caste")
        headers = {"HTTP_BUILD_VERSION": "old"}

        data = {
            "menu_id": self.menu.id,
            "employee_id": self.employee.id,
        }

        response = self.client.post(url, data, format="json", **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Vote recorded successfully"})

    def test_vote_invalid_menu_id(self):
        url = reverse("vote-caste")
        headers = {"HTTP_BUILD_VERSION": "old"}

        data = {
            "menu_id": 999,  # Invalid menu ID
            "employee_id": self.employee.id,
        }

        response = self.client.post(url, data, format="json", **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Menu does not exist"})

    def test_vote_invalid_employee_id(self):
        url = reverse("vote-caste")
        headers = {"HTTP_BUILD_VERSION": "old"}

        data = {
            "menu_id": self.menu.id,
            "employee_id": 999,  # Invalid employee ID
        }

        response = self.client.post(url, data, format="json", **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Employee ID is not valid"})


class VoteResultsForCurrentDayAPIViewTest(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Restaurant A"
        )  # Create a Restaurant instance
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant, votes=0, date="2024-09-10"
        )
        self.menu2 = Menu.objects.create(
            restaurant=self.restaurant, votes=0, date="2024-09-12"
        )
        self.menu3 = Menu.objects.create(
            restaurant=self.restaurant, votes=0, date="2024-09-13"
        )
        self.url = reverse("vote-results-for-current-day")

    def test_get_vote_results_no_votes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["msg"], "No votes found for today.")
