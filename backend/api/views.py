from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import AuthorOrAdminOrReadOnlyAccess
from api.serializers import (IngredientSerializer,
                             RecipeCreateUpdateSerializer, RecipeSerializer,
                             TagSerializer)
from core import constants as const
from core.services.recipes_services import add_or_delete_recipe_in_list
from core.views import (download_shopping_cart_main, get_recipe_or_404,
                        get_short_link)
from recipes.models import FavoriteList, Ingredient, Recipe, ShoppingCart, Tag


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
    permission_classes = (AuthorOrAdminOrReadOnlyAccess,)

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
        return add_or_delete_recipe_in_list(
            self=self,
            request=request,
            pk=pk,
            intermediate_model=FavoriteList.objects
        )

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        return add_or_delete_recipe_in_list(
            self=self,
            request=request,
            pk=pk,
            intermediate_model=ShoppingCart.objects
        )

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        return download_shopping_cart_main(request)

    @action(methods=['get'], detail=True,
            url_path='get-link', url_name='get-link')
    def get_link(self, request, pk=None):
        get_recipe_or_404(pk)
        if request.method == 'GET':
            short_link = get_short_link(request, pk)
            return (Response(
                {'short-link': short_link},
                status=status.HTTP_200_OK))
        return Response(
            {'error': const.RECIPE_GET_LINK_ERROR_MESSAGE},
            status=status.HTTP_400_BAD_REQUEST)
