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

    ORIGEM_CHOICES = (
        ('san_marino', 'San Marino'),
        ('nossa_escola', 'Nossa Escola'),
        ('colegio_torres', 'Colégio Torres'),
        ('indicacao', 'Indicação'),
        ('avulso', 'Avulso'),
        ('google', 'Google'),
        ('instagram', 'Instagram'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebido')
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, null=True, blank=True)
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_entrega_prevista = models.DateField()
    data_entrega_real = models.DateField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Comanda"
        verbose_name_plural = "Comandas"
        ordering = ['-data_entrada']

    def __str__(self):
        return f"Comanda {self.id} - {self.cliente.nome_completo}"

    def atualizar_total(self):
        resultado = self.itens.aggregate(
            total=Sum(F('quantidade') * F('preco_unitario'), output_field=models.DecimalField())
        )
        self.valor_total = resultado['total'] or Decimal('0.00')
        self.save(update_fields=['valor_total'])

    @property
    def saldo_devedor(self):
        try:
            recebidos = self.pagamentos.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            return self.valor_total - recebidos
        except AttributeError:
            return self.valor_total


class ItemComanda(models.Model):
    TIPO_SERVICO_CHOICES = (
        ('reforma', 'Reforma'),
        ('uniforme', 'Uniforme'),
        ('confeccao', 'Confecção'),
    )

    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='itens')
    descricao_servico = models.CharField(max_length=255)
    tipo_servico = models.CharField(max_length=20, choices=TIPO_SERVICO_CHOICES, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descricao_servico} ({self.quantidade}x)"