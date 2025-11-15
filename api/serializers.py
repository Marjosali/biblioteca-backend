from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book
from loans.models import Loan

User = get_user_model()

# ============================================================
# 🔹 SERIALIZER DE USUÁRIO
# ============================================================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email",
            "is_active", "is_staff", "is_superuser", "password"
        ]
        read_only_fields = ["is_staff", "is_superuser"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")

        if request is None or request.user.is_superuser:
            return rep
        elif request.user.is_staff:
            if instance.is_superuser:
                return None
            return rep
        else:
            if instance.id != request.user.id:
                return None
            rep.pop("is_staff", None)
            rep.pop("is_superuser", None)
            return rep


# ============================================================
# 🔹 SERIALIZER DE LIVROS
# ============================================================
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


# ============================================================
# 🔹 SERIALIZER DE EMPRÉSTIMOS (SIMPLIFICADO)
# ============================================================
class LoanSerializer(serializers.ModelSerializer):
    # Campos simplificados para exibição
    user_name = serializers.CharField(source="user.username", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    # Campos para criação
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = Loan
        fields = [
            "id",
            "user_name", "book_title",  # Apenas nomes no retorno
            "user_id", "book_id",       # IDs para criação
            "borrowed_at", "returned", "returned_at"
        ]
        read_only_fields = ["borrowed_at", "returned_at"]