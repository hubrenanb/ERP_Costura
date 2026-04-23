from django.db import models
from core.models import Empresa
from producao.models import Comanda

class Produto(models.Model):
    TIPO_CHOICES = (
        ('materia_prima', 'Matéria Prima (Produção)'),
        ('uso_consumo', 'Uso e Consumo (Limpeza/Escritório)'),
        ('ativo_imobilizado', 'Ferramentas e Ativos (Tesouras/Máquinas)'),
    )
    UNIDADE_CHOICES = (
        ('un', 'Unidade'), ('m', 'Metros'), ('cm', 'Centímetros'), ('rolo', 'Rolo'), ('litro', 'Litro'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    unidade_medida = models.CharField(max_length=10, choices=UNIDADE_CHOICES)
    quantidade_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTO = (('entrada', 'Entrada'), ('saida', 'Saída'))

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTO)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimento = models.DateTimeField(auto_now_add=True)
    observacao = models.CharField(max_length=255, blank=True, null=True) 
    comanda = models.ForeignKey(Comanda, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo} ({self.quantidade})"
