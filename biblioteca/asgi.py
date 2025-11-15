import os
from django.core.asgi import get_asgi_application

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')

# Cria a aplicação ASGI
application = get_asgi_application()
