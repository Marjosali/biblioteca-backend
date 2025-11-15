from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from books.models import Book


class Loan(models.Model):
    """
    Modelo que representa um empréstimo de livro.
    Cada empréstimo está vinculado a um usuário e a um livro.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name='Usuário'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name='Livro'
    )
    borrowed_at = models.DateTimeField(auto_now_add=True, verbose_name='Data do Empréstimo')
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name='Data da Devolução')
    returned = models.BooleanField(default=False, verbose_name='Devolvido')

    turma = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Turma',
        help_text='Turma do aluno (opcional)'
    )

    class Meta:
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"
        ordering = ['-borrowed_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=models.Q(returned=False),
                name='unique_active_loan'
            )
        ]

    def clean(self):
        """Validação: impede empréstimo duplicado de livro ainda não devolvido."""
        if not self.returned and Loan.objects.filter(book=self.book, returned=False).exclude(pk=self.pk).exists():
            raise ValidationError("❌ Este livro já está emprestado e ainda não foi devolvido.")

    def save(self, *args, **kwargs):
        """
        Atualiza automaticamente:
        - Disponibilidade do livro
        - Data de devolução
        """
        self.clean()

        if self.returned:
            if not self.returned_at:
                self.returned_at = timezone.now()
            self.book.available = True
        else:
            self.book.available = False
            self.returned_at = None

        # Salva o livro antes do empréstimo
        self.book.save(update_fields=['available'])
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Devolvido" if self.returned else "Emprestado"
        turma_info = f" - {self.turma}" if self.turma else ""
        return f"{self.book.title} - {self.user.username}{turma_info} ({status})"