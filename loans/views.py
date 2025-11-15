# =======================================
# LOANS
# =======================================
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from loans.models import Loan
from .serializers import LoanSerializer

User = get_user_model()


class LoanViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar empréstimos.
    - Admin/Superuser podem criar e devolver.
    - Usuário comum só visualiza seus empréstimos.
    """

    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Loan.objects.select_related("book", "user")
        return qs.order_by("-borrowed_at") if user.is_staff or user.is_superuser else qs.filter(user=user)

    # =======================================
    # CREATE (EMPRÉSTIMO)
    # =======================================
    def perform_create(self, serializer):
        request = self.request
        if not (request.user.is_staff or request.user.is_superuser):
            raise ValidationError("🚫 Apenas administradores podem registrar empréstimos.")

        user_id = self.request.data.get("user_id")
        if not user_id:
            raise ValidationError("⚠️ Campo 'user_id' é obrigatório.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("Usuário informado não existe.")

        turma = self.request.data.get("turma")
        serializer.save(user=user, turma=turma)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "✅ Empréstimo criado com sucesso!", "loan": serializer.data}, status=status.HTTP_201_CREATED)

    # =======================================
    # UPDATE (DEVOLUÇÃO)
    # =======================================
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Se a requisição indica devolução, força o campo
        if request.data.get("action") == "devolver":
            request.data["returned"] = True

        serializer = self.get_serializer(instance, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()  # Lógica de devolução está no modelo
        except ValidationError as e:
            return Response({"message": str(e)}, status=400)

        return Response({"message": "✅ Empréstimo atualizado com sucesso!", "loan": serializer.data}, status=200)

    # =======================================
    # ENDPOINT CUSTOMIZADO PARA DEVOLUÇÃO
    # =======================================
    @action(detail=True, methods=["post"], url_path="devolver")
    def devolver(self, request, pk=None):
        loan = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"message": "🚫 Apenas administradores podem devolver."}, status=403)

        loan.returned = True
        loan.save()  # Atualiza disponibilidade e returned_at via modelo
        serializer = self.get_serializer(loan)
        return Response({"message": "✅ Livro devolvido!", "loan": serializer.data}, status=200)

    # =======================================
    # DELETE (SOMENTE ADMIN)
    # =======================================
    def destroy(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"message": "🚫 Apenas administradores podem excluir empréstimos."}, status=403)
        return super().destroy(request, *args, **kwargs)