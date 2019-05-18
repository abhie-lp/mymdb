from . import models
from django.views import generic


class MovieListView(generic.ListView):
    model = models.Movie


class MovieDetailView(generic.DetailView):
    model = models.Movie
