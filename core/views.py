from . import models, forms
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class MovieListView(generic.ListView):
    model = models.Movie
    paginate_by = 12


class MovieDetailView(generic.DetailView):
    queryset = models.Movie.objects.all_with_related_persons_and_score()

    def get_context_data(self, **kwargs):
        ctx = super(MovieDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx["image_form"] = forms.MovieImageForm()

            vote = models.Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user,
            )

            if vote.id:
                vote_form_url = reverse("core:update_vote", kwargs={
                    "movie_id": vote.movie.id,
                    "pk": vote.id
                })
            else:
                vote_form_url = reverse("core:create_vote", kwargs={
                    "movie_id": self.object.id
                })

            vote_form = forms.VoteForm(instance=vote)
            ctx["vote_form"] = vote_form
            ctx["vote_form_url"] = vote_form_url

        return ctx


class PersonDetailView(generic.DetailView):
    queryset = models.Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, generic.CreateView):
    form_class = forms.VoteForm

    def get_initial(self):
        initial = super(CreateVote, self).get_initial()
        initial["user"] = self.request.user.id
        initial["movie"] = self.kwargs["movie_id"]

        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse("core:detail", args=[movie_id])

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["object"].id
        movie_detail_url = reverse("core:detail", args=[movie_id])

        return redirect(movie_detail_url)


class UpdateVote(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.VoteForm
    queryset = models.Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super(UpdateVote, self).get_object(queryset=queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied("Can't change another user's vote")
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse("core:detail", args=[movie_id])

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["object"].id
        movie_detail_url = reverse("core:detail", args=[movie_id])
        return redirect(movie_detail_url)


class MovieImageUploadView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.MovieImageForm

    def get_initial(self):
        initial = super(MovieImageUploadView, self).get_initial()
        initial["user"] = self.request.user.id
        initial["movie"] = self.kwargs.get("movie_id")

        return initial

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs.get("movie_id")
        movie_detail_url = reverse('core:detail', args=[movie_id])

        return movie_detail_url

    def get_success_url(self):
        movie_id = self.kwargs.get("movie_id")
        movie_detail_url = reverse("core:detail", args=[movie_id])

        return movie_detail_url
