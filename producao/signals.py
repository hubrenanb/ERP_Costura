from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemComanda

@receiver(post_save, sender=ItemComanda)
@receiver(post_delete, sender=ItemComanda)
def recalcular_total_comanda(sender, instance, **kwargs):
    instance.comanda.atualizar_total()