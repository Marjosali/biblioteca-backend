from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Book
from .serializers import BookSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de livros no catálogo.

    - Qualquer usuário pode visualizar livros.
    - Apenas administradores podem criar, editar ou remover livros.
    """
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer

    # Permite upload de capa via frontend
    parser_classes = [MultiPartParser, FormParser]

    # Filtros opcionais para listagem
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'author', 'publication_year']

    def get_permissions(self):
        """
        Define permissões baseadas na ação:
        - Leitura (list/retrieve): acesso livre
        - Escrita (create/update/delete): apenas admin
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
