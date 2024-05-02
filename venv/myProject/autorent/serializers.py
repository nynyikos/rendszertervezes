from rest_framework import serializers
from .models import user, category, car, rental, sale

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = car
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = sale
        fields = '__all__'