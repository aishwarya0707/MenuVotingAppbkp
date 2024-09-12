from django.urls import path

# Importing views that handle the respective API endpoints
from .views import RegisterView, LoginView, LogoutView, CreateEmployeeAPIView

# URL patterns for the application's API endpoints
urlpatterns = [
    # Endpoint for user registration
    # Maps to the RegisterView which handles user registration requests
    path('register/', RegisterView.as_view(), name='register'),

    # Endpoint for user login
    # Maps to the LoginView which handles user login requests
    path('login/', LoginView.as_view(), name='login'),

    # Endpoint for user logout
    # Maps to the LogoutView which handles user logout requests
    path('logout/', LogoutView.as_view(), name='logout'),

    # Endpoint for creating a new employee
    # Maps to the CreateEmployeeAPIView which handles employee creation requests
    path('create-employee/', CreateEmployeeAPIView.as_view(), name='employee_create'),
]
