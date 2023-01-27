from django.contrib import admin
from .models import Category,Subcategory,Product,ProductImage
# Register your models here.


admin.site.register(Category)
admin.site.register(Subcategory)


class ImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = (
        ImageInline,
    )

admin.site.register(Product,ProductAdmin)