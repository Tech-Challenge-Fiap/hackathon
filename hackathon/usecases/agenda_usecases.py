from datetime import datetime, timedelta
from hackathon.models import Agenda, Consulta, PerfilUsuario

def add_horarios_agenda(medico, horarios):
    medico = PerfilUsuario.objects.get(usuario=medico, tipo_usuario='Medico')
    horarios_validos = []

    # Pré-carregar todas as agendas existentes do médico que não foram deletadas
    agendas_existentes = Agenda.objects.filter(medico=medico, deleted=False)
    
    for horario in horarios:
        data_hora_inicio = horario['data_hora_inicio']
        duracao = horario['duracao']
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao)
        
        # Verificar sobreposição de horários em memória
        sobreposicoes = [
            agenda for agenda in agendas_existentes
            if not (agenda.data_hora_inicio >= data_hora_fim or (agenda.data_hora_inicio + timedelta(minutes=agenda.duracao)) <= data_hora_inicio)
        ]
        
        if sobreposicoes:
            raise ValueError(f"Há uma sobreposição de horários para o horário {data_hora_inicio}")
        
        horarios_validos.append(
            Agenda(
                medico=medico,
                data_hora_inicio=data_hora_inicio,
                duracao=duracao,
                valor_consulta=horario.get('valor_consulta', 0),
                deleted=False
            )
        )
    
    # Criação em bulk
    Agenda.objects.bulk_create(horarios_validos)


def remove_horarios_agenda(medico, horarios_ids):
    medico = PerfilUsuario.objects.get(usuario=medico, tipo_usuario='Medico')
    agendas = Agenda.objects.filter(medico=medico, id__in=horarios_ids, deleted=False)

    # Pré-carregar consultas confirmadas relacionadas a essas agendas
    consultas_confirmadas = Consulta.objects.filter(agenda__in=agendas, status=Consulta.Status.CONFIRMADA)
    
    if consultas_confirmadas.exists():
        raise ValueError("Não é possível remover horários com consultas confirmadas.")
    
    # Marcar os horários como deletados
    agendas.update(deleted=True)


def get_agenda_medico(medico_id):
    agenda = Agenda.objects.filter(medico_id=medico_id, deleted=False).order_by('data_hora_inicio')
    return [
        {
            'id': item.id,
            'data_hora_inicio': item.data_hora_inicio,
            'duracao': item.duracao,
            'valor_consulta': item.valor_consulta,
        } for item in agenda
    ]
