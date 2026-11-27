from django.views.generic import ListView, CreateView, UpdateView, FormView
from apps.core.mixins import RolRequeridoMixins
from apps.caja.models import Caja, SesionCaja
from apps.core.constantes import Rol
from django.contrib.messages.views import SuccessMessageMixin
from apps.caja.forms import CajaForm, AperturaTurnoForm
from apps.caja.services import abrir_turno
from apps.caja.exceptions import TurnoError
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from apps.caja.models import Caja, SesionCaja
# Create your views here.

class CajaListView(RolRequeridoMixins, ListView):
    template_name = "caja/caja_list.html"
    model = Caja
    roles_permitidos = [Rol.ADMIN]
    context_object_name="cajas"

class CajaCreateView(RolRequeridoMixins, SuccessMessageMixin, CreateView):
    model = Caja
    template_name = "caja/caja_create.html" 
    form_class = CajaForm
    roles_permitidos=[Rol.ADMIN]
    success_message="Se ha creado una caja nueva con éxito"
    success_url = reverse_lazy("caja:caja_list")
  

class CajaUpdateView(RolRequeridoMixins, SuccessMessageMixin, UpdateView):
    model = Caja
    template_name = "caja/caja_create.html"
    form_class = CajaForm
    roles_permitidos=[Rol.ADMIN]
    success_message="Se ha actualizado la caja exitosamente"
    success_url = reverse_lazy("caja:caja_list")

class CajaDeactivateView(RolRequeridoMixins, SingleObjectMixin, View):
    """ Vista para activar o desactivar Caja """
    model = Caja
    roles_permitidos=[Rol.ADMIN]

    def post(self, request, *args, **kwargs):
        caja=self.get_object()
        caja.activa = not caja.activa
        caja.save(update_fields=["activa"])
        if caja.activa:
            messages.success(request,"La caja se ha activado exitosamente")
        else:
            messages.success(request, "La caja ha sido desactivada exitosamente")  
        return redirect("caja:caja_list")        

class AperturaTurnoView(RolRequeridoMixins, FormView):
    """El empleado abre su turno: elige caja y dinero base; el servicio crea el turno."""
    template_name = "caja/apertura.html"
    form_class = AperturaTurnoForm
    roles_permitidos = [Rol.EMPLEADO]
    success_url = reverse_lazy("core:panel_empleado")

    def form_valid(self, form):
        empleado = self.request.user.empleado
        try:
            abrir_turno(
                empleado,
                form.cleaned_data["caja"],
                form.cleaned_data["monto_inicial"],
            )
        except TurnoError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        messages.success(self.request, "Turno abierto con éxito.")
        return super().form_valid(form)

class TurnoHistorialView(RolRequeridoMixins, ListView):
    """Historial de turnos: el ADMIN ve todos; el EMPLEADO solo los suyos."""
    template_name = "caja/caja_historial.html"
    context_object_name = "turnos"
    roles_permitidos = [Rol.ADMIN, Rol.EMPLEADO]

    def get_queryset(self):
        turnos = SesionCaja.objects.select_related("caja", "empleado__usuario").order_by("-fecha_apertura")
        if self.request.user.rol == Rol.EMPLEADO:
            turnos = turnos.filter(empleado=self.request.user.empleado)
        return turnos