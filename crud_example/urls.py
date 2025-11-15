from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehicles/', include('vehiclesapp.urls')),
    path('', lambda request: redirect('list_vehiculos', permanent=False)),  # Ruta raíz: redirige a /vehicles/
]