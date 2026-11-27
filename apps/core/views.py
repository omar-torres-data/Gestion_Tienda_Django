from django.views.generic import TemplateView

from apps.core.constantes import Rol
from apps.core.mixins import RolRequeridoMixins


class Inicio(TemplateView):
    """Página pública de inicio: bienvenida y datos de la tienda. No exige sesión."""
    template_name = "core/inicio.html"


class PanelAdminView(RolRequeridoMixins, TemplateView):
    """Panel del administrador. Exige sesión y rol ADMIN; otro rol recibe 403."""
    template_name = "core/panel_admin.html"
    roles_permitidos = [Rol.ADMIN]
    # (ícono de Bootstrap Icons, título, descripción, nombre de URL o None) de cada módulo
    extra_context = {"modulos": [
        ("bi-people", "Usuarios", "Crear, editar y desactivar cuentas.", None),
        ("bi-box-seam", "Productos", "Catálogo, categorías y precios.", "productos:producto_list"),
        ("bi-clipboard-data", "Inventario", "Stock, movimientos y ajustes.", None),
        ("bi-truck", "Proveedores y compras", "Proveedores, compras y pagos.", "proveedores:proveedor_list"),
        ("bi-person-vcard", "Clientes", "Datos de los clientes.", "clientes:lista_clientes"),
        ("bi-receipt", "Ventas y facturas", "Consultar y anular ventas.", None),
        ("bi-cash-stack", "Caja", "Turnos y arqueos de todas las cajas.", "caja:caja_historial"),
        ("bi-person-badge", "Empleados y nómina", "Cargos, empleados y pagos.", "empleados:empleado_list"),
        ("bi-graph-up", "Reportes", "Ventas, utilidades e inventario.", None),
    ]}


class PanelEmpleadoView(RolRequeridoMixins, TemplateView):
    """Panel del empleado (caja y ventas). Exige sesión y rol EMPLEADO; otro rol recibe 403."""
    template_name = "core/panel_empleado.html"
    roles_permitidos = [Rol.EMPLEADO]
    # Sin costos ni acumulado de caja (RNF-10)
    extra_context = {"modulos": [
        ("bi-cash-coin", "Mi turno de caja", "Abrir, cobrar y cerrar tu turno.", "caja:caja_historial"),
        ("bi-cart-plus", "Nueva venta", "Registrar una venta y cobrarla.", None),
        ("bi-receipt", "Mis ventas", "Consultar las ventas que registraste.", None),
        ("bi-person-vcard", "Clientes", "Crear y consultar clientes.", "clientes:lista_clientes"),
        ("bi-box-seam", "Productos y stock", "Consultar productos y existencias.", None),
        ("bi-wallet2", "Mis pagos", "Consultar tus pagos de salario.", None),
    ]}


class PanelClienteView(RolRequeridoMixins, TemplateView):
    """Panel del cliente (sus datos y facturas). Exige sesión y rol CLIENTE; otro rol recibe 403."""
    template_name = "core/panel_cliente.html"
    roles_permitidos = [Rol.CLIENTE]
    extra_context = {"modulos": [
        ("bi-receipt", "Mis facturas", "Consultar e imprimir tus facturas.", None),
        ("bi-person-circle", "Mis datos", "Ver y actualizar tu perfil.", None),
        ("bi-shop", "Catálogo", "Ver los productos de la tienda.", None),
    ]}
