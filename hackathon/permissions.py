from rest_framework.permissions import BasePermission

class PermissaoMedico(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.perfilusuario.tipo_usuario == 'Medico'

class PermissaoPaciente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.perfilusuario.tipo_usuario == 'Paciente'
