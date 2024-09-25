from django.urls import path

from .views import list, detail

app_name = "services"
urlpatterns = [
    path("", list, name="list"),
    path("<int:pk>/", detail, name="detail"),
]
