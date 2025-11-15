from django.contrib import admin
from django.utils.html import format_html
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para o modelo Book.
    Permite gerenciar o catálogo de livros de forma eficiente.
    """

    # Campos exibidos na listagem do admin
    list_display = ('title', 'author', 'genre', 'publication_year', 'available', 'cover_thumbnail')

    # Campos pesquisáveis
    search_fields = ('title', 'author', 'genre')

    # Filtros laterais
    list_filter = ('available', 'genre', 'publication_year')

    # Ordenação padrão
    ordering = ('title',)

    # Campos das seções do formulário de edição
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('title', 'author', 'genre', 'description', 'publication_year'),
        }),
        ('Disponibilidade e Capa', {
            'fields': ('available', 'cover_image'),
        }),
    )

    # Paginação
    list_per_page = 20

    # Miniatura da capa
    @admin.display(description="Capa")
    def cover_thumbnail(self, obj):
        """Exibe uma miniatura da capa do livro no admin."""
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="75" style="object-fit:cover;"/>', obj.cover_image.url)
        return "Sem capa"

    # Ajuste do queryset (exemplo se houver relacionamentos)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
