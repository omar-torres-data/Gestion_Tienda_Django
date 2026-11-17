from django.shortcuts import render
from apps.core.mixins import RolRequeridoMixins
from django.views.generic import ListView, CreateView, UpdateView, FormView
from apps.empleados.models import Cargo, Empleado
from apps.core.constantes import Rol
from apps.empleados.forms import CargoForm, EmpleadoAltaForm
from apps.usuarios.services import alta_empleado
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.

class CargoView(RolRequeridoMixins, ListView):
    """ Vista para listar cargos existentes"""
    template_name = "empleados/cargo_list.html"
    model = Cargo
    context_object_name="cargos"
    roles_permitidos =[Rol.ADMIN] 

class CargoCreateView(RolRequeridoMixins, SuccessMessageMixin, CreateView):
    template_name="empleados/create_cargo.html"
    form_class=CargoForm
    model = Cargo
    roles_permitidos = [Rol.ADMIN] 
    success_message = "El cargo ha sido creado exitosamente "
    success_url = reverse_lazy("empleados:cargo_list")


class CargoUpdateView(RolRequeridoMixins, SuccessMessageMixin, UpdateView):
   template_name ="empleados/create_cargo.html"
   form_class=CargoForm
   model = Cargo
   roles_permitidos=[Rol.ADMIN]
   success_message="El cargo ha sido actualizado exitosamente"
   success_url=reverse_lazy("empleados:cargo_list")

class CargoDeactivate(RolRequeridoMixins, SingleObjectMixin, View):
     """ Vista para desactivar el cargo """
     model = Cargo 
     roles_permitidos = [Rol.ADMIN]

     def post(self, request, *args, **kwargs):
         cargo = self.get_object()
         cargo.activo = not cargo.activo
         cargo.save(update_fields = ["activo"])
         if cargo.activo:
             messages.success(request,"Se ha activado el campo del cargo")
         else:
             messages.success(request, "Se ha desactivado el cargo")    
         return redirect("empleados:cargo_list")


class EmpleadoCreateView(RolRequeridoMixins, FormView):
    template_name="empleados/empleado_form.html"
    form_class = EmpleadoAltaForm
    roles_permitidos=[Rol.ADMIN]
    success_url=reverse_lazy("empleados:empleado_list")

    def form_valid(self, form):
        """Llama al servicio para crear la cuenta y el empleado; luego redirige a la lista."""
        alta_empleado(form.cleaned_data)
        messages.success(self.request, "Empleado creado con éxito")
        return super().form_valid(form)
    
class EmpleadoListView(RolRequeridoMixins, ListView):
    """ Clase que lista los empleados de la tienda """
    model = Empleado
    template_name = "empleados/empleado_list.html"    
    roles_permitidos = [Rol.ADMIN]
    context_object_name="empleados"
    queryset=Empleado.objects.select_related("usuario", "cargo")
    