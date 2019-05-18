from . import models
from django.views import generic


class MovieListView(generic.ListView):
    model = models.Movie
    paginate_by = 12


class MovieDetailView(generic.DetailView):
    model = models.Movie
