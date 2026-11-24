from django.urls import path

from . import views

app_name = 'clientes'

urlpatterns = [
    path("cliente/", views.ClienteListView.as_view(), name="lista_clientes"),
    path("cliente_nuevo/", views.ClienteCreateView.as_view(), name="create_cliente"),
    path("cliente_update/<int:pk>/", views.ClienteUpdateView.as_view(), name="update_cliente"),
    path("cliente_detalle/<int:pk>/", views.ClienteDetailView.as_view(), name="detalle_cliente")
]
