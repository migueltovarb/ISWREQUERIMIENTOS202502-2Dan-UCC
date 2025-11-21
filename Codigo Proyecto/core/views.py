from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Laboratorio, Reserva, Equipo
from .forms import ReservaForm


@login_required
def home(request):
    laboratorios = Laboratorio.objects.all().order_by('nombre')
    
    # MUESTRA TODAS TUS RESERVAS (sin límite de 5)
    mis_reservas = Reserva.objects.filter(
        usuario=request.user
    ).order_by('-fecha_inicio')  # Más reciente primero

    context = {
        'laboratorios': laboratorios,
        'mis_reservas': mis_reservas,
    }
    return render(request, 'home.html', context)

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            messages.success(request, '¡Reserva creada con éxito! Espera aprobación.')
            return redirect('home')
    else:
        form = ReservaForm()

    return render(request, 'crear_reserva.html', {'form': form})

@login_required
def mis_reservas(request):
    return render(request, 'mis_reservas.html')

@login_required
def labs(request):
    return render(request, 'labs.html')