from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Book
from loans.models import Loan
from .serializers import BookSerializer
from loans.serializers import LoanSerializer

User = get_user_model()

# =======================================
# BOOKS
# =======================================
class BookViewSet(viewsets.ModelViewSet):
    """
    Controla CRUD de livros.
    - Qualquer usuário pode visualizar.
    - Apenas admin pode criar/editar/excluir.
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # ✅ Suporte para upload de imagem

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()