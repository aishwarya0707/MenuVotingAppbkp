from django.urls import path

from .views import (MenuCreateView, MenuDetailView, RestaurantCreateView,
                    VoteMenuView, VoteResultsForCurrentDayAPIView)

urlpatterns = [
    path(
        "create-restaurant/", RestaurantCreateView.as_view(), name="restaurant-create"
    ),
    path("upload-menu/", MenuCreateView.as_view(), name="menu-create"),
    path("current-day-menus/", MenuDetailView.as_view(), name="current-day-menus"),
    path("caste-votes/", VoteMenuView.as_view(), name="vote-caste"),
    path(
        "restaurant-votes/",
        VoteResultsForCurrentDayAPIView.as_view(),
        name="vote-results-for-current-day",
    ),
]
