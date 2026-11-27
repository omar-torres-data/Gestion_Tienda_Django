from django.db import transaction
from apps.clientes.models import Cliente
from .models import Usuario
from apps.core.constantes import Rol, EstadoEmpleado
from apps.empleados.models import Empleado
from .exceptions import VinculoError, EmpleadoError
from apps.caja.services import turno_abierto_de
"""
Cliente.objects consulta la tabla clientes. .select_for_update() 
lee la fila y la bloquea hasta que termine la transacción, 
para que nadie más la modifique mientras tanto. .filter(tipo_documento=..., documento=...) 
busca el cliente con ese tipo y número de documento. Y .first() 
devuelve el primero que encuentre, o None si no existe, sin lanzar error
"""

def crear_cuenta(datos: dict, rol: str) -> Usuario:
    """Crea una cuenta de acceso. No sabe nada de clientes ni empleados."""
    usuario = Usuario.objects.create_user(
        email=datos["email"],
        password=datos["password1"],
        first_name=datos["first_name"],
        last_name=datos["last_name"],
        tipo_documento=datos["tipo_documento"],
        documento=datos["documento"],
        telefono=datos.get("telefono", ""), # tecnica recomendada para datos no obligatorios
        rol=rol,
    )
    return usuario

def registrar_cliente(datos: dict) -> Cliente:
    cliente = Cliente.objects.create(
        nombre = f"{datos["first_name"]} {datos["last_name"]}",
        tipo_documento = datos["tipo_documento"],
        numero_documento = datos["documento"],
        telefono = datos.get("telefono", ""),
        direccion=datos.get("direccion", ""),
        correo=datos.get("email", ""),
    )
    return cliente

def obtener_o_crear_cliente(datos: dict) -> Cliente:
    """Devuelve el cliente con ese documento (bloqueado); si no existe, lo crea.
       Cubre a quien ya compró sin cuenta (P3): se reutiliza su registro.
    """
    cliente = Cliente.objects.select_for_update().filter(
        tipo_documento=datos["tipo_documento"],
        numero_documento=datos["documento"],
    ).first()
    if cliente:
        return cliente
    return registrar_cliente(datos)
"""
   if cliente.usuario: valida que el cliente tenga un usuario
   si no se entra por el if se vincula el cliente con el usuario
   Al vincularlos, la app puede saber qué cliente es la persona que inició sesión y mostrarle sus datos:
"""
def vincular_cliente_cuenta(cliente: Cliente, usuario: Usuario) -> Usuario:

    if cliente.usuario:   # El cliente ya tiene usuario registrado
        raise VinculoError("El cliente ya tiene cuenta")
    
    cliente.usuario = usuario
    cliente.save(update_fields=["usuario"])
    return usuario

@transaction.atomic
def registrarse(datos: dict) -> Usuario:
    """Proceso de la página de registro: cuenta + cliente + vínculo, todo o nada."""

    usuario = crear_cuenta(datos, rol=Rol.CLIENTE)
    cliente = obtener_o_crear_cliente(datos)
    vincular_cliente_cuenta(cliente, usuario)
    return usuario

def registrar_empleado(usuario: Usuario, datos: dict) -> Empleado:
    """ Este servicio recibe un usuario y sus datos, registra el empleado y lo retorna"""
    empleado = Empleado.objects.create(
        usuario = usuario,
        cargo =datos["cargo"],
        salario = datos["salario"],
        fecha_ingreso = datos["fecha_ingreso"],
    )
    return empleado

def fijar_acceso(usuario: Usuario, estado: bool) -> Usuario:
    """Activa o bloquea la cuenta del usuario y guarda solo ese campo."""
    usuario.is_active = estado 
    usuario.save(update_fields=["is_active"])
    return usuario

"""
   Al entrar a la uncion se crea una transacción, si no hay errores se confirma con un commit,
   Si hay error, se deshace todo con un Rollback
"""
@transaction.atomic
def alta_empleado(datos: dict) -> Empleado:
    """Alta de empleado: cuenta con rol EMPLEADO + registro de empleado, todo o nada."""
    usuario = crear_cuenta(datos, Rol.EMPLEADO)
    empleado = registrar_empleado(usuario, datos)
    return empleado

def fijar_estado_empleado(empleado: Empleado, estado: str) -> Empleado:
    """ Cambia el estado laboral del empleado y guarda solo ese campo """
    empleado.estado = estado
    empleado.save(update_fields=["estado"])
    return empleado

def bloquear_empleado(empleado_id: int) -> Empleado:
    """Lee el empleado y bloquea su fila hasta que termine la transacción."""
    return Empleado.objects.select_for_update().select_related("usuario").get(pk=empleado_id)

@transaction.atomic
def retirar_empleado(empleado_id: int) -> Empleado:
    """Retira al empleado: estado RETIRADO y cuenta bloqueada, todo o nada."""
    empleado = bloquear_empleado(empleado_id)
    if empleado.estado == EstadoEmpleado.RETIRADO:
        raise EmpleadoError("El empleado ya está retirado.")
    
    if turno_abierto_de(empleado):
       raise EmpleadoError("No se puede retirar: el empleado tiene un turno de caja abierto.")
    fijar_estado_empleado(empleado, EstadoEmpleado.RETIRADO)
    fijar_acceso(empleado.usuario, False)
    return empleado

@transaction.atomic
def reingresar_empleado(empleado_id: int) -> Empleado:
    """ Reingresa a un empleado RETIRADO: estado ACTIVO y cuenta habilitada, todo o nada."""

    empleado = bloquear_empleado(empleado_id)   #Bloquea dentro de la transaccion

    if empleado.estado != EstadoEmpleado.RETIRADO:
        raise EmpleadoError("El empleado no está retirado")

    fijar_estado_empleado(empleado, EstadoEmpleado.ACTIVO)
    fijar_acceso(empleado.usuario, True)
    return empleado


    
