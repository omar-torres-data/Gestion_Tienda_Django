from django import forms
from apps.core.forms import BootstrapFormMixin
from apps.clientes.models import Cliente

class ClienteForm(BootstrapFormMixin, forms.ModelForm):
    """ Formulario para crear o editar un cliente"""

    class Meta:
        model = Cliente
        fields=["nombre", "tipo_documento", "numero_documento", "telefono", "correo", "direccion"]
        widgets ={
            "nombre":forms.TextInput(attrs={"placeholder":"Digite nombres y apellidos"}),
            "numero_documento":forms.TextInput(attrs={"placeholder":"Digite el número del documento"}),
            "telefono":forms.TextInput(attrs={"placeholder":"Digite su número de teléfono"}),
            "correo":forms.EmailInput(attrs={"placeholder":"Digite su correo electrónico"}),
            "direccion":forms.TextInput(attrs={"placeholder":"Digite su dirección"}),
        }
