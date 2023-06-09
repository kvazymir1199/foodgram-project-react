from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from djoser.serializers import UserSerializer
from .models import Subscription
from .pagination import CustomPageNumberPagination
from .serializers import SubscriptionSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    @action(
        detail=False,
        methods=('get',),
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        user = self.request.user
        authors = user.subscribes.all().values_list('author_id')
        queryset = User.objects.filter(pk__in=authors)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        user = self.request.user

        author = get_object_or_404(User, pk=id)
        if self.request.method == 'POST':

            if user == author:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(
                user=user,
                author=author
            ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            Subscription.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Subscription.objects.filter(
            user=user,
            author=author
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        subscription = get_object_or_404(
            Subscription,
            user=user,
            author=author
        )
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
