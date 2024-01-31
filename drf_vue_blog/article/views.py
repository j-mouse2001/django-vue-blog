from django.shortcuts import render
from .models import Article, Category, Tag
from .serializers import (ArticleListSerializers, ArticleDetailSerializers, CategorySerializer, ArticleCategoryDetailSerializer,
                          CategoryDetailSerializer, TagSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .permissions import IsAdminUserOrReadOnly
from rest_framework import filters
from rest_framework import viewsets


# Create your views here.
class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializers
    permission_classes = (IsAdminUserOrReadOnly,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializers
    permission_classes = (IsAdminUserOrReadOnly,)


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

