from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Restaurant, Food

def main(request):
    all_restaurants = Restaurant.objects.all()
    template = loader.get_template('main.html')
    context = {
        'all_restaurants': all_restaurants,
    }
    return HttpResponse(template.render(context, request))

def restaurant(request, id):
    myrestaurant = get_object_or_404(Restaurant, id = id)
    meun = myrestaurant.menu_items.all()
    template = loader.get_template('restaurant.html')
    context = {
        'myrestaurant': myrestaurant,
        'menu': meun,
    }
    return HttpResponse(template.render(context, request))

def food(request, id):
    food = get_object_or_404(Food, id = id)
    template = loader.get_template('food.html')
    context = {
        'food': food,
    }
    return HttpResponse(template.render(context, request))