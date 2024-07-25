"""
URL configuration for hack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hackathon.views import (
    ViewPacienteLogin,
    ViewMedicoLogin,
    ViewMedicoAddHorarioAgenda,
    ViewMedicoRemoveHorarioAgenda,
    ViewPacienteMedicos,
    ViewPacienteAgendaMedico,
    ViewPacienteConsultas,
    ViewPacienteSolicitaConsulta,
    ViewPacienteCancelaConsulta,
    ViewMedicoConsultas,
    ViewMedicoConfirmaConsulta,
    ViewMedicoCancelaConsulta,
    PingView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', PingView.as_view(), name="ping"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/medico/login/', ViewMedicoLogin.as_view(), name='token_obter_medico'),
    path('api/medico/agenda/add/', ViewMedicoAddHorarioAgenda.as_view(), name='add_horario_agenda'),
    path('api/medico/agenda/remove/', ViewMedicoRemoveHorarioAgenda.as_view(), name='remove_horario_agenda'),
    path('api/medico/consultas/', ViewMedicoConsultas.as_view(), name='medico_consultas'),
    path('api/medico/consultas/confirmar/', ViewMedicoConfirmaConsulta.as_view(), name='medico_confirmar_consulta'),
    path('api/medico/consultas/cancelar/', ViewMedicoCancelaConsulta.as_view(), name='medico_cancelar_consulta'),
    path('api/paciente/login/', ViewPacienteLogin.as_view(), name='token_obter_paciente'),
    path('api/paciente/medicos/', ViewPacienteMedicos.as_view(), name='paciente_medicos'),
    path('api/paciente/medicos/agenda/', ViewPacienteAgendaMedico.as_view(), name='paciente_medico_agenda'),
    path('api/paciente/consultas/', ViewPacienteConsultas.as_view(), name='paciente_consultas'),
    path('api/paciente/consultas/solicitar/', ViewPacienteSolicitaConsulta.as_view(), name='paciente_solicita_consulta'),
    path('api/paciente/consultas/cancelar/', ViewPacienteCancelaConsulta.as_view(), name='paciente_cancela_consulta'),
]
