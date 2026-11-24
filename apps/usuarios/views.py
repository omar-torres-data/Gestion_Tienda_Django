from django.shortcuts import render
from .forms import RegistroForm, LoginForm
from .services import registrarse
from .exceptions import VinculoError
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from apps.core.constantes import Rol

# Create your views here.

class RegistroView(FormView):
    template_name = "usuarios/registro.html"
    form_class = RegistroForm
    success_url = reverse_lazy("core:inicio")

    def form_valid(self, form):
        try:
            usuario = registrarse(form.cleaned_data)
        except VinculoError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        login(self.request, usuario)
        messages.success(self.request, "Cuenta creada. ¡Bienvenido a TiendaGest!")
        return super().form_valid(form)   

class IngresoView(LoginView):
    """ El metodo gestiona la autenticacion para los diferentes perfiles del usuario"""
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
  
    def get_success_url(self):
        destino = self.get_redirect_url()
        if destino:
            return destino
        elif self.request.user.rol == Rol.ADMIN:   
            return reverse("core:panel_admin")
        elif self.request.user.rol == Rol.EMPLEADO:
            return reverse("core:panel_empleado")   
        elif self.request.user.rol == Rol.CLIENTE:
            return reverse("core:panel_cliente")
        else:
            return reverse("core:inicio")   


class SalirView(LogoutView):
    next_page=reverse_lazy("core:inicio")  #Pendiente defirnir la salida
