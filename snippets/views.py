from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.response import Response

from django.contrib.auth.models import User

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly

#CBV - class-based views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    essa viewset prove automaticamente as ações de list e retrieve
    """   
    queryset = User.objects.all()
    serializer_class = UserSerializer

    '''
    o método perfom_create nos permite modificar como o salvamento da instância é gerenciado 
    e manipular qualquer informação implícita na solicitação de entrada ou URL solicitada.
    Ou seja, ele manipula o snippet para pegar o user e associa-lo ao owner no banco de dados
    '''
    
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])  
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
         
    

