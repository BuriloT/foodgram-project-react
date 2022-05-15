from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            Shopping_Cart, Subscribe, Tag, User)

admin.site.unregister(User)
admin.site.empty_value_display = '--Пусто--'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name',
        'username', 'email', 'is_staff'
    )
    list_filter = ('username', 'email')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('slug',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name', 'image', 'text',
        'cooking_time', 'favorite_count'
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)

    def favorite_count(self, obj):
        return obj.favorite_recipe.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


@admin.register(Subscribe)
class SubscirbeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'user')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(Shopping_Cart)
class Shopping_CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
