from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.FloatField()
    discount = models.FloatField()
    stock = models.PositiveIntegerField()
    imageUrl = models.URLField()
    CATEGORY_CHOICES = [
        ("supermarket", "Supermercado"),
        ("tecnology", "Tecnologia"),
        ("house-and-furniture", "Casa e Móveis"),
        ("home-appliances", "Eletrodomésticos"),
        ("sports-and-fitness", "Esportes e Fitness"),
        ("tools-and-construction", "Ferramentas e Construção"),
        ("health", "Saúde"),
        ("beauty-and-self-care", "Beleza e Cuidado Pessoal"),
        ("fashion", "Moda"),
        ("babies", "Bebês"),
        ("toys", "Brinquedos"),
        ("aerospace", "Aeroespacial"),
        ("military", "Bélicos"),
    ]
    category = models.CharField(
        max_length=22,
        choices=CATEGORY_CHOICES,
        null=False
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
