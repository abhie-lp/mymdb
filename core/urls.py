from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("movie/<int:movie_id>/image/upload/", views.MovieImageUploadView.as_view(), name="image"),
    path("movie/<int:movie_id>/vote/<int:pk>/", views.UpdateVote.as_view(), name="update_vote"),
    path("movie/<int:movie_id>/vote", views.CreateVote.as_view(), name="create_vote"),
    path("person/<int:pk>/", views.PersonDetailView.as_view(), name="person"),
    path("movie/<int:pk>/", views.MovieDetailView.as_view(), name="detail"),
    path("movies/", views.MovieListView.as_view(), name="list"),
    path("top_movies/", views.TopMovieView.as_view(), name="top_movies")
]
