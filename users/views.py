from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# =======================================
# Permissão: Admin ou Superusuário
# =======================================
class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Superusuário tem acesso total.
    Admin (is_staff=True) tem acesso, mas não vê superusuários.
    Usuário comum só vê o próprio perfil (/me).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        if view.action in ["retrieve", "me"]:
            return True

        return False


# =======================================
# ViewSet principal de usuários
# =======================================
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

        queryset = User.objects.all().order_by("username")

        if not user.is_superuser:
            queryset = queryset.filter(is_superuser=False)

        return queryset

    def create(self, request, *args, **kwargs):
        """Cria um novo usuário (apenas admin/superuser)."""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"detail": "❌ Somente administradores podem criar usuários."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Define a senha corretamente
        password = serializer.validated_data.get("password")
        if password:
            user.set_password(password)
        user.is_active = True
        user.save()

        return Response(
            {
                "message": "✅ Usuário criado com sucesso!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    # =======================================
    # Rota personalizada /api/users/me/
    # =======================================
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """Retorna dados do usuário autenticado"""
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
        }
        return Response(data, status=status.HTTP_200_OK)
