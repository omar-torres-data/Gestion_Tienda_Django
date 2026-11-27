"""
Errores de negocio de la app caja.

Cada clase hereda de la clase base Exception.
El servicio la lanza con raise cuando una regla de negocio no se cumple.

"""
class TurnoError(Exception):
    """Cuando se produce errores en los cambios de turno se lanza un error"""


