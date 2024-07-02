from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import (SetPasswordAPIView, UserAvatarAPIView,
                         UserProfileAPIView, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('users/set_password/',
         SetPasswordAPIView.as_view(), name='set_password'),
    path('users/me/avatar/', UserAvatarAPIView.as_view(), name='user_avatar'),
    path('users/me/', UserProfileAPIView.as_view(), name='user_profile'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
