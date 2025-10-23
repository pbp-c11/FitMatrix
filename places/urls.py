from django.urls import path

from .views import place_detail, place_list

app_name = "places"

urlpatterns = [
    path("", place_list, name="list"),
    path("<slug:slug>/", place_detail, name="detail"),
]
