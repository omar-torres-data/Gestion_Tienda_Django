from django.urls import path

from . import views

app_name = 'caja'

urlpatterns = [
    path("caja_list/", views.CajaListView.as_view(), name="caja_list"),
    path("caja_create/", views.CajaCreateView.as_view(), name="caja_create"),
    path("caja_update/<int:pk>/", views.CajaUpdateView.as_view(), name="caja_update"),
    path("caja_deactivate/<int:pk>/", views.CajaDeactivateView.as_view(), name="caja_deactivate"),
    path("apertura/", views.AperturaTurnoView.as_view(), name="apertura"),
    path("historial/", views.TurnoHistorialView.as_view(), name="caja_historial"),
]
