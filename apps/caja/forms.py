from django import forms
from apps.core.forms import BootstrapFormMixin
from apps.core.constantes import EstadosSesion
from apps.caja.models import Caja


class CajaForm(BootstrapFormMixin, forms.ModelForm):
    """ formulario para crear o editar una caja """
    class Meta:
       model = Caja
       fields = ["nombre", "ubicacion"]
       widgets={
             "nombre": forms.TextInput(attrs={"placeholder": "ejemplo: Caja_1"})
       }


class AperturaTurnoForm(BootstrapFormMixin, forms.Form):
    """Apertura de turno: el cajero elige la caja y escribe el dinero base."""

    caja = forms.ModelChoiceField(
        queryset=Caja.objects.filter(activa=True).exclude(sesion__estado=EstadosSesion.ABIERTA),
        label="Caja",
        empty_label="Seleccione una caja",
    )
    monto_inicial = forms.DecimalField(
        max_digits=12, decimal_places=2, min_value=0, label="Dinero base",
    )
