from django.urls import path

from .views import place_list

app_name = "places"

urlpatterns = [
    path("", place_list, name="list"),
]
