from django import forms
from apps.core.forms import BootstrapFormMixin
from apps.empleados.models import Cargo
from apps.usuarios.forms import RegistroForm
from django.utils import timezone

class CargoForm(BootstrapFormMixin, forms.ModelForm):
   """ Formulario para crear o editar un cargo """
   class Meta:
       model = Cargo
       fields = ["nombre", "salario_base", "descripcion"]
       widgets ={
            "descripcion" : forms.Textarea(attrs={"placeholder": "Decripcion del cargo", "rows":3})
       }
       
class EmpleadoAltaForm(RegistroForm):
    """Alta de empleado: datos de la cuenta (heredados de RegistroForm) + datos laborales."""

    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(activo=True), label="Cargo",
                                   empty_label="Seleccione un cargo")
    salario = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label="Salario")
    fecha_ingreso = forms.DateField(label="Fecha de ingreso", initial=timezone.localdate,
                                    widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
