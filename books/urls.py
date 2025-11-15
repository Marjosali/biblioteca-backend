from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LoanViewSet

# 🔹 Roteador DRF — registra os endpoints principais para 'books' e 'loans'
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    # 🌐 Endpoints principais da API de livros e empréstimos
    path('', include(router.urls)),  # Inclui todos os endpoints do roteador
]

# ✅ Observações:
# - GET  /api/books/          → lista todos os livros
# - POST /api/books/          → cria um livro (somente admin)
# - GET  /api/loans/          → lista empréstimos (usuário vê apenas os seus)
# - POST /api/loans/          → cria novo empréstimo
# - PATCH /api/loans/<id>/    → marca devolução (returned = true)
