from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Restaurant, Food
from django.contrib.auth import authenticate
from django.contrib import auth
from .forms import LoginForm

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

def login(request):
    ''' 登入 '''
    login_page = loader.get_template('login.html')
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return HttpResponse(login_page.render(context, request))
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                main_page = loader.get_template('main.html')
                context = {'user': request.user,
                           'message': 'login ok'}
                return HttpResponse(login_page.render(context, request))
            else:
                message = 'Login failed (auth fail)'
        else:                    
            print ('Login error (login form is not valid)')
    else:
        print ('Error on request (not GET/POST)')


def logout(request):
    ''' 登出 '''
    auth.logout(request)
    main_html = loader.get_template('main.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))