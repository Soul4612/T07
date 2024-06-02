from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('restaurant/<int:id>', views.restaurant, name='restaurant'),
    path('food/<int:id>', views.food, name='food'),
]
