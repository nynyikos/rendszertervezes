from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from .models import user, category, car, rental, sale
from .serializers import UserSerializer, CategorySerializer, CarSerializer, RentalSerializer, SaleSerializer
from django.contrib.auth import authenticate, login

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
    
    # index.html sablon renderelése
    return render(request, 'autorent/index.html', {'data': data})

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
            return redirect('index')  # Átirányítás a főoldalra bejelentkezés után
        else:
            return HttpResponse('Hibás felhasználónév vagy jelszó')
    return render(request, 'autorent/login.html')
