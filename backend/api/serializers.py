from django.contrib.auth import get_user_model
from rest_framework import serializers

from core import constants as const
from core.views import (create_recipe_ingredient, delete_recipe_ingredient,
                        exclude_duplicate, get_is_favorited_recipe_field,
                        get_is_in_shopping_cart_recipe_field,
                        get_recipe_ingredient)
from recipes.models import (FavoriteList, Ingredient, Recipe, RecipeIngredient,
                            Tag)
from users.serializers import Base64ImageField, UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientAndAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all(),
    )
    name = serializers.StringRelatedField(
        source='ingredient.name',
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit',
                  'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = UserSerializer(
        read_only=True
    )

    ingredients = IngredientAndAmountSerializer(read_only=True,
                                                many=True,
                                                source='recipe_ingredient')

    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(default=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return get_is_favorited_recipe_field(self, obj)

    def get_is_in_shopping_cart(self, obj):
        return get_is_in_shopping_cart_recipe_field(self, obj)


class IngredientAndAmountCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(
        min_value=const.AMOUNT_OF_INGREDIENT_MIN_VALUE)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        allow_empty=False,
    )
    author = UserSerializer(
        read_only=True
    )

    ingredients = IngredientAndAmountCreateSerializer(
        many=True,
        source='recipe_ingredient',
        allow_empty=False,
    )

    image = Base64ImageField(required=True)
    name = serializers.CharField(allow_blank=False,
                                 max_length=const.NAME_MAX_LENGHT)

    class Meta:
        model = Recipe
        fields = ('tags', 'author',
                  'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def validate_tags(self, data):
        exclude_duplicate(data,
                          const.DUPLICATE_TAGS_ERROR_MESSAGE)
        return data

    def validate_ingredients(self, data):
        exclude_duplicate(data,
                          const.DUPLICATE_INGREDIENTS_ERROR_MESSAGE)
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipes_ingredients = validated_data.pop('recipe_ingredient')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for recipe_ingredient in recipes_ingredients:
            create_recipe_ingredient(
                recipe=recipe,
                ingredient=recipe_ingredient['id'],
                amount=recipe_ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        if validated_data.get('image'):
            instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.text = validated_data.get('text', instance.text)

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        if 'recipe_ingredient' in validated_data:
            recipes_ingredients = validated_data.pop('recipe_ingredient')
            recipe_ingredient_filter = get_recipe_ingredient(instance)
            delete_recipe_ingredient(recipe_ingredient_filter)
            for recipe_ingredient in recipes_ingredients:
                create_recipe_ingredient(
                    recipe=instance,
                    ingredient=recipe_ingredient['id'],
                    amount=recipe_ingredient['amount']
                )
        instance.save()
        return instance

    def to_representation(self, instance):
        return (RecipeSerializer(
            instance, context={'request': self.context.get('request')}).data
        )


class FavoriteListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='recipe.id',
    )
    name = serializers.StringRelatedField(
        read_only=True,
        source='recipe.name'
    )
    image = serializers.StringRelatedField(
        read_only=True,
        source='recipe.image'
    )
    cooking_time = serializers.StringRelatedField(
        read_only=True,
        source='recipe.cooking_time'
    )

    class Meta:
        model = FavoriteList
        fields = ('id', 'name', 'image', 'cooking_time')
