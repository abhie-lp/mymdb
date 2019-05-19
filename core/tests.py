from . import models
from . import views

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse
from django.contrib.auth.models import User

MOVIE_LIST_URL = reverse("core:list")


def movie_detail_url(movie_pk):
    """Generate detail url for a movoie"""

    return reverse("core:detail", args=[movie_pk])


class MovieListTestCase(TestCase):
    """Test the MovieList template"""

    ACTIVE_PAGINATION_HTML = """
    <li class="page-item active">
        <a href="{}?page={}" class="page-link">{}</a>
    </li>
    """

    def setUp(self):
        for n in range(15):
            models.Movie.objects.create(
                title="Title {}".format(n),
                year=1990 + n,
                runtime=120 + n,
            )

    def test_movie_list_page(self):
        """Test the status code and template used in movie list"""

        res = self.client.get(MOVIE_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "core/movie_list.html")

    def test_first_page(self):
        """Test the pagination"""

        req = RequestFactory().get(MOVIE_LIST_URL)
        res = views.MovieListView.as_view()(req)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context_data["is_paginated"])
        self.assertEqual(len(res.context_data["object_list"]), 12)
        self.assertInHTML(self.ACTIVE_PAGINATION_HTML.format(MOVIE_LIST_URL, 1, 1),
                          res.rendered_content)


class MovieDetailTest(TestCase):
    """Test the MovieDetail template"""

    def setUp(self):
        self.movie = models.Movie.objects.create(
            title="Movie 1",
            year=2019,
            runtime=123,
        )

    def test_movie_detail_page(self):
        res = self.client.get(movie_detail_url(self.movie.pk))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "core/movie_detail.html")
        self.assertEqual(res.context_data["object"].title, self.movie.title)

    def test_error_on_unknown_movie(self):
        """Test returns error on unknown URL"""

        res = self.client.get("/movie/9999999/")

        self.assertEqual(res.status_code, 404)


def vote_create_url(movie_id):

    return reverse("core:create_vote", args=[movie_id])


def vote_update_url(movie_id, vote_id):

    return reverse("core:update_vote", args=[movie_id, vote_id])


class MovieVoteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="django123",
        )

        self.movie = models.Movie.objects.create(
            title="Test Movie",
            year=2019,
            runtime=140,
        )

    def test_no_vote_without_login(self):

        res = self.client.get(movie_detail_url(self.movie.pk))

        self.assertFalse(res.context_data.get("vote_form"))
        self.assertFalse(res.context_data.get("vote_form_url"))

    def test_vote_redirects_without_login(self):

        res = self.client.post(vote_create_url(self.movie.id),
                               {"name": "value", "value": 1})

        redirect_url = reverse("user:login") + "?next=" + vote_create_url(self.movie.id)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, redirect_url)

    def test_vote_context_on_login(self):

        self.client.force_login(self.user)
        res = self.client.get(movie_detail_url(self.movie.id))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context_data.get("vote_form"))
        self.assertTrue(res.context_data.get("vote_form_url"))

    def test_vote_success(self):

        self.client.force_login(self.user)

        self.assertEqual(self.movie.vote_set.all().count(), 0)

        res = self.client.post(vote_create_url(self.movie.id),
                               {"name": "value", "value": 1})

        self.movie.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, movie_detail_url(self.movie.id))
        self.assertEqual(self.movie.vote_set.all().count(), 1)
        self.assertEqual(self.movie.vote_set.all().first().value, 1)

    def test_update_vote_success(self):

        self.client.force_login(self.user)

        vote = models.Vote.objects.create(
            user=self.user,
            movie=self.movie,
            value=-1
        )

        self.movie.refresh_from_db()

        self.assertEqual(len(self.movie.vote_set.all()), 1)
        self.assertEqual(self.movie.vote_set.all().first().value, -1)

        res = self.client.post(vote_update_url(self.movie.pk, vote.pk),
                               {"name": "value", "value": -1})

        self.movie.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, movie_detail_url(self.movie.pk))
        self.assertEqual(self.movie.vote_set.all().first().value, -1)

    def test_fail_to_update_others_vote(self):

        self.client.force_login(self.user)

        user2 = User.objects.create_user(username="test2", password="django123")
        vote = models.Vote.objects.create(user=user2, movie=self.movie, value=1)

        res = self.client.post(vote_update_url(self.movie.id, vote.id),
                               {"name": "value", "value": -1})

        vote.refresh_from_db()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(vote.value, 1)
