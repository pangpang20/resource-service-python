"""
URL configuration for user-service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django_dws.views import CustomerView, LocationView,OrderView,OrderItemView,ProductView,SupplyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('django_dws.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # 根路径路由，指向首页视图

    path('customers/', CustomerView.as_view(), name='customer-list'),
    path('locations/', LocationView.as_view(), name='locations-list'),
    path('orders/', OrderView.as_view(), name='orders-list'),
    path('orderitems/', OrderItemView.as_view(), name='orderitems-list'),
    path('products/', ProductView.as_view(), name='products-list'),
    path('supplys/', SupplyView.as_view(), name='supplys-list'),



    path('customers/<str:pk>/', CustomerView.as_view(), name='customer-detail'),
    path('locations/<str:pk>/', LocationView.as_view(), name='location-detail'),
    path('orders/<str:pk>/', OrderView.as_view(), name='orders-detail'),
    path('orderitems/<str:pk>/', OrderItemView.as_view(), name='orderitems-detail'),
    path('products/<str:pk>/', ProductView.as_view(), name='products-detail'),
    path('supplys/<str:pk>/', SupplyView.as_view(), name='supplys-detail'),
]
