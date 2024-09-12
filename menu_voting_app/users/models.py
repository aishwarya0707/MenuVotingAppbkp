from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    employee_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"
