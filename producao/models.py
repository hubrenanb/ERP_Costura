from decimal import Decimal
from django.db import models
from django.db.models import Sum, F
from core.models import Cliente, Empresa

class Comanda(models.Model):
    STATUS_CHOICES = (
        ('recebido', 'Recebido'),
        ('em_analise', 'Em Análise'),
        ('em_costura', 'Em Costura'),
        ('ajuste_final', 'Ajuste Final'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebido')
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_entrega_prevista = models.DateField()
    data_entrega_real = models.DateField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Comanda"
        verbose_name_plural = "Comandas"
        ordering = ['-data_entrada']

    def __str__(self):
        return f"Comanda {self.id} - {self.cliente.nome_completo}"

    def atualizar_total(self):
        """
        Recalcula o valor total da comanda somando (quantidade * preco_unitario) de cada item.
        Chamado via signals sempre que um ItemComanda é alterado.
        """
        resultado = self.itens.aggregate(
            total=Sum(F('quantidade') * F('preco_unitario'), output_field=models.DecimalField())
        )
        self.valor_total = resultado['total'] or Decimal('0.00')
        # update_fields evita que o save() dispare signals desnecessários em outros campos
        self.save(update_fields=['valor_total'])

    @property
    def saldo_devedor(self):
        """
        Calcula o saldo devedor cruzando com o modelo Transacao do app financeiro.
        Certifique-se que o model Transacao tenha related_name='pagamentos'.
        """
        try:
            # Filtra apenas as receitas vinculadas a esta comanda
            recebidos = self.pagamentos.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            return self.valor_total - recebidos
        except AttributeError:
            # Fallback caso o related_name ainda não esteja configurado no financeiro
            return self.valor_total

class ItemComanda(models.Model):
    # related_name='itens' permite que a Comanda acesse os itens via self.itens
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='itens')
    descricao_servico = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descricao_servico} ({self.quantidade}x)"