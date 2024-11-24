from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Transacao(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa')
    ]
    
    descricao = models.CharField(max_length=200)
    data = models.DateField(default=timezone.now)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='R')
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"      

class SaldosFaturas(models.Model):
    data = models.DateField(default=timezone.now)
    saldo_bradesco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_itau = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_inter = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fatura_bradesco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fatura_itau = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fatura_inter = models.DecimalField(max_digits=10, decimal_places=2, default=0)
