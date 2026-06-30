# BackendP1

Backend Django pour le Projet P1 — plateforme e-commerce multi-acteurs (clients, vendeurs, gestionnaires).

## Stack technique

- **Framework** : Django 6.0.4
- **Langage** : Python 3.14
- **Base de données** : SQLite (développement)

---

## Structure du projet

```
BackEnd/
└── BackendP1/              ← Racine Django (manage.py)
    ├── BackendP1/          ← Configuration centrale
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── authentification/   ← Gestion des utilisateurs et rôles
    ├── produits/           ← Catalogue produits
    ├── commande/           ← Paniers et commandes
    ├── paiement/           ← Paiements et historique
    └── abonnementVendeur/  ← Abonnements des vendeurs
```

---

## Applications

### `authentification`
Gère les comptes utilisateurs et les différents rôles de la plateforme.

| Modèle        | Rôle                                      |
|---------------|-------------------------------------------|
| `user`        | Modèle de base utilisateur                |
| `client`      | Acheteur sur la plateforme                |
| `vendeur`     | Marchand qui publie des produits          |
| `gestionnaire`| Gestionnaire interne de la plateforme     |
| `admin`       | Administrateur avec droits complets       |

---

### `produits`
Gère le catalogue de produits disponibles sur la plateforme.

| Modèle            | Rôle                                      |
|-------------------|-------------------------------------------|
| `produits`        | Fiche produit (nom, prix, description...) |
| `categories`      | Catégorisation des produits               |
| `images`          | Images associées à un produit             |
| `stocks`          | Niveau de stock par produit               |
| `mouvement_stocks`| Historique des entrées/sorties de stock   |

---

### `commande`
Gère le cycle de vie d'une commande, du panier à la validation.

| Modèle          | Rôle                                        |
|-----------------|---------------------------------------------|
| `panier`        | Panier actif d'un client                    |
| `panier_item`   | Produit ajouté dans le panier               |
| `commande`      | Commande passée par un client               |
| `ligne_commande`| Détail d'un produit dans une commande       |

---

### `paiement`
Gère les transactions financières liées aux commandes.

| Modèle              | Rôle                                    |
|---------------------|-----------------------------------------|
| `paiement`          | Transaction de paiement d'une commande  |
| `historique_paiement`| Journal des paiements effectués        |

---

### `abonnementVendeur`
Gère les plans d'abonnement que les vendeurs souscrivent pour accéder à la plateforme.

| Modèle               | Rôle                                        |
|----------------------|---------------------------------------------|
| `plan_abonnement`    | Définition des offres (gratuit, premium...) |
| `abonnement`         | Souscription d'un vendeur à un plan         |
| `paiement_abonnement`| Paiement associé à un abonnement           |

---

## Lancer le projet

```bash
# Installer les dépendances
pip install django

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
```

## Créer un superutilisateur

```bash
python manage.py createsuperuser
```

Interface d'administration disponible sur : `http://127.0.0.1:8000/admin/`
