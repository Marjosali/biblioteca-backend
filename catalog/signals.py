from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import os

from .models import Book


@receiver(post_save, sender=Book)
def log_book_changes(sender, instance, created, **kwargs):
    """Loga quando um livro é criado ou atualizado."""
    if created:
        print(f"✅ Novo livro cadastrado: {instance.title} ({instance.author})")
    else:
        print(f"✏️ Livro atualizado: {instance.title}")


@receiver(pre_save, sender=Book)
def notify_unavailable(sender, instance, **kwargs):
    """
    Envia notificação quando um livro fica indisponível.
    Só dispara se antes estava disponível e agora não.
    """
    if instance.pk:  # Só para updates
        old_instance = Book.objects.get(pk=instance.pk)
        if old_instance.available and not instance.available:
            # Exemplo simples: enviar e-mail (requer configuração de SMTP)
            send_mail(
                subject="Livro indisponível",
                message=f"O livro '{instance.title}' agora está indisponível.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["admin@biblioteca.com"],
                fail_silently=True,
            )
            print(f"📢 Notificação: {instance.title} ficou indisponível.")


@receiver(pre_delete, sender=Book)
def delete_cover_image(sender, instance, **kwargs):
    """Remove a imagem da capa do sistema ao excluir o livro."""
    if instance.cover_image and os.path.isfile(instance.cover_image.path):
        os.remove(instance.cover_image.path)
        print(f"🗑️ Capa removida: {instance.cover_image.path}")