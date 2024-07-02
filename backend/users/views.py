from django.contrib.auth import get_user_model
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core import constants as const
from core.views import (create_follow_object, delete_follow_object,
                        get_follow_object, get_following_object_or_404,
                        get_followings_of_user)
from users.permissions import SubscriptionAccess
from users.serializers import (SetPasswordSerializer, SubscriptionSerializer,
                               UserAvatarSerializer, UserCreateSerializer,
                               UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(SubscriptionAccess,)
    )
    def subscriptions(self, request):
        follower = request.user
        followings = get_followings_of_user(follower)
        page = self.paginate_queryset(followings)
        if page is not None:
            serializer = SubscriptionSerializer(page,
                                                many=True,
                                                context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(followings,
                                            many=True,
                                            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(SubscriptionAccess,)
    )
    def subscribe(self, request, pk=None):
        follower = request.user
        following = get_following_object_or_404(request, pk)
        if request.method == 'POST':
            if follower == following:
                return Response(
                    {'error': const.USER_FOLLOW_THEMSELVES_ERROR_MESSAGE},
                    status=status.HTTP_400_BAD_REQUEST)
            follow = get_follow_object(follower, following)
            if follow.exists():
                return Response(
                    {'error': const.SUBSCRIBE_ERROR_MESSAGE},
                    status=status.HTTP_400_BAD_REQUEST)
            create_follow_object(follower, following)
            serializer = SubscriptionSerializer(
                following, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = get_follow_object(follower, following)
            if follow.exists():
                delete_follow_object(follow)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': const.SUBSCRIBE_DELETE_ERROR_MESSAGE},
                status=status.HTTP_400_BAD_REQUEST)


class SetPasswordAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            request.user.set_password(
                serializer.validated_data['new_password'])
            request.user.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # User.objects.all()
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAvatarAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = UserAvatarSerializer(user,
                                          data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
