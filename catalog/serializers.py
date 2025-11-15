from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer do modelo Book.
    Inclui validações automáticas e exibe status de disponibilidade de forma legível.
    """

    status_display = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y %H:%M")

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'description',
            'publication_year',
            'cover_image',
            'available',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status_display', 'created_at', 'updated_at']

    def get_status_display(self, obj):
        """Retorna uma descrição legível do status de disponibilidade."""
        return "Disponível" if obj.available else "Indisponível"

    def validate_publication_year(self, value):
        """Valida se o ano de publicação é coerente (não no futuro)."""
        from datetime import date
        current_year = date.today().year
        if value and (value < 1000 or value > current_year):
            raise serializers.ValidationError(
                f"Ano de publicação inválido. Deve estar entre 1000 e {current_year}."
            )
        return value

    def validate_cover_image(self, value):
        """Valida a imagem da capa, garantindo formato e tamanho adequado."""
        if value:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                raise serializers.ValidationError("Formato de imagem inválido. Utilize JPG ou PNG.")

            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError("A imagem da capa não pode ser maior que 5MB.")
        return value
