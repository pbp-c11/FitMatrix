from django.urls import path

<<<<<<< HEAD
from .views import place_detail, place_list, place_reviews_partial, place_review_create  # ⬅️ tambahkan ini
=======
from .views import place_detail, place_list
>>>>>>> origin/kanayradeeva010

app_name = "places"

urlpatterns = [
    path("", place_list, name="list"),
    path("<slug:slug>/", place_detail, name="detail"),
<<<<<<< HEAD
    path("<slug:slug>/reviews/", place_reviews_partial, name="reviews_partial"),
    path("<slug:slug>/reviews/new/", place_review_create, name="review_create"),
=======
>>>>>>> origin/kanayradeeva010
]
