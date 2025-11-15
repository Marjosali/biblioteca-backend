from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = "📚 Catálogo de Livros"

    def ready(self):
        """
        Executado quando o app é carregado.
        Ideal para conectar sinais ou inicializar rotinas específicas.
        """
        try:
            import catalog.signals  # Importa sinais do app (se existirem)
            logger.info("✅ Sinais do app 'catalog' carregados com sucesso.")
        except ImportError:
            logger.warning("⚠️ Nenhum módulo 'catalog.signals' encontrado — inicialização padrão.")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar sinais do app 'catalog': {e}")
