from rest_framework import status
from rest_framework.response import Response

from core import constants as const
from core.views import get_recipe_or_404
from users.serializers import RecipeShortReadSerializer


def get_recipe_in_intermediate_model(intermediate_model, user, recipe):
    return intermediate_model.filter(user=user, recipe=recipe)


def add_recipe_to_intermediate_model(intermediate_model, user, recipe):
    return intermediate_model.create(user=user, recipe=recipe)


def delete_recipe_from_intermediate_model(recipe_in_intermediate_model):
    return recipe_in_intermediate_model.delete()


def add_or_delete_recipe_in_list(
        self, request, pk,
        intermediate_model):
    user = request.user
    recipe = get_recipe_or_404(pk)
    recipe_in_intermediate_model = get_recipe_in_intermediate_model(
        user=user,
        recipe=recipe,
        intermediate_model=intermediate_model
    )
    if request.method == 'POST':
        if recipe_in_intermediate_model.exists():
            return Response(
                {'error': const.RECIPE_ALREADY_EXIST_IN_LIST},
                status=status.HTTP_400_BAD_REQUEST)
        add_recipe_to_intermediate_model(
            user=user,
            recipe=recipe,
            intermediate_model=intermediate_model
        )
        serializer = RecipeShortReadSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        if recipe_in_intermediate_model.exists():
            delete_recipe_from_intermediate_model(
                recipe_in_intermediate_model=recipe_in_intermediate_model
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'error': const.RECIPE_DOSNT_EXIST_IN_LIST},
        status=status.HTTP_400_BAD_REQUEST)
