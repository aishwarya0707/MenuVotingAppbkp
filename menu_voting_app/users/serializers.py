from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Employee


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration and representation.
    Handles the serialization and deserialization of user data.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create and return a new User instance using the validated data.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Handles validation of user credentials for login.
    """

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate the user credentials and return the user if valid.
        """
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    Used to validate the data provided for logout (though not directly used here).
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    Handles serialization and deserialization of employee data.
    """

    user = UserSerializer()

    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "user",
            "job_title",
            "date_of_joining",
            "department",
        ]
