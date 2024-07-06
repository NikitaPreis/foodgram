from django.http import Http404
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet, NumberFilter)

from core.views import (get_recipes_from_favorite_list,
                        get_recipes_from_shopping_cart)
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    author = NumberFilter(field_name='author__id',
                          lookup_expr='icontains')
    tags = CharFilter(field_name='tags__slug',
                      method='get_tags',
                      distinct=True)
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart',
                  'author', 'tags')

    def get_tags(self, queryset, name, value,):
        tags_slug_list = self.request.GET.getlist('tags')
        for slug in tags_slug_list:
            queryset = queryset.filter(tags__slug=slug)
        return queryset

    def get_is_favorited(self, queryset, name, value):
        if not self.request.user.is_authenticated:
            raise Http404
        if value == 1:
            queryset = get_recipes_from_favorite_list(recipes=queryset,
                                                      user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not self.request.user.is_authenticated:
            raise Http404
        if value == 1:
            queryset = get_recipes_from_shopping_cart(recipes=queryset,
                                                      user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    name = CharFilter(method='get_name')

    class Meta:
        fields = ('name',)

    def get_name(self, queryset, name, value):
        return queryset.filter(name__istartswith=value)
