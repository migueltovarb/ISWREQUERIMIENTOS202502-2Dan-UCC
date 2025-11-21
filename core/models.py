from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PerfilUsuario(models.Model):
    ROLES = (('estudiante', 'Estudiante'), ('profesor', 'Profesor'), ('admin', 'Administrador'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, default='estudiante')
    correo_institucional = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    capacidad = models.PositiveIntegerField(default=30)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.laboratorio}"

class Reserva(models.Model):
    ESTADOS = (('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('cancelada', 'Cancelada'), ('rechazada', 'Rechazada'))
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    es_grupal = models.BooleanField(default=False)
    cantidad_personas = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('laboratorio', 'fecha_inicio', 'fecha_fin')

    def __str__(self):
        return f"Reserva {self.id} - {self.laboratorio} - {self.usuario}"