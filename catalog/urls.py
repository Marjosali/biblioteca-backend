from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# 🔹 Roteador DRF — CRUD completo de livros
router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')  # raiz do app será /api/catalog/

urlpatterns = [
    path('', include(router.urls)),
]

"""
📚 Endpoints disponíveis — prefixo: /api/catalog/

🔹 Livros (BookViewSet)
    GET     /api/catalog/           → lista todos os livros
    POST    /api/catalog/           → cria novo livro (admin)
    GET     /api/catalog/{id}/      → detalhes de um livro
    PUT     /api/catalog/{id}/      → atualiza livro (admin)
    PATCH   /api/catalog/{id}/      → atualização parcial
    DELETE  /api/catalog/{id}/      → remove livro (admin)
"""
