from django.conf.urls import patterns, include, url

import views

urlpatterns = [
    path('', views.catalog, name="catalog" ),
]