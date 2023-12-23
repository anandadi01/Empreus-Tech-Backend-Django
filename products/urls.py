from django.urls import path
from django.contrib import admin
from .views import ProductList, SignUpView, LoginView, AddToCartView, BuyProductView


urlpatterns = [
    path('api/products/', ProductList.as_view(), name='product-list'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/buy-product/', BuyProductView.as_view(), name='buy-product'),
]
