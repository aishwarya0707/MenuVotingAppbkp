from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration and representation.
    Handles the serialization and deserialization of user data.
    """

    password = serializers.CharField(
        write_only=True
    )  # Password field is write-only to ensure security

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]  # Fields included in the serialized data
        extra_kwargs = {
            "password": {
                "write_only": True
            }  # Ensure password is not readable from serialized data
        }

    def create(self, validated_data):
        """
        Create and return a new User instance using the validated data.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data[
                "password"
            ],  # Use create_user to handle password hashing
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Handles validation of user credentials for login.
    """

    username = serializers.CharField()  # Username field
    password = serializers.CharField()  # Password field

    def validate(self, data):
        """
        Validate the user credentials and return the user if valid.
        """
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:
            return user  # Return the authenticated user
        raise serializers.ValidationError(
            "Invalid credentials"
        )  # Raise an error if authentication fails


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    Used to validate the data provided for logout (though not directly used here).
    """

    username = serializers.CharField()  # Username field for identifying the user
    password = serializers.CharField(write_only=True)  # Password field is write-only


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    Handles serialization and deserialization of employee data.
    """

    user = UserSerializer()  # Nested serializer for user data

    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "user",
            "job_title",
            "date_of_joining",
            "department",
        ]  # Fields included in the serialized data
