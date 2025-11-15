from django.db import models
from django.conf import settings
from django.utils import timezone


class Book(models.Model):
    """
    Modelo que representa um livro no catálogo da biblioteca.
    Inclui informações bibliográficas, capa e status de disponibilidade.
    """

    GENRE_CHOICES = [
        ('ficcao', 'Ficção'),
        ('nao_ficcao', 'Não Ficção'),
        ('infantil', 'Infantil'),
        ('tecnico', 'Técnico'),
        ('outro', 'Outro'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=200, verbose_name="Autor")
    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        default='outro',
        verbose_name="Gênero"
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Ano de Publicação"
    )
    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        verbose_name="Capa do Livro"
    )
    available = models.BooleanField(default=True, verbose_name="Disponível")
    
    # Data de criação e última atualização
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ["title"]

    def __str__(self):
        status = "Disponível ✅" if self.available else "Emprestado ❌"
        return f"{self.title} — {status}"

    def short_description(self):
        """
        Retorna um resumo da descrição (limite de 100 caracteres).
        """
        return self.description[:100] + '...' if len(self.description) > 100 else self.description

    def get_full_description(self):
        """
        Retorna a descrição completa do livro.
        """
        return self.description

    def save(self, *args, **kwargs):
        """
        Verifica se o ano de publicação é válido (não pode ser no futuro).
        """
        if self.publication_year and self.publication_year > timezone.now().year:
            raise ValueError("O ano de publicação não pode ser no futuro.")

        super().save(*args, **kwargs)

