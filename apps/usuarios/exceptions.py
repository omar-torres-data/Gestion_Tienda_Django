"""
Errores de negocio de la app usuarios.

Cada clase hereda de la clase base Exception.
El servicio la lanza con raise cuando una regla de negocio no se cumple.
No requiere que se escriba código, ya que lo que se necesita se hereda de Exception.
"""


class VinculoError(Exception):
    """Error de negocio al vincular un cliente con una cuenta."""


class EmpleadoError(Exception):
    """Error de negocio al retirar o reingresar un empleado."""
