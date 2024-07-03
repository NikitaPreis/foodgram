import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_short_url.views import get_surl

from foodgram.settings import BASE_DIR
from recipes.models import (FavoriteList, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart)

User = get_user_model()


def get_followings_of_user(follower):
    return User.objects.filter(following__user=follower)


def get_following_object_or_404(request, following_id=None):
    return get_object_or_404(User, id=following_id)


def get_follow_object(follower, following):
    return Follow.objects.filter(user=follower, following=following)


def create_follow_object(follower, following):
    return Follow.objects.create(user=follower, following=following)


def delete_follow_object(follow):
    return follow.delete()


def check_follow_exist(follow):
    return follow.exists()


def get_is_subscribed_user_field(self, obj):
    user = self.context['request'].user
    if not user.is_authenticated:
        return False
    follow = get_follow_object(user, obj)
    if follow.exists():
        return True
    return False


def get_recipe_or_404(id):
    return get_object_or_404(Recipe, id=id)


def get_recipe_in_favorite_list(user, recipe):
    return FavoriteList.objects.filter(author=user, recipe=recipe)


def get_recipes_from_favorite_list(recipes, user):
    return recipes.filter(favorite_recipe__author=user)


def add_recipe_to_favorite_list(user, recipe):
    return FavoriteList.objects.create(author=user, recipe=recipe)


def delete_recipe_from_favorite_list(favorite_recipe):
    return favorite_recipe.delete()


def get_recipe_in_shopping_cart(user, recipe):
    return ShoppingCart.objects.filter(user=user, recipe=recipe)


def get_recipes_from_shopping_cart(recipes, user):
    return recipes.filter(shopping_recipe__user=user)


def add_recipe_to_shopping_cart(user, recipe):
    return ShoppingCart.objects.create(user=user, recipe=recipe)


def delete_recipe_from_shopping_cart(recipe_in_shopping_cart):
    return recipe_in_shopping_cart.delete()


def get_is_favorited_recipe_field(self, obj):
    user = self.context['request'].user
    if not user.is_authenticated:
        return False
    recipe_in_favorite_list = get_recipe_in_favorite_list(user, obj)
    if recipe_in_favorite_list.exists():
        return True
    return False


def get_is_in_shopping_cart_recipe_field(self, obj):
    user = self.context['request'].user
    if not user.is_authenticated:
        return False
    recipe_in_shopping_cart = get_recipe_in_shopping_cart(user, obj)
    if recipe_in_shopping_cart.exists():
        return True
    return False


def get_recipe_ingredient(recipe):
    return RecipeIngredient.objects.filter(recipe=recipe)


def create_recipe_ingredient(ingredient, recipe, amount):
    return (RecipeIngredient.objects.create(
        ingredient=ingredient,
        recipe=recipe,
        amount=amount)
    )


def delete_recipe_ingredient(recipe_ingredient):
    return recipe_ingredient.delete()


def get_ingredients_name_starstwith_sample(ingredients, sample):
    return ingredients.filter(name__startswith=sample)


def get_ingredients_from_shopping_cart(user):
    ingredients_from_shopping_list = Ingredient.objects.filter(
        recipe__shopping_recipe__user=user
    ).annotate(Sum('recipe_ingredient__amount'))
    return ingredients_from_shopping_list


def make_shopping_cart_download_file_name(user):
    file_name_request_user_username = user.username
    txt_extension = '.txt'
    return file_name_request_user_username + txt_extension


def get_shopping_cart_path_to_file(file_name):
    rel_path = f'static_dev/files/{file_name}'
    return os.path.join(BASE_DIR, rel_path)


def create_shopping_cart_file_txt(path_to_file,
                                  ingredients_from_shopping_list):
    with open(f'{path_to_file}', "w+") as new_file:
        for ingredient in ingredients_from_shopping_list:
            string_pattern = (f'• {ingredient.name} '
                              f'({ingredient.measurement_unit}) — '
                              f'{ingredient.recipe_ingredient__amount__sum}\n')

            new_file.write(string_pattern)


def open_shopping_cart_file_txt_binary_mode(path_to_file):
    with open(f'{path_to_file}', "rb") as new_file:
        return HttpResponse(new_file, content_type='application/txt')


def download_shopping_cart_main(request):
    ingredients_from_shopping_list = get_ingredients_from_shopping_cart(
        request.user)

    file_name = make_shopping_cart_download_file_name(request.user)

    path_to_file = get_shopping_cart_path_to_file(file_name)
    create_shopping_cart_file_txt(path_to_file,
                                  ingredients_from_shopping_list)
    return open_shopping_cart_file_txt_binary_mode(path_to_file)


def exclude_duplicate(collection, error_message):
    if isinstance(collection, list):
        collection_set = set()
        for element in collection:
            print(element)
            collection_set.add(str(element))
    else:
        collection_set = set()
        for element in collection:
            collection_set.add(element.get('id'))
    if len(collection_set) != len(collection):
        raise ValidationError(error_message)


def get_short_link(request):
    absolute_url = request.build_absolute_uri()[0: -9]
    surl = get_surl(absolute_url)
    return request.META['HTTP_HOST'] + surl
