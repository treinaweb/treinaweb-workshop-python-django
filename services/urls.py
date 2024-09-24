from django.urls import path

from .views import list

app_name = "services"
urlpatterns = [
    path("", list, name="list"),
]
