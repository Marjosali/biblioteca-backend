from django.contrib import admin
from django.utils.html import format_html
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    🔹 Painel administrativo para gerenciamento de livros.
    Permite marcar livros como disponíveis ou emprestados,
    além de visualizar miniaturas das capas.
    """

    # Campos mostrados na listagem
    list_display = ('title', 'author', 'genre', 'publication_year', 'available', 'capa_preview')

    # Campos de busca
    search_fields = ('title', 'author', 'genre')

    # Filtros laterais
    list_filter = ('available', 'genre', 'publication_year')

    # Edição rápida de disponibilidade
    list_editable = ('available',)

    # Ordenação padrão
    ordering = ('title',)

    # Campos somente leitura no formulário de edição
    readonly_fields = ('capa_preview',)

    # Ações personalizadas
    actions = ['marcar_como_disponivel', 'marcar_como_emprestado']

    @admin.display(description="📘 Capa")
    def capa_preview(self, obj):
        """Mostra miniatura da capa do livro na listagem e formulário."""
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="60" height="90" '
                'style="object-fit:cover; border-radius:4px; box-shadow:0 0 4px rgba(0,0,0,0.3);" alt="Capa do livro"/>',
                obj.cover_image.url
            )
        return format_html('<span style="color: #999;">Sem capa</span>')

    @admin.action(description="✅ Marcar como disponível")
    def marcar_como_disponivel(self, request, queryset):
        """Marca os livros selecionados como disponíveis."""
        updated = queryset.update(available=True)
        if updated:
            self.message_user(request, f"✅ {updated} livro(s) marcado(s) como disponível(is).")
        else:
            self.message_user(request, "Nenhum livro foi atualizado.", level="warning")

    @admin.action(description="🚫 Marcar como emprestado")
    def marcar_como_emprestado(self, request, queryset):
        """Marca os livros selecionados como emprestados."""
        updated = queryset.update(available=False)
        if updated:
            self.message_user(request, f"🚫 {updated} livro(s) marcado(s) como emprestado(s).")
        else:
            self.message_user(request, "Nenhum livro foi atualizado.", level="warning")
