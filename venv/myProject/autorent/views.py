from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import user, category, car, rental, sale
from .serializers import UserSerializer, CategorySerializer, CarSerializer, RentalSerializer, SaleSerializer

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
