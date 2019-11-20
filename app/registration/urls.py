from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegistrationView.as_view(), name="user-register"),
    path('validation/', views.RegistrationValidationView.as_view(), name="user-register-validate"),
]
