from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from hackathon.usecases import agenda_usecases, consulta_usecases
from .serializers import (
    SerializerRemoveHorarios,
    SerializerTokenPaciente,
    SerializerTokenMedico,
    SerializerAddHorarios,
    SerializerConfirmaConsulta,
    SerializerCancelaConsulta,
    SerializerBuscaMedicos,
    SerializerBuscaAgendaMedico,
    SerializerSolicitaConsulta
)
from .permissions import PermissaoMedico, PermissaoPaciente


class ViewMedicoLogin(TokenObtainPairView):
    serializer_class = SerializerTokenMedico


class PingView(APIView):
    def get(self, request):
        return Response({"message": "pong"})


class ViewMedicoAddHorarioAgenda(APIView):
    permission_classes = [PermissaoMedico]

    def post(self, request):
        serializer = SerializerAddHorarios(data=request.data)
        try:
            if serializer.is_valid():
                agenda_usecases.add_horarios_agenda(medico=request.user, horarios=serializer.validated_data["horarios"])
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewMedicoRemoveHorarioAgenda(APIView):
    permission_classes = [PermissaoMedico]

    def delete(self, request):
        serializer = SerializerRemoveHorarios(data=request.data)
        try:
            if serializer.is_valid():
                agenda_usecases.remove_horarios_agenda(medico=request.user, horarios_ids=serializer.validated_data["horarios_ids"])
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewMedicoConsultas(APIView):
    permission_classes = [PermissaoMedico]

    def get(self, request):
        try:
            dados = consulta_usecases.get_consultas_medico(medico=request.user)
            return Response(dados, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewMedicoConfirmaConsulta(APIView):
    permission_classes = [PermissaoMedico]

    def post(self, request):
        serializer = SerializerConfirmaConsulta(data=request.data)
        try:
            if serializer.is_valid():
                consulta_usecases.confirma_consulta_medico(medico=request.user, consulta_id=serializer.validated_data["consulta_id"])
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewMedicoCancelaConsulta(APIView):
    permission_classes = [PermissaoMedico]

    def post(self, request):
        serializer = SerializerCancelaConsulta(data=request.data)
        try:
            if serializer.is_valid():
                consulta_usecases.cancela_consulta_medico(
                    medico=request.user,
                    consulta_id=serializer.validated_data["consulta_id"],
                    justificativa=serializer.validated_data["justificativa"]
                )
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as value_error:
            return Response({"error": str(value_error)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewPacienteLogin(TokenObtainPairView):
    serializer_class = SerializerTokenPaciente


class ViewPacienteMedicos(APIView):
    permission_classes = [PermissaoPaciente]

    def get(self, request):
        serializer = SerializerBuscaMedicos(data=request.data)
        try:
            if serializer.is_valid():
                dados = consulta_usecases.get_medicos(
                    especialidade=serializer.validated_data["especialidade"],
                    km_maximo=serializer.validated_data["km_maximo"],
                    latitude=serializer.validated_data["latitude"],
                    longitude=serializer.validated_data["longitude"],
                )
                return Response(dados, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewPacienteAgendaMedico(APIView):
    permission_classes = [PermissaoPaciente]

    def get(self, request):
        serializer = SerializerBuscaAgendaMedico(data=request.query_params)
        try:
            if serializer.is_valid():
                dados = agenda_usecases.get_agenda_medico(medico_id=serializer.validated_data["medico_id"])
                return Response(dados, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewPacienteSolicitaConsulta(APIView):
    permission_classes = [PermissaoPaciente]

    def post(self, request):
        serializer = SerializerSolicitaConsulta(data=request.data)
        try:
            if serializer.is_valid():
                consulta_usecases.solicita_consulta(
                    paciente=request.user,
                    medico_id=serializer.validated_data["medico_id"],
                    horario_agenda_id=serializer.validated_data["horario_agenda_id"]
                )
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as value_error:
            return Response({"error": str(value_error)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ViewPacienteCancelaConsulta(APIView):
    permission_classes = [PermissaoPaciente]

    def post(self, request):
        serializer = SerializerCancelaConsulta(data=request.data)
        try:
            if serializer.is_valid():
                consulta_usecases.cancela_consulta_paciente(
                    paciente=request.user,
                    consulta_id=serializer.validated_data["consulta_id"],
                    justificativa=serializer.validated_data["justificativa"]
                )
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as value_error:
            return Response({"error": str(value_error)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewPacienteConsultas(APIView):
    permission_classes = [PermissaoPaciente]

    def get(self, request):
        try:
            dados = consulta_usecases.get_consultas_paciente(paciente=request.user)
            return Response(dados, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "erro interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
