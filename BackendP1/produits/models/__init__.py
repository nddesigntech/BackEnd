from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='produits')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Image(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()

    def __str__(self):
        return f'Image {self.id} pour {self.produit.nom}'


class Stock(models.Model):
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE, related_name='stock')
    quantite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.produit.nom} stock: {self.quantite}'


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='mouvements')
    quantite = models.IntegerField()
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type_mouvement} {self.quantite} {self.produit.nom}'
