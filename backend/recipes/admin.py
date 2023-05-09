from django.contrib import admin

from backend.settings import VALUE_DISPLAY

from .models import (Favorites, Ingredient, IngredientQuantity, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites',
                    'amount_tags', 'amount_ingredients',)
    list_filter = ('author', 'name', 'tags',)
    search_fields = ('name',)
    empty_value_display = VALUE_DISPLAY

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    def amount_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def amount_ingredients(obj):
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredients', 'recipe', 'quantity',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    empty_value_display = VALUE_DISPLAY


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    empty_value_display = VALUE_DISPLAY
