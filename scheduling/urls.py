from django.urls import path

from .views import upcoming_sessions

app_name = "scheduling"

urlpatterns = [
    path("", upcoming_sessions, name="sessions"),
]
