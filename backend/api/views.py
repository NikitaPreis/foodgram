from django_filters.rest_framework import DjangoFilterBackend
from django_short_url.views import get_surl
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import RecipePermission
from api.serializers import (IngredientSerializer,
                             RecipeCreateUpdateSerializer, RecipeSerializer,
                             TagSerializer)
from core import constants as const
from core.views import (add_recipe_to_favorite_list,
                        add_recipe_to_shopping_cart,
                        delete_recipe_from_favorite_list,
                        delete_recipe_from_shopping_cart,
                        download_shopping_cart_main,
                        get_recipe_in_favorite_list,
                        get_recipe_in_shopping_cart, get_recipe_or_404)
from recipes.models import Ingredient, Recipe, Tag
from users.serializers import RecipeShortReadSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = IngredientFilter
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (RecipePermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_recipe_or_404(pk)
        favorite_recipe = get_recipe_in_favorite_list(user, recipe)
        if request.method == 'POST':
            if favorite_recipe.exists():
                return Response(
                    {'error': const.RECIPE_ALREADY_EXIST_IN_FAVORITE_LIST},
                    status=status.HTTP_400_BAD_REQUEST)
            add_recipe_to_favorite_list(user, recipe)
            serializer = RecipeShortReadSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if favorite_recipe.exists():
                delete_recipe_from_favorite_list(favorite_recipe)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': const.RECIPE_DOSNT_EXIST_IN_FAVORITE_LIST},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        return download_shopping_cart_main(request)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_recipe_or_404(pk)
        recipe_in_shopping_cart = get_recipe_in_shopping_cart(user, recipe)
        if request.method == 'POST':
            if recipe_in_shopping_cart.exists():
                return Response(
                    {'error': const.RECIPE_ALREADY_EXIST_IN_SHOPPING_CART},
                    status=status.HTTP_400_BAD_REQUEST)
            add_recipe_to_shopping_cart(user, recipe)
            serializer = RecipeShortReadSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if recipe_in_shopping_cart.exists():
                delete_recipe_from_shopping_cart(recipe_in_shopping_cart)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': const.RECIPE_DOSNT_EXIST_IN_SHOPPING_CART},
                status=status.HTTP_400_BAD_REQUEST)

    # Снйчас не возвращает домен
    @action(methods=['get'], detail=True,
            url_path='get-link', url_name='get-link')
    def get_link(self, request, pk=None):
        get_recipe_or_404(pk)
        if request.method == 'GET':
            absolute_url = request.build_absolute_uri()[0: -9]
            # заменить на const в past строке
            surl = get_surl(absolute_url)
            # добавить домен в .env
            # short_link = os.getenv('DOMAIN') + surl
            # import os
            # from pathlib import Path
            # load_dotenv()
            return (Response(
                {'short-link': surl},  # short_link
                status=status.HTTP_200_OK))
        return Response(
            {'error': const.RECIPE_GET_LINK_ERROR_MESSAGE},
            status=status.HTTP_400_BAD_REQUEST)
