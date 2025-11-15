from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Book(models.Model):
    """
    Modelo que representa um livro no catálogo.
    Inclui informações completas de identificação, capa e status.
    """

    class Genre(models.TextChoices):
        ROMANCE = 'Romance', _('Romance')
        AVENTURA = 'Aventura', _('Aventura')
        TERROR = 'Terror', _('Terror')
        FANTASIA = 'Fantasia', _('Fantasia')
        HISTORIA = 'História', _('História')
        BIOGRAFIA = 'Biografia', _('Biografia')
        OUTROS = 'Outros', _('Outros')

    title = models.CharField(
        max_length=200,
        verbose_name=_("Título"),
        help_text=_("Título completo do livro.")
    )
    author = models.CharField(
        max_length=200,
        verbose_name=_("Autor"),
        help_text=_("Nome do autor ou autores do livro.")
    )
    genre = models.CharField(
        max_length=100,
        choices=Genre.choices,
        blank=True,
        null=True,
        verbose_name=_("Gênero"),
        help_text=_("Selecione o gênero literário.")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Descrição"),
        help_text=_("Breve resumo ou sinopse do livro.")
    )
    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Ano de Publicação"),
        help_text=_("Ano em que o livro foi publicado.")
    )
    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        verbose_name=_("Capa do Livro"),
        help_text=_("Imagem da capa do livro (formato JPG ou PNG).")
    )
    available = models.BooleanField(
        default=True,
        verbose_name=_("Disponível"),
        help_text=_("Indica se o livro está disponível para empréstimo.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data de Cadastro")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última Atualização")
    )

    class Meta:
        verbose_name = _("📘 Livro")
        verbose_name_plural = _("📚 Livros")
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_book_by_author"
            )
        ]

    def clean(self):
        """Validações adicionais antes de salvar."""
        if self.publication_year and (self.publication_year < 1400 or self.publication_year > 2100):
            raise ValidationError({"publication_year": _("Ano de publicação inválido.")})

    def __str__(self):
        """Representação legível do livro."""
        status = _("Disponível") if self.available else _("Emprestado")
        return f"{self.title} — {status}"
