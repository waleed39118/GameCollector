from django.contrib import admin
from .models import Game, Category

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'genre', 'rating', 'release_date', 'category')
    list_filter = ('platform', 'genre', 'rating', 'category')
    search_fields = ('name', 'platform', 'genre')
    ordering = ('-release_date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)