from django.shortcuts import render
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet,ViewSet
from .models import Product,Category,Subcategory
from .serializers import CategorySerializer,SubCategoryListSerializer,SubCategoryDetailSerializer,ProductListSerializer,ProductDetailSerializer
# Create your views here.


class CategoryViewset(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'



class SubCategoryViewset(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = Subcategory.objects.all()
    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubCategoryDetailSerializer
        if self.action == 'list':
            return SubCategoryListSerializer

class ProductViewset(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer