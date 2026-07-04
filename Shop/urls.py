"""
URL configuration for CakeShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from. import views


urlpatterns = [
    path('', views.home , name='home'),
    path('shop/', views.shop, name='shop'),
    path('why/', views.why , name='why'),
    path('testimonial/', views.testimonial , name='testimonial'),
    path('contact/', views.contact , name='contact'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
path('cart/', views.cart_view, name='cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove'),


 path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]