from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MovimentacaoEstoque

@receiver(post_save, sender=MovimentacaoEstoque)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        if instance.tipo == 'entrada':
            produto.quantidade_atual += instance.quantidade
        elif instance.tipo == 'saida':
            produto.quantidade_atual -= instance.quantidade
        produto.save()