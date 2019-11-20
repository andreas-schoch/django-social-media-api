from django.urls import path
from . import views

app_name = 'me'


urlpatterns = [
    path('', views.GetOrUpdateUserData.as_view(), name="get-or-update-user-data"),
]
