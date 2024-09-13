from django.db import models
from django.utils import timezone

from users.models import Employee


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    cuisine_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="menus", on_delete=models.CASCADE
    )
    date = models.DateField()
    items = models.TextField()
    votes = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        unique_together = ("restaurant", "date")

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    points = models.IntegerField(default=1)
    voted_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Vote by {self.employee.user.username} for {self.menu.restaurant.name} on {self.voted_date}"
