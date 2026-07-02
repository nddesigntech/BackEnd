from django.contrib import admin

from .models import Categorie, Image, MouvementStock, Produit, Stock


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'description']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prix', 'categorie', 'date_creation', 'date_modification']
    list_filter = ['categorie']
    search_fields = ['nom', 'description']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'produit', 'url']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'produit', 'quantite']


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ['id', 'produit', 'type_mouvement', 'quantite', 'date']
