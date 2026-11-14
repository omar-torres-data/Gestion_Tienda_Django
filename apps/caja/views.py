from django.views.generic import ListView, CreateView, UpdateView
from apps.core.mixins import RolRequeridoMixins
from apps.caja.models import Caja
from apps.core.constantes import Rol
from django.contrib.messages.views import SuccessMessageMixin
from apps.caja.forms import CajaForm
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
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


