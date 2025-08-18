"""
Intégration PayPal pour RG Luxe Events
Ce fichier contient les fonctions pour intégrer PayPal au système de paiement
"""

import json
import requests
from django.conf import settings
from django.urls import reverse

class PayPalIntegration:
    """Classe pour gérer l'intégration PayPal"""
    
    def __init__(self):
        self.client_id = settings.PAYMENT_SETTINGS['PAYPAL_CLIENT_ID']
        self.client_secret = settings.PAYMENT_SETTINGS['PAYPAL_CLIENT_SECRET']
        self.mode = settings.PAYMENT_SETTINGS['PAYPAL_MODE']
        self.base_url = 'https://api-m.sandbox.paypal.com' if self.mode == 'sandbox' else 'https://api-m.paypal.com'
        self.access_token = None
    
    def get_access_token(self):
        """Obtenir un token d'accès PayPal"""
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'client_credentials',
        }
        
        response = requests.post(
            url,
            headers=headers,
            data=data,
            auth=(self.client_id, self.client_secret)
        )
        
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return self.access_token
        else:
            raise Exception(f"Erreur lors de l'obtention du token PayPal: {response.text}")
    
    def create_payment(self, order, return_url, cancel_url):
        """Créer un paiement PayPal"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.base_url}/v1/payments/payment"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        
        payment_data = {
            'intent': 'sale',
            'payer': {
                'payment_method': 'paypal'
            },
            'redirect_urls': {
                'return_url': return_url,
                'cancel_url': cancel_url
            },
            'transactions': [{
                'amount': {
                    'total': str(order.total_price),
                    'currency': settings.PAYMENT_SETTINGS['CURRENCY']
                },
                'description': f'Réservation {order.booking_type} - {order.order_number}',
                'item_list': {
                    'items': [{
                        'name': f'Service {order.booking_type}',
                        'price': str(order.total_price),
                        'currency': settings.PAYMENT_SETTINGS['CURRENCY'],
                        'quantity': 1
                    }]
                }
            }]
        }
        
        response = requests.post(url, headers=headers, json=payment_data)
        
        if response.status_code == 201:
            payment_info = response.json()
            return payment_info['id'], payment_info['links']
        else:
            raise Exception(f"Erreur lors de la création du paiement PayPal: {response.text}")
    
    def execute_payment(self, payment_id, payer_id):
        """Exécuter un paiement PayPal"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.base_url}/v1/payments/payment/{payment_id}/execute/"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'payer_id': payer_id
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de l'exécution du paiement PayPal: {response.text}")
    
    def get_payment_details(self, payment_id):
        """Obtenir les détails d'un paiement PayPal"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.base_url}/v1/payments/payment/{payment_id}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la récupération des détails du paiement: {response.text}")

def create_paypal_payment_url(order, request):
    """Fonction utilitaire pour créer une URL de paiement PayPal"""
    paypal = PayPalIntegration()
    
    # URLs de retour
    base_url = request.build_absolute_uri('/')[:-1]  # Enlever le slash final
    return_url = f"{base_url}/payment/paypal/success/{order.id}/"
    cancel_url = f"{base_url}/payment/paypal/cancel/{order.id}/"
    
    try:
        payment_id, links = paypal.create_payment(order, return_url, cancel_url)
        
        # Trouver l'URL d'approbation
        approval_url = None
        for link in links:
            if link['rel'] == 'approval_url':
                approval_url = link['href']
                break
        
        if approval_url:
            return approval_url, payment_id
        else:
            raise Exception("URL d'approbation PayPal non trouvée")
            
    except Exception as e:
        print(f"Erreur lors de la création du paiement PayPal: {e}")
        return None, None

# Exemple d'utilisation
if __name__ == "__main__":
    print("🔧 Configuration PayPal pour RG Luxe Events")
    print("\n📋 Étapes de configuration:")
    print("1. Créer un compte développeur PayPal")
    print("2. Obtenir les clés API (Client ID et Secret)")
    print("3. Configurer les URLs de retour")
    print("4. Tester en mode sandbox")
    print("5. Passer en mode production")
    
    print("\n⚙️ Variables à configurer dans settings.py:")
    print("PAYPAL_CLIENT_ID = 'your_client_id'")
    print("PAYPAL_CLIENT_SECRET = 'your_client_secret'")
    print("PAYPAL_MODE = 'sandbox'  # ou 'live'")
    
    print("\n🌐 URLs de retour à configurer:")
    print("- Succès: /payment/paypal/success/{order_id}/")
    print("- Annulation: /payment/paypal/cancel/{order_id}/")
    
    print("\n📧 Webhooks à configurer:")
    print("- Paiement approuvé")
    print("- Paiement échoué")
    print("- Remboursement") 