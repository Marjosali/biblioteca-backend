from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Modelo de Usuário personalizado para o sistema de biblioteca.
    - Adiciona campo `is_admin` para administradores internos.
    - Evita conflitos de relacionamento com os modelos padrão de grupos e permissões.
    """

    # 🔹 Campo adicional para distinguir administradores internos
    is_admin = models.BooleanField(
        default=False,
        help_text=_("Define se o usuário é um administrador interno do sistema."),
        verbose_name=_("Administrador interno"),
    )

    # 🔹 Corrige conflitos com relacionamentos padrão do AbstractUser
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text=_("Grupos aos quais este usuário pertence."),
        verbose_name=_("Grupos"),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text=_("Permissões específicas deste usuário."),
        verbose_name=_("Permissões de usuário"),
    )

    # 🔹 Campo adicional
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Data de nascimento"),
    )

    # 🔹 Campos de metadados e métodos utilitários
    def __str__(self):
        """Exibe o nome de usuário, ou o ID se o nome estiver ausente."""
        return self.username or f"Usuário {self.id}"

    @property
    def full_role(self):
        """
        Retorna uma string representando o tipo de usuário:
        - "Superusuário"
        - "Administrador"
        - "Usuário comum"
        """
        if self.is_superuser:
            return "Superusuário"
        elif self.is_staff or self.is_admin:
            return "Administrador"
        return "Usuário comum"

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        ordering = ["username"]
