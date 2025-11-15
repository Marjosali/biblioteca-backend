from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Administração personalizada do modelo de usuários da biblioteca."""

    # 🔹 Campos exibidos na listagem de usuários
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
    )
    list_filter = ("is_active", "is_staff", "is_admin", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # 🔧 Organização dos campos dentro da página de edição
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Informações pessoais"), {"fields": ("first_name", "last_name", "email", "date_of_birth")}),
        (
            _("Permissões e Funções"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
    )

    # 🆕 Campos exibidos na página de criação de novo usuário
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                ),
            },
        ),
    )

    # ✅ Campos somente leitura
    readonly_fields = ("last_login", "date_joined")

    # 💡 Controle de permissões de edição
    def has_change_permission(self, request, obj=None):
        """
        Impede usuários não-superusuários de modificar superusuários.
        """
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Garante que a senha seja criptografada ao criar um novo usuário.
        """
        if not change and obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
