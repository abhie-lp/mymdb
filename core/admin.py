from . import models
from django.contrib import admin


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = "id", "title", "year", "runtime", "get_rating_display",
    list_display_links = "title",
    list_filter = "year", "runtime",
    search_fields = "title", "year",


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = "id", "first_name", "last_name", "born", "died",
    list_display_links = "first_name", "last_name",
    search_fields = "first_name", "last_name",


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = "id", "person", "movie", "name",
    list_display_links = "person", "movie", "name",
    search_fields = "name",


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = "id", "movie", "user", "value",
    list_display_links = "movie",
