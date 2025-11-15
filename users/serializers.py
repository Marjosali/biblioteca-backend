from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo de Usuário.
    ✅ Cria usuários com senha criptografada.
    ✅ Impede que usuários comuns concedam privilégios.
    ✅ Compatível com JWT e React (retorna flags de acesso).
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="Informe um endereço de e-mail válido e único."
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="A senha deve atender aos critérios de segurança do sistema."
    )

    full_role = serializers.ReadOnlyField(help_text="Função do usuário (Superusuário, Administrador ou Comum)")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_admin",
            "full_role",
        ]
        read_only_fields = ["id", "full_role"]

    # 🔹 Criação segura de usuário
    def create(self, validated_data):
        request = self.context.get("request")

        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            is_active=validated_data.get("is_active", True),
        )

        # 🔒 Controle de privilégios
        if request and getattr(request.user, "is_staff", False):
            user.is_staff = validated_data.get("is_staff", False)
            user.is_superuser = validated_data.get("is_superuser", False)
            user.is_admin = validated_data.get("is_admin", False)
        else:
            # Usuário comum nunca pode se autoconceder permissões
            user.is_staff = False
            user.is_superuser = False
            user.is_admin = False

        # 🔐 Criptografa a senha antes de salvar
        user.set_password(validated_data["password"])
        user.save()
        return user

    # 🔹 Atualização segura de usuário
    def update(self, instance, validated_data):
        request = self.context.get("request")

        # Atualiza senha, se enviada
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        # Controle de privilégios
        for attr, value in validated_data.items():
            if attr in ["is_staff", "is_superuser", "is_admin"]:
                if request and getattr(request.user, "is_staff", False):
                    setattr(instance, attr, value)
                else:
                    raise PermissionDenied("❌ Você não tem permissão para alterar privilégios de administrador.")
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    # 🔹 Exibição formatada para o frontend (React)
    def to_representation(self, instance):
        """
        Garante que todos os campos de status e papéis sejam sempre retornados.
        """
        data = super().to_representation(instance)
        data["is_admin"] = getattr(instance, "is_admin", instance.is_staff or instance.is_superuser)
        data["full_role"] = getattr(instance, "full_role", "Usuário comum")
        return data
