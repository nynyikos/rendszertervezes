from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, CarViewSet, RentalViewSet, SaleViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'cars', CarViewSet)
router.register(r'rentals', RentalViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('',views.index,name='index'),
    path('item/',views.item,name='item'),
    path('', include(router.urls)),
]


