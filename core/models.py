from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_fantasia

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionario'),
    )
    
    # Refatoração: Email agora é obrigatório e único para login
    email = models.EmailField('Endereço de e-mail', unique=True)
    
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        related_name='usuarios', 
        null=True,
        blank=True
    )
    tipo = models.CharField(max_length=15, choices=TIPO_USUARIO, default='funcionario')
    telefone = models.CharField(max_length=15, blank=True, null=True)

    # Define o email como o campo de login oficial
    USERNAME_FIELD = 'email'
    # O username ainda existe no banco, mas passa a ser apenas um campo adicional exigido
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.empresa.nome_fantasia if self.empresa else 'S/E'})"

class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=False)
    telefone = models.CharField(max_length=15)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.empresa.nome_fantasia}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome_completo']