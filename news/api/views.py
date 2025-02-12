from rest_framework import generics, viewsets
from rest_framework.viewsets import ModelViewSet


from news.api.serializers import NewsSerializer, CategorySerializer
from news.models import News, Category


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class NewsListView(generics.ListAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#
#
# class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#
