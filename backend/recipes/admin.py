from django.contrib import admin

from recipes.models import FavoriteList, Follow, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'text', 'cooking_time', 'author',
              'image')
    search_fields = ('name', 'author')
    list_filter = ('tags',)
    list_display = ('name', 'author', 'count_of_favorites')
    readonly_fields = ('count_of_favorites',)

    def count_of_favorites(self, obj):
        return FavoriteList.objects.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'measurement_unit')


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow)
admin.site.register(Ingredient, IngredientAdmin)
