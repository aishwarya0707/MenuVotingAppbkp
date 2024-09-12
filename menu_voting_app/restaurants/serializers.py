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
        fields = [
            "id",
            "restaurant",
            "items",
            "date",
        ]  # Specifies which fields to include in the serialization.


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.
    """

    class Meta:
        model = Vote  # Specifies the model this serializer is associated with.
        fields = [
            "menu",
            "employee",
            "points",
            "voted_date",
        ]  # Specifies which fields to include in the serialization.


class VoteRequestSerializer(serializers.Serializer):
    """
    Serializer for handling vote requests, including validation for multiple menu votes.
    """

    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )  # Validate employee ID against Employee model.
    voted_date = serializers.DateField()  # Validate that voted_date is a valid date.
    menu_1 = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all()
    )  # Validate that menu_1 is a valid Menu instance.
    menu_2 = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all()
    )  # Validate that menu_2 is a valid Menu instance.
    menu_3 = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all()
    )  # Validate that menu_3 is a valid Menu instance.

    def validate(self, data):
        """
        Custom validation for ensuring that all menu choices are unique.
        """
        menu_1, menu_2, menu_3 = data["menu_1"], data["menu_2"], data["menu_3"]

        # Ensure all menu choices are unique
        if len({menu_1, menu_2, menu_3}) != 3:
            raise serializers.ValidationError(
                "Menus must be unique."
            )  # Raise an error if duplicate menus are found.

        return data
