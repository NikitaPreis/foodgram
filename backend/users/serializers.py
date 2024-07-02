import base64

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from rest_framework import serializers

from core import constants as const
from core.views import get_is_subscribed_user_field
from recipes.models import Follow, Recipe
from users.models import FoodgramUser

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=const.FOODGRAM_EMAIL_MAXLENGTH,)
    is_subscribed = serializers.SerializerMethodField()

    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'avatar')
        read_only_fields = ('id', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        return get_is_subscribed_user_field(self, obj)


class UserDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = FoodgramUser
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed', 'avatar')
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        return get_is_subscribed_user_field(self, obj)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=const.FOODGRAM_EMAIL_MAXLENGTH,)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipeShortReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = Base64ImageField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count', 'avatar')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return get_is_subscribed_user_field(self, obj)

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')
        author = self.context['request'].user
        if recipes_limit is not None:
            queryset = Recipe.objects.filter(
                author__following__user=author)[:int(recipes_limit)]
            serializer = RecipeShortReadSerializer(queryset, many=True)
            return serializer.data
        queryset = Recipe.objects.filter(author__following__user=author)
        serializer = RecipeShortReadSerializer(queryset, many=True)
        return serializer.data


class FollowSerializer(serializers.ModelSerializer):
    following = SubscriptionSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'following')


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        required=True
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )

    def validate_current_password(self, value):
        request = self.context['request']
        user = request.user
        if user.check_password(value):
            return value
        raise serializers.ValidationError(
            const.PASSWORD_VALIDATION_ERROR_MESSAGE)

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserProfileSeriliazer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(default=False)
    avatar = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed')
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'avatar')


class UserAvatarSerializer(serializers.Serializer):
    avatar = Base64ImageField(allow_null=True, required=True)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
