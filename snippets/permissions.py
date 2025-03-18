from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Personalizar permissao para permitir apenas owners de um objeto editar-los.
    '''
    def has_object_permission(self, request, view, obj):
        # permissões de leitura sao permitidas para qualquer solicitação,
        # entao sempre permitiremos solicitacos GET HEAD ou OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissoes de gravacao sao concedidas somente ao proprietario do snippet
        return obj.owner == request.user
        
    