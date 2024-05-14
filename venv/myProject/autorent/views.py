from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from rest_framework import viewsets
from .models import user, category, car, rental, sale
from .serializers import UserSerializer, CategorySerializer, CarSerializer, RentalSerializer, SaleSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import car

# Create your views here.
#-----API------
#--------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = category.objects.all()
    serializer_class = CategorySerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = car.objects.all()
    serializer_class = CarSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = rental.objects.all()
    serializer_class = RentalSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = sale.objects.all()
    serializer_class = SaleSerializer
#-----API------
#--------------
def index(request):
    # Egyszerű kezdőlap, ami üdvözli a felhasználót.
    return HttpResponse('Üdv az autófoglalás oldalán! A későbbiekben itt tudsz majd bejelentkezni.')

@login_required
def data_view(request):
    # Lekéri a 'data_type' paramétert a kérésből, alapértelmezett érték 'users'
    data_type = request.GET.get('data_type', 'users')
    
    # Dinamikusan kiválasztás kérés alapján
    data_sources = {
        'users': user.objects.all(),
        'cars': car.objects.all(),
        'rentals': rental.objects.all(),
        'sales': sale.objects.all(),
    }
    
    data = list(data_sources.get(data_type, user.objects.none()).values())
    
    # Ellenőrizd, hogy van-e bejelentkezett felhasználó
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "NoUserLogin"
    
    # index.html sablon renderelése a felhasználónévvel
    return render(request, 'autorent/index.html', {'data': data, 'username': username})

def item(request):
    # Egy egyszerű válasz, ami jelzi, hogy lesz itt tartalom.
    return HttpResponse('<h1>There will be a car here</h1>')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('data_view')  # Átirányítás a felhasználói oldalra
        else:
            # Átirányítás a hiba oldalra, ha hibás a felhasználónév vagy jelszó
            return render(request, 'autorent/invalid_login.html')
    return render(request, 'autorent/login.html')

def browse_cars(request):
    cars = car.objects.all()
    return render(request, 'autorent/browse_cars.html', {'cars': cars})