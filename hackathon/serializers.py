from datetime import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from pydantic import BaseModel

from hackathon.models import PerfilUsuario

class SerializerTokenPaciente(TokenObtainPairSerializer):
    cpf = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    username_field = "cpf"

    def validate(self, attrs):
        cpf = attrs.get('cpf')
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            perfil = PerfilUsuario.objects.get(cpf=cpf, email=email, tipo_usuario='Paciente')
            usuario = authenticate(username=perfil.usuario.username, password=password)
            if usuario is None:
                raise serializers.ValidationError('Credenciais inválidas')
        except PerfilUsuario.DoesNotExist:
            raise serializers.ValidationError('Credenciais inválidas')

        refresh = self.get_token(usuario)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class SerializerTokenMedico(TokenObtainPairSerializer):
    crm = serializers.CharField()
    password = serializers.CharField(write_only=True)
    username_field = "crm"

    def validate(self, attrs):
        crm = attrs.get('crm')
        password = attrs.get('password')

        try:
            perfil = PerfilUsuario.objects.get(crm=crm, tipo_usuario='Medico')
            usuario = authenticate(username=perfil.usuario.username, password=password)
            if usuario is None:
                raise serializers.ValidationError('Credenciais inválidas')
        except PerfilUsuario.DoesNotExist:
            raise serializers.ValidationError('Credenciais inválidas')

        refresh = self.get_token(usuario)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

class ModelHorario(serializers.Serializer):
    data_hora_inicio = serializers.DateTimeField()
    duracao = serializers.IntegerField()


class SerializerAddHorarios(serializers.Serializer):
    horarios = serializers.ListField(child=ModelHorario())


class SerializerRemoveHorarios(serializers.Serializer):
    horarios_ids = serializers.ListField(child=serializers.IntegerField())


class SerializerConfirmaConsulta(serializers.Serializer):
    consulta_id = serializers.IntegerField()


class SerializerCancelaConsulta(serializers.Serializer):
    consulta_id = serializers.IntegerField()
    justificativa = serializers.CharField()


class SerializerBuscaMedicos(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=7, decimal_places=5, required=False, default=None)
    longitude = serializers.DecimalField(max_digits=7, decimal_places=5, required=False, default=None)
    km_maximo = serializers.IntegerField(required=False, default=None)
    especialidade = serializers.CharField(required=False, default=None)
    
    def validate(self, data):
        km_maximo = data.get('km_maximo')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if km_maximo is not None:
            if latitude is None or longitude is None:
                raise serializers.ValidationError(
                    "Latitude e longitude são obrigatórias quando km_maximo é fornecido."
                )

        return data


class SerializerBuscaAgendaMedico(serializers.Serializer):
    medico_id = serializers.IntegerField()


class SerializerSolicitaConsulta(serializers.Serializer):
    medico_id = serializers.IntegerField()
    horario_agenda_id = serializers.IntegerField()
