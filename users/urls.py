from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CurrentUserView

# 🔹 Router padrão DRF para operações CRUD de usuários
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # 🙋 Endpoint para obter o usuário autenticado
    path('users/me/', CurrentUserView.as_view(), name='current_user'),

    # ⚙️ Inclui todas as rotas automáticas do ViewSet (list, create, retrieve, etc.)
    path('', include(router.urls)),
]
