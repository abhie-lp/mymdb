from . import models
from django.contrib import admin


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = "id", "title", "year", "runtime", "get_rating_display",
    list_display_links = "title",
    list_filter = "year", "runtime",
    search_fields = "title", "year",
