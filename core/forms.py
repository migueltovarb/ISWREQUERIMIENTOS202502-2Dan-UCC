from django import forms
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from .models import Reserva, Laboratorio


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['laboratorio', 'equipo', 'fecha_inicio', 'fecha_fin',
                  'es_grupal', 'cantidad_personas', 'notas']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')
        lab = cleaned_data.get('laboratorio')

        if not inicio or not fin or not lab:
            return cleaned_data  # Si falta algún campo, Django ya mostrará error

        # 1. No permitir reservas en el pasado
        if inicio < timezone.now():
            raise forms.ValidationError("No puedes reservar en fechas/horas pasadas.")

        # 2. Fecha fin debe ser posterior a fecha inicio
        if fin <= inicio:
            raise forms.ValidationError("La fecha/hora de fin debe ser posterior a la de inicio.")

        # 3. Validar solapamiento (excluye la propia reserva si se está editando)
        solapadas = Reserva.objects.filter(
            laboratorio=lab,
            estado__in=['pendiente', 'aprobada'],
            fecha_inicio__lt=fin,
            fecha_fin__gt=inicio
        )
        if self.instance and self.instance.pk:
            solapadas = solapadas.exclude(pk=self.instance.pk)

        if solapadas.exists():
            raise forms.ValidationError("Ya existe una reserva aprobada o pendiente en ese horario.")

        # 4. Validar aforo del laboratorio
        personas_actuales = Reserva.objects.filter(
            laboratorio=lab,
            estado='aprobada',
            fecha_inicio__lt=fin,
            fecha_fin__gt=inicio
        ).aggregate(total=Sum('cantidad_personas'))['total'] or 0

        nuevas_personas = cleaned_data.get('cantidad_personas', 0)
        if personas_actuales + nuevas_personas > lab.capacidad:
            raise forms.ValidationError(
                f"Supera la capacidad del laboratorio ({lab.capacidad} personas). "
                f"Actualmente hay {personas_actuales} reservadas."
            )

        return cleaned_data