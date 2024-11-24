from django.db import models

class Carteira(models.Model):
    TIPOS_INVESTIMENTO = [
        ('Ação', 'Ação'),
        ('FII', 'FII'),
        ('ETF', 'ETF'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_INVESTIMENTO)
    quantidade = models.IntegerField()
    preco_medio = models.DecimalField(max_digits=10, decimal_places=2)
    patrimonio_atual = models.DecimalField(max_digits=10, decimal_places=2)
    ganho_perda = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
