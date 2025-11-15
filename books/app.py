from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    verbose_name = "📚 Catálogo de Livros"

    def ready(self):
        """
        Método executado automaticamente quando o app 'books' é carregado.
        Ideal para registrar sinais (signals), inicializações específicas ou 
        configurações adicionais para o app de livros.
        """
        try:
            # Registra sinais, como para sincronização de empréstimos ou atualizações automáticas.
            import books.signals  
        except ImportError:
            # Caso o módulo de sinais não exista, ignora o erro (útil durante o desenvolvimento inicial)
            pass
