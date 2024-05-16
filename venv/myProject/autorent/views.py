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
from django.urls import reverse
from django.http import HttpResponseRedirect

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

@login_required
def data_view(request):
    #--> tábla lekérés, alapérték a user
    data_type = request.GET.get('data_type', 'users')
    #--> dinamikus tábla lekérés az alapján amit választok
    data_sources = {
        'users': user.objects.all(),
        'cars': car.objects.all(),
        'rentals': rental.objects.all(),
        'sales': sale.objects.all(),
    }
    
    data = list(data_sources.get(data_type, user.objects.none()).values())

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "NoUserLogin"
    return render(request, 'autorent/index.html', {'data': data, 'username': username})


def login_view(request): #--> bejelentkezési oldal
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            return HttpResponse('Hibás felhasználónév vagy jelszó', status=401)
        
    return render(request, 'autorent/login.html')

def browse_cars(request): #--> alap reg nélküli oldal, csak kocsinézés
    cars = car.objects.all()
    return render(request, 'autorent/browse_cars.html', {'cars': cars})

def register(request): #--> regisztrálás + belépés
    if request.method == 'POST' and 'password2' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                return HttpResponse("A felhasználónév már foglalt.", status=400)
            else:
                django_user = User.objects.create_user(username=username, password=password)
                django_user.save()

                my_user = user(username=username, name=username)  
                my_user.save()

                login(request, django_user) 
                return redirect('data_view')
        else:
            return HttpResponse("A jelszavak nem egyeznek.", status=400)
    
    return render(request, 'autorent/login.html')




def redirect_to_login(request):#--> vissza login oldalra redirect
    return redirect('/autorent/login/')


@login_required #-->kocsifoglalás hozzáadás
def create_rental(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        car = car.objects.get(id=car_id)
        user = request.user  

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

@login_required #---> foglalás
def create_rental(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if not car_id or not from_date or not to_date:
            return HttpResponse('Minden mező kitöltése kötelező!', status=400)

        try:
            selected_car = car.objects.get(id=car_id)
            user_instance = user.objects.get(username=request.user.username)

            new_rental = rental(user=user_instance, car=selected_car, from_date=from_date, to_date=to_date)
            new_rental.save()
            # Válasz + visszagomb
            return HttpResponse(f'''
                <html>
                <head><title>Foglalás Sikeres</title></head>
                <body>
                <h1>Foglalás sikeres!</h1>
                <p><a href="{reverse('data_view')}">Vissza a felhasználói oldalra</a></p>
                </body>
                </html>
            ''')
        except car.DoesNotExist:
            return HttpResponse('A kiválasztott autó nem létezik.', status=404)
        except user.DoesNotExist:
            return HttpResponse('Nem található felhasználó.', status=404)
    else:
        available_cars = car.objects.all()
        return render(request, 'autorent/index.html', {'available_cars': available_cars})
