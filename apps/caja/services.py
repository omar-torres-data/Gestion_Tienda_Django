from apps.caja.models import SesionCaja
from apps.core.constantes import EstadosSesion
from apps.empleados.models import Empleado
from apps.caja.models import Caja
from decimal import Decimal
from apps.caja.exceptions import TurnoError
from django.db import IntegrityError, transaction

def turno_abierto_de(empleado:Empleado) ->SesionCaja | None:
    """ El código ejecuta una consulta al modelo SesionCaja y la consulta usa el id del empleado y el valor de estado"""
    sesion_caja = SesionCaja.objects.filter(
        empleado = empleado,
        estado = EstadosSesion.ABIERTA
    ).first()
    return sesion_caja

@transaction.atomic
def abrir_turno(empleado:Empleado, caja:Caja, monto:Decimal) -> SesionCaja:
   """Abre un turno del empleado en la caja con su dinero base, todo o nada."""

   if turno_abierto_de(empleado):
      raise TurnoError("Usted tiene un turno abierto")
   
   if not caja.activa:
      raise TurnoError("La caja está inactiva")
   
   if SesionCaja.objects.filter(caja=caja, estado =EstadosSesion.ABIERTA).exists():
      raise TurnoError("La caja ya tiene un turno abierto")
   try:
        turno = SesionCaja.objects.create(
            caja=caja, empleado=empleado, monto_inicial=monto
   )
   except IntegrityError:
       raise TurnoError("La caja Tiene un turno abierto")  
   return turno   
     
    