from django.contrib import admin
from .models import Product, Order, OrderItem, Table, MenuItem, MenuCategory


admin.site.register(Product)
admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(MenuCategory)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)

admin.site.register(Order, OrderAdmin)