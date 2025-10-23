from django.urls import path

from .views import place_detail, place_list, place_reviews_partial, place_review_create  # ⬅️ tambahkan ini

app_name = "places"

urlpatterns = [
    path("", place_list, name="list"),
    path("<slug:slug>/", place_detail, name="detail"),
    path("<slug:slug>/reviews/", place_reviews_partial, name="reviews_partial"),
    path("<slug:slug>/reviews/new/", place_review_create, name="review_create"),
]
