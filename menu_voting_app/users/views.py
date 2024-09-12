from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee
from rest_framework.exceptions import ValidationError
from .serializers import (
    LoginSerializer,
    UserSerializer,
    EmployeeSerializer,
    LogoutSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    Handles user registration via POST requests.
    """

    # Define the serializer class used for user registration
    serializer_class = UserSerializer

    def post(self, request):
        # Initialize the serializer with request data
        serializer = UserSerializer(data=request.data)
        try:
            # Validate and save the new user data
            if serializer.is_valid():
                serializer.save()  # Save the new user to the database
                return Response(
                    {"message": "User registered successfully"},
                    status=status.HTTP_201_CREATED,
                )
            # Return validation errors if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any unexpected errors
            return Response(
                {"message": "An error occurred during registration.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(generics.CreateAPIView):
    """
    Handles user login via POST requests.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.validated_data
                auth_login(request, user)
                return Response(
                    {"success": "Login successful."}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle any unexpected errors
            return Response(
                {"message": "An error occurred during login.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(generics.CreateAPIView):
    """
    Handles user logout via POST requests.
    """

    # Define the serializer class used for logout
    serializer_class = LogoutSerializer

    def post(self, request):
        # Initialize the serializer with request data
        serializer = LogoutSerializer(data=request.data)
        try:
            # Validate the serializer
            if serializer.is_valid():
                logout(request)  # Log the user out
                return Response(
                    {"message": "Successfully logged out."}, status=status.HTTP_200_OK
                )
            # Return validation errors if the data is invalid
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle any unexpected errors
            return Response(
                {"message": "An error occurred during logout.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreateEmployeeAPIView(generics.CreateAPIView):
    """
    Handles the creation of employee records via POST requests.
    """

    # Define the serializer class used for employee creation
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        # Retrieve data from the request
        data = self.request.data
        try:
            # Extract employee details
            email = data.get("user.email")
            username = data.get("user.username")
            employee_id = data.get("employee_id")

            # Check if an employee with the same ID already exists
            if Employee.objects.filter(employee_id=employee_id).exists():
                raise ValidationError(f"Employee with ID {employee_id} already exists.")

            # Create or get user profile
            user_profile, created = User.objects.get_or_create(
                email=email, username=username
            )

            # Save the employee record
            serializer.save(user=user_profile)
        except Exception as e:
            # Handle any unexpected errors during employee creation
            raise ValidationError(f"Error during employee creation: {str(e)}")

    def post(self, request, *args, **kwargs):
        # Initialize the serializer with request data
        serializer = self.get_serializer(data=request.data)
        try:
            # Validate the serializer
            if serializer.is_valid():
                self.perform_create(serializer)  # Perform the creation process
                headers = self.get_success_headers(serializer.data)
                return Response(
                    {
                        "msg": "Employee successfully created.",
                        "data": serializer.data,
                        "success": True,
                    },
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            # Return validation errors if the data is invalid
            return Response(
                {
                    "msg": "Validation failed.",
                    "errors": serializer.errors,
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            # Handle validation errors specifically
            return Response(
                {"msg": "Validation error occurred.", "errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle any unexpected errors during employee creation
            return Response(
                {"msg": "An error occurred during employee creation.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
