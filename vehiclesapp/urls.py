from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_vehiculos, name='list_vehiculos'),
    path('create/', views.create_vehiculo, name='create_vehiculo'),
    path('update/<int:pk>/', views.update_vehiculo, name='update_vehiculo'),
    path('delete/<int:pk>/', views.delete_vehiculo, name='delete_vehiculo'),
]