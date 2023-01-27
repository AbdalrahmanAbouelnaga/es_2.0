from rest_framework import serializers
from drf_writable_nested.mixins import NestedCreateMixin,NestedUpdateMixin
from .models import Category,Subcategory,Product,ProductImage
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer,NestedHyperlinkedRelatedField
from rest_framework.reverse import reverse



class ProductImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)
    def get_thumbnail(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail.url)
    class Meta:
        model = ProductImage
        fields = (
            'id',
            'image',
            'thumbnail',
        )
    
    def create(self, validated_data):
        img = ProductImage.objects.create(**validated_data)
        if img.thumbnail.url is None:
            img.make_thumbnail()
        img.save()
        return img



class ProductListSerializer(NestedCreateMixin,NestedUpdateMixin,serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'subcategory_slug': 'subcategory_slug',
        'category_slug':'subcategory_category__slug',
    }
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('product-detail', kwargs={'category_slug': obj.subcategory.category.slug,
            'subcategory_slug': obj.subcategory.slug,
            'slug': obj.slug}))
    images = ProductImagesSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'url',
            'title',
            'slug',
            'price',
            'images'
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ProductDetailSerializer(NestedCreateMixin,NestedUpdateMixin,serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'subcategory_slug': 'subcategory_slug',
        'category_slug':'subcategory_category__slug',
    }
    images = ProductImagesSerializer(many=True)
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'price',
            'subcategory',
            'description',
            'images'
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }



class SubCategoryDetailSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'category_slug': 'category_slug'
    }
    products = ProductListSerializer(many=True)
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subcategory-detail', kwargs={'category_slug': obj.category.slug,
            'slug': obj.slug}))
    class Meta:
        model = Subcategory
        fields = (
            'url',
            'title',
            'products'
        )
        lookup_field = 'subcategory_slug'





class SubCategoryListSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'category_slug': 'category_slug'
    }
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subcategory-detail', kwargs={'category_slug': obj.category.slug,
            'slug': obj.slug}))
    class Meta:
        model = Subcategory
        fields = (
            'url',
            'title',
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

        

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subCategories = SubCategoryListSerializer(many=True)
    class Meta:
        model = Category
        fields = (
            'url',
            'title',
            'subCategories'
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }