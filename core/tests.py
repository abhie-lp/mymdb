from . import models
from . import views

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

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
