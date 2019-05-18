from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("movie/<int:pk>/", views.MovieDetailView.as_view(), name="detail"),
    path("movies/", views.MovieListView.as_view(), name="list"),
]
