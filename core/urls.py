from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("movies/", views.MovieListView.as_view(), name="list"),
]
