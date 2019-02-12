from django.urls import path

from . import views

urlpatterns = [
    path('', views.catalog, name="catalog" ),
    path('cart/', views.cart, name="cart"),
    path('cart/remove/', views.removefromcart, name = "remove"),
]