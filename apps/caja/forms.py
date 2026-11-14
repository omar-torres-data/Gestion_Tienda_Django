from django import forms
from apps.core.forms import BootstrapFormMixin
from apps.caja.models import Caja

class CajaForm(BootstrapFormMixin, forms.ModelForm):
    """ formulario para crear o editar una caja """
    class Meta:
       model = Caja
       fields = ["nombre", "ubicacion"]
       widgets={
             "nombre": forms.TextInput(attrs={"placeholder": "ejemplo: Caja_1"})
       }
