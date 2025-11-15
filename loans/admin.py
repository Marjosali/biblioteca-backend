from django.contrib import admin, messages
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """
    Configuração do painel administrativo para empréstimos de livros.
    Permite visualizar, filtrar e marcar devoluções diretamente do admin.
    """

    list_display = (
        'book',
        'user',
        'turma',
        'borrowed_at',
        'returned_at',
        'returned',
    )
    list_filter = (
        'returned',
        'borrowed_at',
        'turma',
    )
    search_fields = (
        'book__title',
        'user__username',
        'turma',
    )
    ordering = ['-borrowed_at']
    actions = ['marcar_como_devolvido']

    @admin.action(description="📚 Marcar como devolvido")
    def marcar_como_devolvido(self, request, queryset):
        """
        Ação personalizada para marcar empréstimos selecionados como devolvidos.
        Usa a lógica do modelo para atualizar disponibilidade e data.
        """
        updated = 0
        errors = 0

        for loan in queryset:
            if not loan.returned:
                try:
                    loan.returned = True
                    loan.save()  # Lógica completa no modelo (returned_at + disponibilidade)
                    updated += 1
                except Exception as e:
                    errors += 1
                    self.message_user(
                        request,
                        f"⚠️ Erro ao atualizar empréstimo de '{loan.book.title}': {e}",
                        level=messages.ERROR
                    )

        if updated:
            self.message_user(
                request,
                f"✅ {updated} empréstimo(s) marcado(s) como devolvido(s).",
                level=messages.SUCCESS
            )

        if errors:
            self.message_user(
                request,
                f"⚠️ {errors} empréstimo(s) não puderam ser atualizados.",
                level=messages.WARNING
            )

    def get_readonly_fields(self, request, obj=None):
        """
        Impede que usuários comuns alterem diretamente campos críticos.
        """
        if not request.user.is_superuser:
            return ['user', 'borrowed_at']
        return super().get_readonly_fields(request, obj)