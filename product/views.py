from django.shortcuts import render
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet,ViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,Category,Subcategory
from .serializers import CategorySerializer,SubCategoryListSerializer,SubCategoryDetailSerializer,ProductListSerializer,ProductDetailSerializer
# Create your views here.

@api_view(['GET'])
def latestProducts(request):
    queryset = Product.objects.all().order_by('-created')
    serializer = ProductListSerializer(queryset,many=True,context={'request': request})
    return Response(serializer.data,status=200)


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