from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee
from .serializers import (EmployeeSerializer, LoginSerializer,
                          LogoutSerializer, UserSerializer)


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


class CreateEmployeeAPIView(APIView):

    def post(self, request):
        data = request.data
        # Check if employee with the given ID already exists
        employee_id = data.get("employee_id")
        if employee_id and Employee.objects.filter(employee_id=employee_id).exists():
            error_message = f"Employee with ID {employee_id} already exists"
            return Response(
                {"msg": error_message, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        userDetails = data["user"]
        email = userDetails["email"]
        username = userDetails["username"]
        userData, created = User.objects.get_or_create(email=email, username=username)
        userData.save()

        try:
            # Create the employee
            employee = Employee.objects.create(
                employee_id=employee_id,
                user=userData,
                date_of_joining=data.get("date_of_joining"),
            )
        except Exception as e:
            error_message = f"Failed to create employee: {str(e)}"
            return Response(
                {"msg": error_message, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = EmployeeSerializer(employee)
        response_data = {
            "msg": "Employee successfully created.",
            "data": serializer.data,
            "success": True,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
