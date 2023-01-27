from rest_framework_nested.routers import NestedDefaultRouter,DefaultRouter
from . import views
from django.urls import path,include

router = DefaultRouter()

router.register(r'categories',views.CategoryViewset,basename='category')

category_router = NestedDefaultRouter(router,r'categories',lookup='category')
category_router.register(r'subcategories',views.SubCategoryViewset,basename='subcategory')

subcategory_router = NestedDefaultRouter(category_router,r'subcategories',lookup='subcategory')
subcategory_router.register(r'products',views.ProductViewset,basename='product')


urlpatterns = [
    path(r'',include(router.urls)),
    path(r'',include(category_router.urls)),
    path(r'',include(subcategory_router.urls))
]