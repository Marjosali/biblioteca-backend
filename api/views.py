from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import transaction
from books.models import Book
from loans.models import Loan
from .serializers import UserSerializer, BookSerializer, LoanSerializer

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# ============================================================
# 🔹 TOKEN PERSONALIZADO
# ============================================================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ============================================================
# 🔹 PERMISSÃO CUSTOMIZADA
# ============================================================
class IsAdminOrSuperUser(permissions.BasePermission):
    """Permite acesso apenas a administradores e superusuários."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.is_active:
            return False
        if getattr(view, 'action', None) == 'me':
            return True
        return request.user.is_staff or request.user.is_superuser

# ============================================================
# 🔹 USERS
# ============================================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser]

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif user.is_staff:
            return User.objects.filter(is_superuser=False)
        return User.objects.filter(id=user.id)

# ============================================================
# 🔹 BOOKS
# ============================================================
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# ============================================================
# 🔹 LOANS
# ============================================================
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().select_related('book', 'user')
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Loan.objects.select_related('book', 'user')
        if user.is_staff or user.is_superuser:
            return qs.order_by('-borrowed_at')
        return qs.filter(user=user).order_by('-borrowed_at')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'devolver']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @transaction.atomic
    def perform_create(self, serializer):
        book = serializer.validated_data.get('book')
        if not book.available:
            raise ValidationError({"message": f"❌ O livro '{book.title}' não está disponível."})

        # ✅ Agora salva usando os dados enviados (user_id e book_id)
        loan = serializer.save()

        # Atualiza disponibilidade do livro
        book.available = False
        book.save(update_fields=['available'])

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'returned' in request.data and not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"message": "🚫 Apenas administradores podem registrar devoluções."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        loan = serializer.save()

        # ✅ Atualiza disponibilidade do livro
        loan.book.available = not loan.returned
        loan.book.save(update_fields=['available'])

        return Response(
            {"message": "✅ Empréstimo atualizado com sucesso!", "loan": serializer.data},
            status=status.HTTP_200_OK
        )

    # ✅ Endpoint customizado para devolução
    @action(detail=True, methods=["post"], url_path="devolver")
    @transaction.atomic
    def devolver(self, request, pk=None):
        loan = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"message": "🚫 Apenas administradores podem devolver."}, status=403)

        loan.returned = True
        loan.save()

        # ✅ Atualiza disponibilidade do livro
        loan.book.available = True
        loan.book.save(update_fields=['available'])

        serializer = self.get_serializer(loan)
        return Response({"message": "✅ Livro devolvido!", "loan": serializer.data}, status=200)
