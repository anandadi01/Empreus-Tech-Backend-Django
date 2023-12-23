from rest_framework import serializers
from .models import Product, User, CartItem, Purchase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):

    is_authenticated = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'description', 'price', 'is_authenticated']

    def get_is_authenticated(self, obj):

        request = self.context.get('request')
        return request.user.is_authenticated


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

        def create(self, validated_data):
            # Implement logic to create and return a new user instance
            return User.objects.create(**validated_data)
        

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity']