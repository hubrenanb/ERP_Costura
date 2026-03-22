from django.db import models
from core.models import Empresa
from producao.models import Comanda

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('receita', 'Receita (Entrada)'),
        ('despesa', 'Despesa (Saída)'),
    )
    
    PAGAMENTO_CHOICES = (
        ('dinheiro', 'Dinheiro'),
        ('pix', 'Pix'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('transferencia', 'Transferência'),
        ('outro', 'Outro'),
    )

    # Categorias para o Dashboard de BI classificar os gastos
    CATEGORIA_CHOICES = (
        ('venda', 'Venda de Serviço/Comanda'),
        ('estoque', 'Compra de Material/Insumo'),
        ('limpeza', 'Produtos de Limpeza'),
        ('infra', 'Infraestrutura (Luz/Água/Internet)'),
        ('aluguel', 'Aluguel'),
        ('salario', 'Pró-labore/Salários'),
        ('marketing', 'Marketing/Anúncios'),
        ('outros', 'Outros Gastos'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros')
    descricao = models.CharField(max_length=255, help_text="Ex: 5m de Jeans ou Material de Limpeza")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_transacao = models.DateTimeField(auto_now_add=True)
    metodo_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES)
    
    # Vinculação opcional com comanda (para receitas vindas de serviços)
    comanda = models.ForeignKey(
        Comanda, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='pagamentos'
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} (R$ {self.valor})"

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ['-data_transacao']