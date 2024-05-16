from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import login_view, browse_cars, register, create_rental

#--> Router beállítása az API végpontok számára
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'rentals', views.RentalViewSet)
router.register(r'sales', views.SaleViewSet)

#--> URL minták definiálása
urlpatterns = [
    path('', login_view, name='login'),  #--> Az alapértelmezett útvonal a bejelentkezési oldalra visz
    path('index/', views.index, name='index'),  #--> Az index oldal, ahol az autók listázása és foglalása történik
    path('user/', views.data_view, name='data_view'),  #--> Csak bejelentkezett felhasználók érik el; adatok megjelenítése
    path('api/', include(router.urls)),  #--> API végpontok
    path('browse/', browse_cars, name='browse_cars'),  #--> Regisztráció nélküli nézelődő oldal
    path('register/', register, name='register'),  #--> Regisztrációs lehetőség
    path('create_rental/', create_rental, name='create_rental'),  #--> Kocsi foglalás
]