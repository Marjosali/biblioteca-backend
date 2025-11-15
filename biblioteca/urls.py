# biblioteca/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Painel de administração
    path('admin/', admin.site.urls),

    # 🔹 Endpoints de autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 Endpoints da API principal (pasta api)
    path('api/', include('api.urls')),  # conecta todos os ViewSets: users, livros, emprestimos

    # 🔹 Página inicial renderizando home.html (frontend)
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
]

# 🔹 Servir arquivos de mídia em DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
