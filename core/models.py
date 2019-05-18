from django.db import models


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, "NR - Not Rated"),
        (RATED_G, "G - General Audience"),
        (RATED_PG, "PG - Parental Guidance"),
        (RATED_R, "R - Restricted"),
    )

    title = models.CharField(max_length=155)
    plot = models.TextField()
    year = models.PositiveSmallIntegerField()
    rating = models.PositiveSmallIntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveSmallIntegerField()
    website = models.URLField(blank=True)

    class Meta:
        ordering = "-year", "title",

    def __str__(self):
        return self.title
