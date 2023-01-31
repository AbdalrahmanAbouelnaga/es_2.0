from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.


class ItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    model= Order
    inlines=[
        ItemInline,
    ]

admin.site.register(Order,OrderAdmin)