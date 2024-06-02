from django.contrib import admin
from .models import Member, Restaurant, Food, CartItem, OrderItem

class MemberAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name")
admin.site.register(Member, MemberAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "rating", "img")
    def rating(self, obj):
        return obj.get_rating()
    rating.short_description = '評分'
admin.site.register(Restaurant, RestaurantAdmin)

class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "stars", "sales", "rating", "img")
    def rating(self, obj):
        return obj.get_rating()
    rating.short_description = '評分'
admin.site.register(Food, FoodAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ("member", "food", "quantity")
admin.site.register(CartItem, CartItemAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("member", "food", "quantity")
admin.site.register(OrderItem, OrderItemAdmin)
