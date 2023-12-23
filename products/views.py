from django.shortcuts import render, redirect

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.views.generic.edit import CreateView
from .models import User
from django.urls import reverse_lazy

from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer, CartItemSerializer, PurchaseSerializer


from rest_framework.pagination import PageNumberPagination

from .models import CartItem, Purchase


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BuyProductView(generics.CreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Request data:", request.data)
            response = super().create(request, *args, **kwargs)
            print("Response data:", response.data)
            return redirect('api/login')
            # return response
        except Exception as e:
            print("Error:", str(e))
            raise


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print("Entering LoginView")
        print(f"Request body: {request.body}")
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)

        print(f"Login attempt with email: {email}, password: {password}")

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email and password and obtain auth token
        response = obtain_auth_token(request._request)
        # print(f"Response body: {response.body}")

        print(f"Login response: {response.status_code}, data: {response.data}")


    
        if response.status_code == status.HTTP_200_OK:
            # Successful login
            user = request.user
            serializer = UserSerializer(user)
            data = {'token': response.data['token'], 'user': serializer.data}
            print("Exiting LoginView with IF")
            return Response(data, status=status.HTTP_200_OK)
        else:
            # Login failed, return the response as is
            print("Exiting LoginView with ELSE")
            return response
        

# class SignUpView(CreateView):
#     model = User
#     fields = ['name', 'email', 'password', 'confirmPassword']  # Adjust fields as per your model
#     template_name = 'signup.html'  # Provide the template name
#     success_url = reverse_lazy('success_page')  # Replace 'success_page' with your success page name