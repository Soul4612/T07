from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Member, Restaurant, Food, CartItem, OrderItem
from .forms import LoginForm, RegisterForm, SearchForm, AddFoodForm

def main(request):
    if request.method == 'GET':
        all_restaurants = Restaurant.objects.all()
        Search_Form = SearchForm()
        context = {
            'all_restaurants': all_restaurants,
            'Search_Form': Search_Form,
        }
        return render(request, 'main.html', context)
    
    Search_Form = SearchForm(request.POST)
    if not Search_Form.is_valid():
        context = {
            'Search_Form': Search_Form,
            'message': "系統錯誤，請再試一次",
        }
        return render(request, 'result.html', context)
    
    text = Search_Form.cleaned_data['text']
    foods = Food.objects.filter(name__icontains=text)
    restaurants = Restaurant.objects.filter(name__icontains=text)
    food_set = set()
    for restaurant in restaurants:
        food_set.update(restaurant.menu_items.all())
    foods = sorted(set(foods) | food_set, key=lambda x: x.get_rating(), reverse=True)
    context = {
        'Search_Form': Search_Form,
        'message': f"共搜尋到{len(foods)}個結果",
        'foods': foods,
    }
    return render(request, 'result.html', context)

def restaurant(request, id):
    myrestaurant = get_object_or_404(Restaurant, id = id)
    meun = myrestaurant.menu_items.all()
    context = {
        'myrestaurant': myrestaurant,
        'menu': meun,
    }
    return render(request, 'restaurant.html', context)

def food(request, id):
    food = get_object_or_404(Food, id = id)
    addfood_success = False
    quantity = 0
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        addofood_form = AddFoodForm(request.POST)
        if addofood_form.is_valid():
            quantity = addofood_form.cleaned_data['quantity']
            member = Member.objects.get(user=request.user)
            cartitem, created = CartItem.objects.get_or_create(member=member, food=food, defaults={'quantity': quantity})
            if not created:
                cartitem.quantity += quantity
                cartitem.save()
            addfood_success = True
        else:
            context = {
                'food': food,
                'addofood_form': addofood_form,
                'addfood_success': addfood_success,
                'message': "系統錯誤！請再試一次",
            }
            return render(request, 'food.html', context)
    else:
        addofood_form = AddFoodForm()
    
    context = {
        'food': food,
        'addofood_form': addofood_form,
        'addfood_success': addfood_success,
        'quantity': quantity,
    }
    return render(request, 'food.html', context)

@login_required
def member_info(request):
    member = Member.objects.get(user=request.user)
    context = {
        'member': member,
    }
    return render(request, 'member_info.html', context)

def login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'login.html', context)
    
    login_form = LoginForm(request.POST)
    if not login_form.is_valid():
        context = {
            'login_form': login_form,
            'message': "系統錯誤",
        }
        return render(request, 'login.html', context)
    
    username = login_form.cleaned_data['username']
    password = login_form.cleaned_data['password']
    if not Member.objects.filter(username=username).exists():
        context = {
            'login_form': login_form,
            'message': "帳號不存在",
        }
        return render(request, 'login.html', context)
    
    user = authenticate(username=username, password=password)
    if user is None:
        context = {
            'login_form': login_form,
            'message': "密碼錯誤",
        }
        return render(request, 'login.html', context)
    
    auth.login(request, user)
    return redirect('member_info')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, 'register.html', context)
    
    register_form = RegisterForm(request.POST)
    if not register_form.is_valid():
        context = {
            'register_form': register_form,
            'message': "系統錯誤",
        }
        return render(request, 'register.html', context)

    first_name = register_form.cleaned_data['first_name']
    last_name = register_form.cleaned_data['last_name']
    username = register_form.cleaned_data['username']
    password = register_form.cleaned_data['password']
    password2 = register_form.cleaned_data['password2']
    
    if Member.objects.filter(username=username).exists():
        context = {
            'register_form': register_form,
            'message': "用戶已存在",
        }
        return render(request, 'register.html', context)
    
    if password != password2:
        context = {
            'register_form': register_form,
            'message': "確認密碼不相符",
        }
        return render(request, 'register.html', context)
    
    user = User.objects.create_user(username=username, password=password)
    user.save()
    new_member = Member(user=user, first_name=first_name, last_name=last_name, username=username, password=password)
    new_member.save()
    return render(request, 'register_successful.html')

@login_required
def cart(request):
    member = Member.objects.get(user=request.user)
    cart = member.cart_items.all()
    message = ''
    if request.method == 'POST':
        if 'update' in request.POST:
            cartitem_id = request.POST.get('update')
            cartitem = CartItem.objects.get(id=cartitem_id)
            new_quantity = int(request.POST.get(f'quantity_{cartitem_id}'))
            cartitem.quantity = new_quantity
            cartitem.save()
            message = f"餐點數量修改成功!\n餐點 '{cartitem.food.name}' 的數量已修改為 {cartitem.quantity}份"
        elif 'delete' in request.POST:
            cartitem_id = request.POST.get('delete')
            cartitem = CartItem.objects.get(id=cartitem_id)
            message = f"餐點 '{cartitem.food.name}' ×{cartitem.quantity} 刪除成功!"
            cartitem.delete()
        else:
            order_list = request.POST.getlist('checkbox')
            for i in order_list:
                cartitem = CartItem.objects.get(id=i)
                orderitem = OrderItem(member=member, food=cartitem.food, quantity=cartitem.quantity)
                orderitem.save()
                cartitem.delete()
            message = "餐點訂購成功!請至訂單進行取餐及評分!"
        
        cart = member.cart_items.all()
        context = {
            'cart': cart,
            'message': message,
        }
        return render(request, 'cart.html', context)
    
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

@login_required
def order(request):
    member = Member.objects.get(user=request.user)
    order = member.order_items.all()
    if request.method == 'POST':
        id = request.POST.get('rating')
        orderitem = OrderItem.objects.get(id=id)
        star = int(request.POST.get('star'))
        food = Food.objects.get(id=orderitem.food.id)
        food.sales += orderitem.quantity
        food.stars += star * orderitem.quantity
        food.save()
        orderitem.delete()
        order = member.order_items.all()
        context = {
            'order': order,
            'message': "感謝您的評分!祝您用餐愉快!",
        }
        return render(request, 'order.html', context)
    context = {
        'order': order,
    }
    return render(request, 'order.html', context)