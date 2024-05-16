from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from rest_framework import viewsets
from .models import user, category, car, rental, sale
from .serializers import UserSerializer, CategorySerializer, CarSerializer, RentalSerializer, SaleSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import car
from django.contrib.auth.models import User

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
    # Egyszerű kezdőlap, ami üdvözli a felhasználót. ---- ez azóta módosítva lett, már nem él.
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


def login_view(request):
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('data_view')
        else:
            return HttpResponse('Hibás felhasználónév vagy jelszó', status=401)

    return render(request, 'autorent/login.html')

def browse_cars(request):
    cars = car.objects.all()
    return render(request, 'autorent/browse_cars.html', {'cars': cars})

def register(request):
    if request.method == 'POST' and 'password2' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                return HttpResponse("A felhasználónév már foglalt.", status=400)
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('data_view')
        else:
            return HttpResponse("A jelszavak nem egyeznek.", status=400)
    
    return render(request, 'autorent/login.html')



def redirect_to_login(request):
    return redirect('/autorent/login/')

def user_table(request):
    return render(request, 'autorent/table.html') 

@login_required
def create_rental(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        car = car.objects.get(id=car_id)
        user = request.user  # A bejelentkezett felhasználó

        new_rental = rental(user=user, car=car, from_date=from_date, to_date=to_date)
        new_rental.save()

        return HttpResponse('Foglalás sikeres!')
    else:
        available_cars = car.objects.all()
        return render(request, 'autorent/index.html', {'available_cars': available_cars})

@login_required
def index(request):
    available_cars = car.objects.all()
    username = request.user.username if request.user.is_authenticated else "NoUserLogin"
    return render(request, 'autorent/index.html', {'available_cars': available_cars, 'username': username})
