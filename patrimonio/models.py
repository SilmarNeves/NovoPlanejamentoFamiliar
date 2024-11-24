from django.db import models

class CarteiraBase(models.Model):
    ativo = models.CharField(max_length=10)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_atual = models.DecimalField(max_digits=10, decimal_places=2)
    data_atualizacao = models.DateTimeField()

    class Meta:
        abstract = True

class CarteiraConsolidada(CarteiraBase):
    class Meta:
        db_table = 'carteira_consolidada'

class CarteiraSilmar(CarteiraBase):
    class Meta:
        db_table = 'carteira_silmar'

class CarteiraMonica(CarteiraBase):
    class Meta:
        db_table = 'carteira_monica'
