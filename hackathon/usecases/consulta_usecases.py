from math import radians, sin, cos, sqrt, atan2
from hackathon.models import Consulta, PerfilUsuario, Agenda


class EdicaoNaoAutorizada(Exception):
    pass


def solicita_consulta(paciente, medico_id, horario_agenda_id):
    paciente = PerfilUsuario.objects.get(usuario=paciente, tipo_usuario='Paciente')
    try:
        agenda = Agenda.objects.get(id=horario_agenda_id, medico_id=medico_id, deleted=False)
    except Agenda.DoesNotExist:
        raise ValueError("Horario não permitido para agendamento")
    
    if agenda.consulta_set.filter(
        status__in=(Consulta.Status.CONFIRMADA, Consulta.Status.PENDENTE)
    ).exists():
        raise ValueError("Horario já possui consulta marcada")

    Consulta.objects.create(
        medico_id=medico_id,
        paciente=paciente,
        agenda=agenda,
        status=Consulta.Status.PENDENTE
    )


def confirma_consulta_medico(medico, consulta_id):
    consulta = Consulta.objects.filter(id=consulta_id, medico__usuario=medico).first()
    if not consulta:
        raise EdicaoNaoAutorizada
    consulta.status = Consulta.Status.CONFIRMADA
    consulta.save()


def cancela_consulta_medico(medico, consulta_id, justificativa):
    consulta = Consulta.objects.filter(id=consulta_id, medico__usuario=medico).first()
    if not consulta:
        raise EdicaoNaoAutorizada
    consulta.status = Consulta.Status.CANCELADA
    consulta.justificativa_cancelamento = justificativa
    consulta.save()


def cancela_consulta_paciente(paciente, consulta_id, justificativa):
    consulta = Consulta.objects.filter(id=consulta_id, paciente__usuario=paciente).first()
    if not consulta:
        raise EdicaoNaoAutorizada
    consulta.status = Consulta.Status.CANCELADA
    consulta.justificativa_cancelamento = justificativa
    consulta.save()


def get_consultas_medico(medico):
    consultas = Consulta.objects.filter(medico__usuario=medico).order_by('agenda__data_hora_inicio')
    return [
        {
            'id': consulta.id,
            'paciente': consulta.paciente.nome,
            'data_hora_inicio': consulta.agenda.data_hora_inicio,
            'status': consulta.status,
        } for consulta in consultas
    ]


def get_consultas_paciente(paciente):
    consultas = Consulta.objects.filter(paciente__usuario=paciente).order_by('agenda__data_hora_inicio')
    return [
        {
            'id': consulta.id,
            'medico': consulta.medico.nome,
            'data_hora_inicio': consulta.agenda.data_hora_inicio,
            'status': consulta.status,
        } for consulta in consultas
    ]


def _calcular_distancia(lat1, lon1, lat2, lon2):
    # Raio da Terra em quilômetros
    R = 6371.0
    
    # Converter graus para radianos
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    # Diferença de coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = R * c
    
    return distancia

def get_medicos(especialidade=None, km_maximo=None, latitude=None, longitude=None):
    medicos = PerfilUsuario.objects.filter(tipo_usuario='Medico')
    
    if especialidade:
        medicos = medicos.filter(especialidades__contains=[especialidade])
    
    if latitude is not None and longitude is not None and km_maximo is not None:
        medicos_com_distancia = []
        
        for medico in medicos:
            if medico.clinica:
                clinica_lat = medico.clinica.latitude
                clinica_lon = medico.clinica.longitude
                distancia = _calcular_distancia(latitude, longitude, clinica_lat, clinica_lon)
                
                if distancia <= km_maximo:
                    medicos_com_distancia.append(medico)
        
        medicos = medicos_com_distancia

    return [
        {
            'id': medico.id,
            'nome': medico.nome,
            'especialidades': medico.especialidades,
            'clinica': medico.clinica.nome if medico.clinica else None,
        } for medico in medicos
    ]
