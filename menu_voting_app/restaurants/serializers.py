from rest_framework import serializers

from users.models import Employee

from .models import Menu, Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model.
    """

    class Meta:
        model = Restaurant  # Specifies the model this serializer is associated with.
        fields = "__all__"  # Include all fields of the Restaurant model in the serialization.


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model.
    """

    class Meta:
        model = Menu  # Specifies the model this serializer is associated with.
        fields = ["id", "restaurant", "items", "date", "votes"]


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.
    """

    class Meta:
        model = Vote
        fields = ["menu", "employee", "points"]
