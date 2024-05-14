from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import login_view, register
from .views import browse_cars

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'rentals', views.RentalViewSet)
router.register(r'sales', views.SaleViewSet)

urlpatterns = [
    path('', views.index, name='index'),  # Ez a kezdőoldal
    path('item/', views.item, name='item'), # Ez csak egy teszt oldal, első lépések között kreáltam, de benne hagyom a feladat végéig, ha esetleg későbbiekben át akarnám dolgozni
    path('user/', views.data_view, name='data_view'),  # user útvonal; 
    path('api/', include(router.urls)),  # API végpontok
    path('login/', login_view, name='login'), # Belépési oldal
    path('browse/', browse_cars, name='browse_cars'), # regisztráció nélkül nézelődő oldal
    path('register/', register, name='register'), #regisztrációs lehetőség
]
