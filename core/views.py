from . import models
from django.views import generic


class MovieListView(generic.ListView):
    model = models.Movie
