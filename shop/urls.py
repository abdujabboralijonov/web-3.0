from django.urls import path
from .views import Index
from . import views

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
