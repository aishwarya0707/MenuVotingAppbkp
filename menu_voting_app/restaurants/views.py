from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics, status, versioning
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Menu, Restaurant, Vote
from .serializers import (
    MenuSerializer,
    RestaurantSerializer,
    VoteRequestSerializer,
    VoteSerializer,
)


class RestaurantCreateView(generics.CreateAPIView):
    """
    API view to create new restaurant records.
    """

    queryset = (
        Restaurant.objects.all()
    )  # Specifies the queryset used for retrieving restaurant data.
    serializer_class = RestaurantSerializer  # Defines the serializer class to validate and serialize input data.

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for creating a new restaurant.
        """
        serializer = self.get_serializer(
            data=request.data
        )  # Initialize serializer with request data.
        try:
            if serializer.is_valid():
                self.perform_create(
                    serializer
                )  # Save the new restaurant instance to the database.
                headers = self.get_success_headers(
                    serializer.data
                )  # Get headers for the response.
                return Response(
                    {
                        "message": "Restaurant created successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,  # HTTP 201 Created status code.
                    headers=headers,
                )
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },  # Return validation errors.
                status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred during restaurant creation.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 Internal Server Error status code.
            )


class MenuCreateView(generics.CreateAPIView):
    """
    API view to create new menu items.
    """

    queryset = (
        Menu.objects.all()
    )  # Specifies the queryset used for retrieving menu data.
    serializer_class = MenuSerializer  # Defines the serializer class to validate and serialize input data.

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for creating a new menu item.
        """
        serializer = self.get_serializer(
            data=request.data
        )  # Initialize serializer with request data.
        try:
            if serializer.is_valid():
                self.perform_create(
                    serializer
                )  # Save the new menu instance to the database.
                headers = self.get_success_headers(
                    serializer.data
                )  # Get headers for the response.
                return Response(
                    {
                        "message": "Menu item created successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,  # HTTP 201 Created status code.
                    headers=headers,
                )
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },  # Return validation errors.
                status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred during menu creation.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 Internal Server Error status code.
            )


class MenuListView(generics.ListAPIView):
    """
    API view to list all menu items for a specific restaurant.
    """

    serializer_class = (
        MenuSerializer  # Defines the serializer class to serialize the output data.
    )

    def get_queryset(self):
        """
        Retrieves the list of menu items for the specified restaurant.
        """
        try:
            restaurant_id = self.kwargs[
                "restaurant_id"
            ]  # Get the restaurant ID from URL parameters.
            return Menu.objects.filter(
                restaurant_id=restaurant_id
            )  # Filter menus by restaurant ID.
        except Menu.DoesNotExist:
            return (
                Menu.objects.none()
            )  # Return an empty queryset if the restaurant does not exist.


class MenuDetailView(generics.ListAPIView):
    """
    API view to retrieve menu details for the current day.
    """

    serializer_class = (
        MenuSerializer  # Defines the serializer class to serialize the output data.
    )

    def get_queryset(self):
        """
        Retrieves the list of menu items for the current day.
        """
        try:
            today = timezone.now().date()  # Get the current date.
            return Menu.objects.filter(date=today)  # Filter menus by the current date.
        except Exception as e:
            return (
                Menu.objects.none()
            )  # Return an empty queryset in case of any exceptions.

class VoteMenuAPIView(generics.CreateAPIView):
    versioning_class = (
        versioning.AcceptHeaderVersioning
    )  # Specifies the versioning class to handle versioned API requests.

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the API version.
        """
        build_version = self.request.META.get(
            "HTTP_BUILD_VERSION"
        )  # Get the API version from request headers.

        if build_version == "old":
            return VoteSerializer  # Use VoteSerializer for 'old' version.
        elif build_version == "new":
            return VoteRequestSerializer  # Use VoteRequestSerializer for 'new' version.
        return Response(
            {"error": "Invalid API version"}, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for voting, delegates to the appropriate method based on API version.
        """
        serializer_class = (
            self.get_serializer_class()
        )  # Get the serializer class based on API version.
        serializer = serializer_class(
            data=request.data
        )  # Initialize serializer with request data.

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
            )

        try:
            if self.get_serializer_class() == VoteSerializer:
                return self.vote_single_menu(
                    request, serializer
                )  # Handle voting for a single menu item (old version).
            elif self.get_serializer_class() == VoteRequestSerializer:
                return self.vote_multiple_menus(
                    request, serializer
                )  # Handle voting for multiple menu items (new version).
            else:
                return Response(
                    {"error": "Invalid API version"},
                    status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
                )
        except Exception as e:
            return Response(
                {"error": "An error occurred during voting.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 Internal Server Error status code.
            )

    def vote_single_menu(self, request, serializer):
        """
        Handles voting for a single menu item.
        """
        serializer = VoteSerializer(
            data=request.data
        )  # Initialize serializer with request data.
        if serializer.is_valid():
            try:
                menu_id = serializer.validated_data["menu"]
                employee_id = serializer.validated_data["employee"]
                voted_date = timezone.now().date()

                if Vote.objects.filter(
                    menu_id=menu_id, employee_id=employee_id, voted_date=voted_date
                ).exists():
                    return Response(
                        {
                            "error": "You have already voted for this menu today"
                        },  # Return error if the user has already voted today.
                        status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
                    )

                serializer.save()  # Save the vote.
                return Response(
                    {"message": "Vote recorded successfully"},
                    status=status.HTTP_200_OK,  # HTTP 200 OK status code.
                )
            except Exception as e:
                return Response(
                    {
                        "error": "An error occurred while recording the vote.",
                        "details": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 Internal Server Error status code.
                )
        return Response(
            {
                "error": "Invalid data",
                "details": serializer.errors,
            },  # Return validation errors.
            status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
        )

    def vote_multiple_menus(self, request, serializer):
        """
        Handles voting for multiple menu items.
        """
        serializer = VoteRequestSerializer(
            data=request.data
        )  # Initialize serializer with request data.
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                employee = data["employee_id"]
                voted_date = timezone.now().date()
                menu_1, menu_2, menu_3 = data["menu_1"], data["menu_2"], data["menu_3"]

                # Ensure the employee has not voted already today.
                if Vote.objects.filter(
                    employee=employee, voted_date=voted_date
                ).exists():
                    return Response(
                        {
                            "error": "You have already voted for today"
                        },  # Return error if the user has already voted today.
                        status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
                    )

                # Process and save votes for the three menus.
                votes = [(menu_1, 3), (menu_2, 2), (menu_3, 1)]
                for menu, points in votes:
                    Vote.objects.create(
                        menu=menu,
                        employee=employee,
                        points=points,
                        voted_date=voted_date,
                    )

                return Response(
                    {"message": "Votes recorded successfully"},
                    status=status.HTTP_201_CREATED,  # HTTP 201 Created status code.
                )
            except Exception as e:
                return Response(
                    {
                        "error": "An error occurred while recording votes.",
                        "details": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 Internal Server Error status code.
                )
        return Response(
            {
                "error": "Invalid data",
                "details": serializer.errors,
            },  # Return validation errors.
            status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
        )


class VoteResultsForCurrentDayAPIView(generics.GenericAPIView):
    """
    API view to retrieve vote results for the current day.
    """

    serializer_class = (
        MenuSerializer  # Defines the serializer class to serialize the output data.
    )

    def get(self, request, *args, **kwargs):
        """
        Retrieves vote results for the current day.
        """
        try:
            today = timezone.now().date()  # Get the current date.

            # Aggregate votes for each menu for the current day.
            menu_votes = (
                Vote.objects.filter(voted_date=today)
                .values("menu")
                .annotate(total_votes=Sum("points"))
                .order_by("-total_votes")
            )

            if menu_votes:
                # Get the menu with the maximum votes.
                max_votes_menu_id = menu_votes[0]["menu"]
                max_votes_menu = Menu.objects.get(id=max_votes_menu_id)
                total_votes = menu_votes[0]["total_votes"]

                # Serialize and return the result.
                serializer = self.get_serializer(max_votes_menu)
                return Response(
                    {"menu": serializer.data, "total_votes": total_votes},
                    status=status.HTTP_200_OK,  # HTTP 200 OK status code.
                )
            else:
                return Response(
                    {"msg": "No votes found for today.", "success": False},
                    status=status.HTTP_404_NOT_FOUND,  # HTTP 404 Not Found status code.
                )
        except Exception as e:
            return Response(
                {
                    "msg": "An error occurred while retrieving vote results.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 Internal Server Error status code.
            )
