import os
from django.core.wsgi import get_wsgi_application

# Configuração da variável de ambiente com o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')

# Criação da aplicação WSGI que será usada pelo servidor
application = get_wsgi_application()
