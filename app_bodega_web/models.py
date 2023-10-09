from django.db import models
from django.contrib.auth import get_user_model


def generateUniqueSlug(productName):
    slug = "-".join(str(productName).split())
    slug = slug.lower()
    slug = slug.replace("/", "-")

    index = 1
    slugBase = slug
    while True:
        try:
            Product.objects.get(slug=slug)
        except:
            return slug

        index += 1
        slug = slugBase + f"--{index}"

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
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

    def save(self, *args, **kwargs):
        self.slug = generateUniqueSlug(self.name)
        return super().save(*args, **kwargs)


class Address(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    STATES_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
        ('DF', 'Distrito Federal'),
    ]
    state = models.CharField(
        max_length=2,
        choices=STATES_CHOICES,
        null=False
    )
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True)


class CartItem(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        unique_toguether: ("user", "product")
