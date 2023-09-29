from django.db import models

# Create your models here.


class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField()
    descricao = models.TextField()
    valor = models.FloatField()
    desconto = models.FloatField()
    estoque = models.PositiveIntegerField()
    urlImagem = models.URLField()
    criadoEm = models.DateTimeField(auto_now_add=True)
    atualizadoEm = models.DateTimeField(auto_now=True)
