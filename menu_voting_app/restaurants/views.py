from datetime import date

from django.db.models import F, Sum
from django.utils import timezone
from rest_framework import generics, status, versioning
from rest_framework.response import Response

from users.models import Employee

from .models import Menu, Restaurant, Vote
from .serializers import MenuSerializer, RestaurantSerializer


class RestaurantCreateView(generics.CreateAPIView):
    """
    API view to create new restaurant records.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for creating a new restaurant.
        """
        serializer = self.get_serializer(data=request.data)
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
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred during restaurant creation.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MenuCreateView(generics.CreateAPIView):
    """
    API view to create new menu items.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

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
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred during menu creation.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MenuDetailView(generics.ListAPIView):
    """
    API view to retrieve menu details for the current day.
    """

    serializer_class = MenuSerializer

    def get_queryset(self):
        """
        Retrieves the list of menu items for the current day.
        """
        try:
            today = timezone.now().date()
            return Menu.objects.filter(date=today)  # Filter menus by the current date.
        except Exception as e:
            return (
                Menu.objects.none()
            )  # Return an empty queryset in case of any exceptions.


class VoteMenuView(generics.GenericAPIView):
    serializer_class = MenuSerializer
    versioning_class = versioning.AcceptHeaderVersioning

    def post(self, request, format=None):
        # Check the 'Build-Version' header in the request
        build_version = request.META.get("HTTP_BUILD_VERSION")

        # Process the request based on the build version
        if build_version == "old":
            return self.vote_single_menu(request)
        elif build_version == "new":
            return self.vote_multiple_menus(request)

        # Return an error response for invalid API version
        return Response(
            {"error": "Invalid API version"}, status=status.HTTP_400_BAD_REQUEST
        )

    def vote_single_menu(self, request):

        menu_id = request.data.get("menu_id")
        employee_id = request.data.get("employee_id")

        # Retrieve the menu instance
        menu = Menu.objects.filter(id=menu_id).first()
       
        # Check if the employee exists
        if not Employee.objects.filter(id=employee_id).exists():
            return Response(
                {"error": "Employee ID is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the menu exists
        if not menu:
            return Response(
                {"error": "Menu does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the employee has already voted for the current day and menu
        if Vote.objects.filter(
            menu=menu, employee_id=employee_id, voted_date=date.today()
        ).exists():
            return Response(
                {"error": "You have already voted for this menu today"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Increment the votes count for the menu
        menu.votes = F("votes") + 1
        menu.save()

        # Create a vote record for the employee
        Vote.objects.create(menu=menu, employee_id=employee_id)

        return Response(
            {"message": "Vote recorded successfully"}, status=status.HTTP_200_OK
        )

    def vote_multiple_menus(self, request):
        # Get the vote data and employee ID from the request data
        vote_data = request.data.get("votes")
        employee_id = request.data.get("employee_id")

        # Check if the vote data is valid
        if not isinstance(vote_data, list) or len(vote_data) != 3:
            return Response(
                {"error": "Invalid vote data"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the employee exists
        if not Employee.objects.filter(id=employee_id).exists():
            return Response(
                {"error": "Provide a valid employee ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Process each vote in the vote data
        for vote in vote_data:
            menu_id = vote.get("menu_id")
            points = vote.get("points")

            # Check if the vote data is valid
            if (
                not menu_id
                or not points
                or not isinstance(points, int)
                or points < 1
                or points > 3
            ):
                return Response(
                    {"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Retrieve the menu instance with the given menu ID
            menu = Menu.objects.filter(id=menu_id).first()

            # Check if the menu exists
            if not menu:
                return Response(
                    {"error": "Menu Does not exist"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the employee has already voted for the current day and menu
            if Vote.objects.filter(
                menu=menu, employee_id=employee_id, voted_date=date.today()
            ).exists():
                return Response(
                    {"error": "You have already voted for this menu today"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Increment the votes count for the menu

            menu.points = F("votes") + points
            menu.save()

            # Create a vote record for the employee
            Vote.objects.create(menu=menu, employee_id=employee_id)

        return Response(
            {"message": "Votes recorded successfully"}, status=status.HTTP_200_OK
        )


class VoteResultsForCurrentDayAPIView(generics.GenericAPIView):
    """
    API view to retrieve vote results for the current day.
    """

    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieves vote results for the current day.
        """
        try:
            today = timezone.now().date()

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
                serializer = self.get_serializer(max_votes_menu)
                return Response(
                    {"menu": serializer.data, "total_votes": total_votes},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "No votes found for today.", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {
                    "msg": "An error occurred while retrieving vote results.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
