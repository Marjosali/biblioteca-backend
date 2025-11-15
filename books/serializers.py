from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    # ✅ Garante que a URL completa da imagem seja retornada
    cover_image = serializers.ImageField(use_url=True)
    loans = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'description',
            'publication_year',
            'cover_image',   # ✅ Campo da capa com URL completa
            'available',
            'loans',
        ]

    def get_loans(self, obj):
        active_loans = obj.loans.filter(returned=False).order_by('-borrowed_at')
        return [
            {
                "loan_id": loan.id,
                "user_id": loan.user.id,
                "username": loan.user.username,
                "borrowed_at": loan.borrowed_at,
                "status": "Emprestado" if not loan.returned else "Devolvido",
                "returned_at": loan.returned_at if loan.returned else None,
            }
            for loan in active_loans
        ]