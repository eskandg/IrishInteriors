from django.contrib import admin

# Register your models here.
from .models import * # Add this import


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(CaUser)
admin.site.register(ProductCategory)
admin.site.register(ShoppingBasket)
admin.site.register(ShoppingBasketItems)
