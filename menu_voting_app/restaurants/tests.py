from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from .serializers import MenuSerializer
from .models import Restaurant, Menu, Vote
from users.models import Employee
from django.contrib.auth.models import User


class RestaurantCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("restaurant-create")  # Adjust the URL name as needed

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
        self.url = reverse("menu-create")  # Adjust the URL name as needed
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
        self.user = User.objects.create(username="testuser")
        self.employee = Employee.objects.create(
            employee_id="E001",
            user=self.user,
            job_title="Developer",
            date_of_joining=date(2020, 1, 1),
            department="IT",
        )
        self.restaurant = Restaurant.objects.create(
            name="Testaurant",
            address="123 Test St",
            phone_number="1234567890",
            cuisine_type="Italian",
            opening_hours="9 AM - 9 PM",
        )
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant,
            date=date(2023, 9, 12),
            items="Pizza, Pasta",
            votes=0,
        )
        self.menu2 = Menu.objects.create(
            restaurant=self.restaurant,
            date=date(2023, 9, 13),
            items="Burger, Fries",
            votes=0,
        )
        self.menu3 = Menu.objects.create(
            restaurant=self.restaurant,
            date=date(2023, 9, 14),
            items="Salad, Soup",
            votes=0,
        )
        self.url = reverse("vote-caste")

    def test_vote_multiple_menus(self):
        headers = {"HTTP_BUILD_VERSION": "new"}
        data = {
            "employee_id": self.employee.id,
            "voted_date": date(2023, 9, 12),
            "menu_1": self.menu1.id,
            "menu_2": self.menu2.id,
            "menu_3": self.menu3.id,
        }
        response = self.client.post(
            self.url, data, format="json",  **headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 3)
        self.assertEqual(
            Vote.objects.filter(
                employee=self.employee, voted_date=date(2023, 9, 12)
            ).count(),
            3,
        )

    # def test_vote_single_menu(self):
    #     headers = {"HTTP_BUILD_VERSION": "old"}
    #     data = {
    #         "menu_id": self.menu1.id,
    #         "employee_id": self.employee.id,
    #         "points": 3,
    #         "voted_date": date(2023, 9, 14),
    #     }
    #     print(data)
    #     response = self.client.post(
    #         self.url, data, format="json", **headers
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {"message": "Vote recorded successfully"})

    #     # Verify that the vote has been recorded in the database
    #     self.assertTrue(Vote.objects.filter(menu=self.menu, employee=self.employee, voted_date=date.today()).exists())



class VoteResultsForCurrentDayAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('vote-results-for-current-day')  # Adjust the URL name as needed

        # Create sample restaurant
        self.restaurant = Restaurant.objects.create(name='Restaurant 1', address='123 Street')

        # Create sample menus
        self.menu1 = Menu.objects.create(restaurant=self.restaurant, date="2024-09-12", items='Item 1, Item 2')
        self.menu2 = Menu.objects.create(restaurant=self.restaurant, date="2024-09-11", items='Item 3, Item 4')
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        # Create sample employee
        self.employee = Employee.objects.create(user=self.user, department='IT',date_of_joining="2024-09-12")

        # Create sample votes
        today = timezone.now().date()
        Vote.objects.create(menu=self.menu1, employee=self.employee, points=2, voted_date=today)
        Vote.objects.create(menu=self.menu1, employee=self.employee, points=1, voted_date=today)
        Vote.objects.create(menu=self.menu2, employee=self.employee, points=3, voted_date=today)

    def test_get_vote_results_for_current_day(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the menu with the maximum votes is returned
        max_votes_menu = Menu.objects.get(id=self.menu1.id)
        serializer = MenuSerializer(max_votes_menu)
        self.assertEqual(response.data, serializer.data)

    def test_no_votes_for_today(self):
        # Clear today's votes
        Vote.objects.all().delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], 'No votes found for today.')
        self.assertFalse(response.data['success'])


    def test_internal_server_error(self):
        # Simulate an internal server error by raising an exception
        with self.assertRaises(Exception):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('An error occurred while retrieving vote results.', response.data['msg'])
