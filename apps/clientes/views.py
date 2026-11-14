from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from apps.core.constantes import Rol
from apps.clientes.models import Cliente
from apps.core.mixins import RolRequeridoMixins
from apps.clientes.forms import ClienteForm
from django.urls import reverse_lazy
# Create your views here.

class ClienteListView(RolRequeridoMixins,ListView):
    """ Se lista los clientes"""
    model = Cliente
    template_name="clientes/cliente_list.html" 
    roles_permitidos=[Rol.ADMIN, Rol.EMPLEADO]
    context_object_name="clientes"

    def get_queryset(self):
        """Lista los clientes; si se escribió un documento en el buscador, filtra por coincidencia parcial (RF-16)."""
        clientes = super().get_queryset()  #Prepara consulta a la tabla de clientes
        documento = self.request.GET.get("documento", "").strip()  #obtiene del numero de documento de la url
        if documento:
            clientes=clientes.filter(numero_documento__icontains=documento) # busca clientes con coincidencias en documento
        return clientes   
    
class ClienteCreateView(RolRequeridoMixins, SuccessMessageMixin, CreateView):
    """ Se crea un nuevo cliente """  
    model = Cliente
    template_name="clientes/create_cliente.html"
    form_class = ClienteForm
    roles_permitidos = [Rol.ADMIN, Rol.EMPLEADO]
    success_message = "Se ha creado un cliente nuevo"
    success_url = reverse_lazy("clientes:lista_clientes")

class ClienteUpdateView(RolRequeridoMixins, SuccessMessageMixin, UpdateView):
    """Actualización de los datos del cliente"""  
    model = Cliente
    template_name = "clientes/create_cliente.html"
    form_class = ClienteForm
    roles_permitidos = [Rol.ADMIN]
    success_message = "Se ha actualizado exitosamente el cliente"
    success_url = reverse_lazy("clientes:lista_clientes")

class ClienteDetailView(RolRequeridoMixins, DetailView):
    """Muestra todos los datos de un cliente. Solo lectura."""
    model = Cliente
    template_name = "clientes/cliente_detalle.html"
    roles_permitidos = [Rol.ADMIN, Rol.EMPLEADO]
    context_object_name = "cliente"

    

     
