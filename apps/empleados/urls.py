from django.urls import path

from . import views

app_name = 'empleados'

urlpatterns = [
    path("cargo/", views.CargoView.as_view(), name="cargo_list"),
    path("cargo_create/", views.CargoCreateView.as_view(), name="cargo_create"),
    path("cargo_update/<int:pk>/", views.CargoUpdateView.as_view(), name="cargo_update"),
    path("cargo_deactivate/<int:pk>/", views.CargoDeactivate.as_view(), name="cargo_deactivate"),
    path("lista_empleados/", views.EmpleadoListView.as_view(), name = "empleado_list"),
    path("empleado_nuevo/", views.EmpleadoCreateView.as_view(), name = "empleado_nuevo"),
]
