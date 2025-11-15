from rest_framework import serializers
from .models import Loan
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class LoanSerializer(serializers.ModelSerializer):
    # Campos somente leitura
    book_title = serializers.ReadOnlyField(source="book.title")
    user_username = serializers.ReadOnlyField(source="user.username")

    # IDs para entrada
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True,
        required=False
    )

    turma = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "user_id",
            "user_username",
            "book_id",
            "book_title",
            "borrowed_at",
            "returned_at",
            "returned",
            "turma",
        ]
        read_only_fields = [
            "borrowed_at",
            "returned_at",
            "book_title",
            "user_username",
        ]

    # 🔥 Aceita userId / user_id / user e bookId / book_id / book
    def to_internal_value(self, data):
        data = data.copy()
        if "userId" in data:
            data["user_id"] = data.pop("userId")
        if "user" in data:
            data["user_id"] = data.pop("user")
        if "bookId" in data:
            data["book_id"] = data.pop("bookId")
        if "book" in data:
            data["book_id"] = data.pop("book")
        return super().to_internal_value(data)

    def validate(self, data):
        """Impede empréstimo duplicado."""
        book = data.get("book")
        if book and Loan.objects.filter(book=book, returned=False).exists():
            raise serializers.ValidationError({
                "book_id": "❌ Este livro já está emprestado e ainda não foi devolvido."
            })
        return data

    def create(self, validated_data):
        """Cria o empréstimo e atribui ao usuário correto."""
        request = self.context.get("request")
        user = validated_data.get("user")
        if not user and request and request.user.is_authenticated:
            validated_data["user"] = request.user
        loan = Loan.objects.create(**validated_data)
        return loan

    def update(self, instance, validated_data):
        """Atualiza devolução e turma."""
        instance.returned = validated_data.get("returned", instance.returned)
        if "turma" in validated_data:
            instance.turma = validated_data["turma"]
        instance.save()  # Lógica de disponibilidade e returned_at é tratada no modelo
        return instance