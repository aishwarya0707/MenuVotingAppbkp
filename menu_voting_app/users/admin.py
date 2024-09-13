from django.contrib import admin

from .models import Employee


# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "user", "job_title", "date_of_joining", "department")


admin.site.register(Employee)
