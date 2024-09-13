from django.urls import path

from .views import MenuCreateView  # View for uploading new menu items
from .views import (
    MenuDetailView,
)  # View for retrieving menu details for the current day
from .views import MenuListView  # View for listing menus for a specific restaurant
from .views import RestaurantCreateView  # View for creating new restaurants
from .views import VoteMenuAPIView  # View for creating or submitting votes for menus
from .views import (
    VoteResultsForCurrentDayAPIView,
)  # View for retrieving vote results for the current day

urlpatterns = [
    # URL pattern for creating a new restaurant
    # URL: /create-restaurant/
    path(
        "create-restaurant/", RestaurantCreateView.as_view(), name="restaurant-create"
    ),
    # URL pattern for uploading a new menu item
    # URL: /upload-menu/
    path("upload-menu/", MenuCreateView.as_view(), name="menu-create"),
    # URL pattern for listing all menus for a specific restaurant
    # URL: /<int:restaurant_id>/get-menus/
    # <int:restaurant_id> is a path parameter representing the ID of the restaurant
    path("<int:restaurant_id>/get-menus/", MenuListView.as_view(), name="menu-list"),
    # URL pattern for retrieving menu details for the current day
    # URL: /current-day-menus
    path("current-day-menus/", MenuDetailView.as_view(), name="current-day-menus"),
    # URL pattern for submitting votes for menus
    # URL: /votes/
    path("caste-votes/", VoteMenuAPIView.as_view(), name="vote-caste"),
    # URL pattern for retrieving vote results for the current day
    # URL: /restaurant-votes/
    path(
        "restaurant-votes/",
        VoteResultsForCurrentDayAPIView.as_view(),
        name="vote-results-for-current-day",
    ),
]
