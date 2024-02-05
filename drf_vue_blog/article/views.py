from django.shortcuts import render
from .models import Article, Category, Tag, Avatar
from .serializers import (ArticleListSerializer, ArticleDetailSerializer, CategorySerializer, ArticleCategoryDetailSerializer,
                          CategoryDetailSerializer, TagSerializer, AvatarSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .permissions import IsAdminUserOrReadOnly
from rest_framework import filters
from rest_framework import viewsets


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        else:
            return ArticleDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]

