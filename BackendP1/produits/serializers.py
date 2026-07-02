from rest_framework import serializers

from .models import Produit, Categorie, Image, Stock, MouvementStock


class CategorieSerializer(serializers.ModelSerializer):
    # Sérialiseur pour les catégories de produits
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'produit']


class StockSerializer(serializers.ModelSerializer):
    # Sérialiseur pour le stock du produit
    class Meta:
        model = Stock
        fields = ['id', 'produit', 'quantite']


class MouvementStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = ['id', 'produit', 'quantite', 'type_mouvement', 'date']


class ProduitSerializer(serializers.ModelSerializer):
    # Sérialiseur principal pour les produits
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(), source='categorie', write_only=True, required=False
    )

    class Meta:
        model = Produit
        fields = [
            'id',
            'nom',
            'description',
            'prix',
            'categorie',
            'categorie_id',
            'date_creation',
            'date_modification',
        ]
