from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('properties/', views.property_list, name='property_list'),

    path('property/<int:id>/', views.property_detail, name='property_detail'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),
]