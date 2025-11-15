from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo
from .forms import VehiculoForm

# Read: Listado de vehículos
def list_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiclesapp/list_view.html', {'vehiculos': vehiculos})

# Create: Crear nuevo vehículo
def create_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_vehiculos')
    else:
        form = VehiculoForm()
    return render(request, 'vehiclesapp/create_view.html', {'form': form})

# Update: Actualizar vehículo
def update_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('list_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiclesapp/update_view.html', {'form': form})

# Delete: Eliminar vehículo
def delete_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('list_vehiculos')
    return render(request, 'vehiclesapp/delete_view.html', {'vehiculo': vehiculo})