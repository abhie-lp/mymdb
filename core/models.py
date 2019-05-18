from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born = models.DateField(blank=True, null=True)
    died = models.DateField(blank=True, null=True)

    class Meta:
        ordering = "first_name", "last_name",

    def __str__(self):
        return self.first_name + " " + self.last_name


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

    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="directed",
        null=True,
        blank=True,
    )
    writers = models.ManyToManyField(
        Person,
        related_name="writing_credits",
        blank=True
    )
    actors = models.ManyToManyField(
        to=Person,
        through="Role",
        related_name="acting_credits",
        blank=True
    )

    class Meta:
        ordering = "-year", "title",

    def __str__(self):
        return self.title


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=60)

    class Meta:
        unique_together = "movie", "person", "name",

    def __str__(self):
        return self.name
