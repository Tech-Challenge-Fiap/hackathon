from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Clinica(models.Model):
    nome = models.TextField()
    endereco = models.TextField()
    longitude = models.DecimalField(decimal_places=5, max_digits=7)
    latitude = models.DecimalField(decimal_places=5, max_digits=7)


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=[('Paciente', 'Paciente'), ('Medico', 'Medico')])
    email = models.EmailField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    crm = models.CharField(max_length=20, blank=True, null=True)
    especialidades = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    clinica = models.ForeignKey(Clinica, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.usuario.username


class Agenda(models.Model):
    medico = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField()
    valor_consulta = models.DecimalField(decimal_places=2, max_digits=5)
    duracao = models.IntegerField()
    deleted = models.BooleanField(default=False)


class Consulta(models.Model):
    class Status(models.TextChoices):
        CONFIRMADA = "confirmada"
        CANCELADA = "cancelada"
        PENDENTE = "pendente"

    medico = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name="medico")
    paciente = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name="paciente")
    agenda = models.ForeignKey(Agenda, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=Status.choices, null=True, blank=True, default=Status.PENDENTE)
    justificativa_cancelamento = models.TextField(null=True, blank=True)
