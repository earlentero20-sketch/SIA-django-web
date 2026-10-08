from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('', views.index, name='product-list'),
    path('products/add/', views.product_create, name='product-create'),
    path('products/<int:product_id>/edit/', views.product_update, name='product-update'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product-delete'),
]
