# Système de Réservation et Paiement - RG Luxe Events

## Vue d'ensemble

Ce système permet aux utilisateurs de réserver des services (transport avec chauffeur, transfert aéroport) et de procéder au paiement en ligne. Le processus se déroule en plusieurs étapes :

1. **Réservation** : L'utilisateur remplit un formulaire de réservation
2. **Calcul du prix** : Le système calcule automatiquement le prix
3. **Récapitulatif** : Affichage des détails de la réservation et du prix
4. **Paiement** : Choix entre PayPal et carte bancaire
5. **Confirmation** : Page de succès ou d'échec selon le résultat

## Fonctionnalités

### 🚗 Services disponibles
- **Transport avec chauffeur** : Trajets personnalisés avec option aller-retour
- **Transfert aéroport** : Service de transport vers/depuis les aéroports

### 💳 Méthodes de paiement
- **PayPal** : Paiement sécurisé via PayPal
- **Carte bancaire** : Support pour Visa, Mastercard, American Express

### 🔒 Sécurité
- Validation des données de carte bancaire
- Chiffrement SSL
- Protection contre les injections
- Validation côté serveur et client

## Installation et Configuration

### Prérequis
- Python 3.8+
- Django 5.1+
- Base de données PostgreSQL ou SQLite

### Installation
```bash
# Cloner le projet
git clone [url-du-projet]

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Configuration
1. **Variables d'environnement** : Configurer les clés API PayPal
2. **Base de données** : Configurer la connexion à la base de données
3. **Email** : Configurer le serveur SMTP pour l'envoi d'emails

## Structure du Code

### Modèles (`app/models.py`)
- `Order` : Gère les commandes avec statut de paiement
- `Payment` : Stocke les informations de paiement
- `DriverBooking` : Réservations de transport avec chauffeur
- `AeroportBooking` : Réservations de transfert aéroport

### Vues (`app/views.py`)
- `home()` : Page d'accueil avec formulaires de réservation
- `booking_summary()` : Récapitulatif de la réservation
- `payment()` : Page de paiement
- `payment_success()` : Confirmation de succès
- `payment_failed()` : Page d'échec

### Formulaires (`app/forms.py`)
- `DriverBookingForm` : Formulaire de réservation transport
- `AeroportBookingForm` : Formulaire de réservation aéroport
- `PaymentForm` : Formulaire de paiement

### Templates
- `home.html` : Page d'accueil avec formulaires
- `booking_summary.html` : Récapitulatif de la réservation
- `payment.html` : Page de paiement
- `payment_success.html` : Confirmation de succès
- `payment_failed.html` : Page d'échec

## Flux d'Utilisation

### 1. Réservation
L'utilisateur remplit un formulaire de réservation sur la page d'accueil :
- Lieu de départ et d'arrivée
- Date et heure
- Options supplémentaires (aller-retour)

### 2. Calcul du Prix
Le système calcule automatiquement le prix basé sur :
- Type de service
- Distance (pour le transport)
- Options sélectionnées

### 3. Récapitulatif
Affichage des détails de la réservation :
- Informations du service
- Prix total
- Bouton pour procéder au paiement

### 4. Paiement
L'utilisateur choisit sa méthode de paiement :
- **PayPal** : Redirection vers PayPal
- **Carte bancaire** : Saisie des informations de carte

### 5. Confirmation
- **Succès** : Affichage des détails de la commande
- **Échec** : Explication des raisons possibles et solutions

## Intégration PayPal

### Configuration
```python
# settings.py
PAYPAL_CLIENT_ID = 'your_client_id'
PAYPAL_CLIENT_SECRET = 'your_client_secret'
PAYPAL_MODE = 'sandbox'  # ou 'live'
```

### Webhooks
Configurer les webhooks PayPal pour :
- Confirmation de paiement
- Remboursements
- Annulations

## Tests

### Tests Unitaires
```bash
python manage.py test app.tests
```

### Tests de Paiement
- Utiliser le mode sandbox PayPal
- Tester avec des cartes de test
- Vérifier les emails de confirmation

## Déploiement

### Production
1. Configurer HTTPS
2. Utiliser des clés API de production
3. Configurer la base de données de production
4. Configurer le serveur SMTP de production

### Sécurité
- Validation stricte des données
- Protection CSRF
- Validation des montants
- Logs de sécurité

## Maintenance

### Monitoring
- Surveiller les échecs de paiement
- Vérifier les emails de confirmation
- Analyser les logs de transaction

### Sauvegarde
- Sauvegarde régulière de la base de données
- Sauvegarde des fichiers de configuration
- Sauvegarde des logs

## Support

Pour toute question ou problème :
- Email : support@rgluxeevents.com
- Documentation : [lien-vers-doc]
- Issues : [lien-vers-github]

## Licence

Ce projet est sous licence [licence]. Voir le fichier LICENSE pour plus de détails. 