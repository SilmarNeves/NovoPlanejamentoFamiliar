from django.db import models

class TransacoesConsolidadas(models.Model):
    data = models.DateField(db_column='Data', blank=True, null=True)
    operacao = models.TextField(db_column='Operacao', blank=True, null=True)
    ativo = models.TextField(db_column='Ativo', blank=True, null=True)
    quantidade = models.IntegerField(db_column='Quantidade', blank=True, null=True)
    preço = models.FloatField(db_column='Preço', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacoes_consolidadas'

class TransacoesMonica(models.Model):
    data = models.DateField(db_column='Data', blank=True, null=True)
    operacao = models.TextField(db_column='Operacao', blank=True, null=True)
    ativo = models.TextField(db_column='Ativo', blank=True, null=True)
    quantidade = models.IntegerField(db_column='Quantidade', blank=True, null=True)
    preço = models.FloatField(db_column='Preço', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacoes_monica'

class TransacoesSilmar(models.Model):
    data = models.DateField(db_column='Data', blank=True, null=True)
    operacao = models.TextField(db_column='Operacao', blank=True, null=True)
    ativo = models.TextField(db_column='Ativo', blank=True, null=True)
    quantidade = models.IntegerField(db_column='Quantidade', blank=True, null=True)
    preço = models.FloatField(db_column='Preço', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacoes_silmar'