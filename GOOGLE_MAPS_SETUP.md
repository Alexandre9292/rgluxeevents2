# Configuration Google Maps API pour RG Luxe Events

## 🗺️ **Fonctionnalités Implémentées**

### ✅ **Carte Interactive**
- Carte centrée sur La Réunion
- Affichage en temps réel
- Style personnalisé avec les couleurs de la marque

### 🔍 **Autocomplétion d'Adresses**
- Suggestions automatiques lors de la saisie
- Restriction géographique à La Réunion
- Support des établissements et adresses

### 🛣️ **Calcul d'Itinéraire**
- Tracé automatique du trajet le plus court
- Affichage de la distance et durée
- Ligne de trajet stylisée (couleur dorée)

## 🔑 **Configuration de l'API**

### 1. **Obtenir une Clé API Google Maps**

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez les APIs suivantes :
   - **Maps JavaScript API**
   - **Places API**
   - **Directions API**
4. Créez des identifiants (clé API)
5. Restreignez la clé API pour la sécurité

### 2. **Restrictions de Sécurité (Recommandé)**

```javascript
// Restreindre par domaine
// Ajoutez votre domaine dans la console Google Cloud
// Exemple : *.rgluxeevents.com, localhost

// Restreindre par API
// Limitez aux APIs nécessaires uniquement
```

### 3. **Mise à Jour de la Configuration**

1. **Dans `rgevents/settings.py` :**
```python
GOOGLE_MAPS_API_KEY = 'VOTRE_VRAIE_CLE_API_ICI'
```

2. **Dans `templates/base.html` :**
```html
<script src="https://maps.googleapis.com/maps/api/js?key=VOTRE_CLE_API&libraries=places"></script>
```

## 🎯 **Utilisation**

### **Pour l'Utilisateur :**
1. **Saisie d'adresse** : Commencez à taper dans les champs départ/arrivée
2. **Sélection** : Choisissez une suggestion dans la liste déroulante
3. **Visualisation** : L'itinéraire s'affiche automatiquement sur la carte
4. **Informations** : Distance et durée estimées s'affichent sous la carte

### **Fonctionnalités Techniques :**
- **Autocomplétion** : Suggestions en temps réel
- **Géocodage** : Conversion adresse → coordonnées GPS
- **Calcul d'itinéraire** : Algorithme de plus court chemin
- **Affichage dynamique** : Mise à jour automatique de la carte

## 🚀 **Déploiement**

### **Variables d'Environnement (Recommandé) :**
```bash
# .env
GOOGLE_MAPS_API_KEY=votre_cle_api_ici
```

### **Dans `settings.py` :**
```python
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
```

## 📱 **Responsive Design**

- **Mobile** : Carte adaptée aux petits écrans
- **Tablette** : Affichage optimisé
- **Desktop** : Carte en pleine largeur

## 🔒 **Sécurité**

### **Bonnes Pratiques :**
1. **Ne jamais exposer** la clé API dans le code source
2. **Restreindre par domaine** dans Google Cloud Console
3. **Limiter les APIs** aux fonctionnalités nécessaires
4. **Surveiller l'utilisation** via Google Cloud Console

### **Limitations :**
- **Quota gratuit** : 2000 requêtes/jour pour Maps JavaScript API
- **Places API** : 1000 requêtes/jour
- **Directions API** : 100 requêtes/jour

## 🐛 **Dépannage**

### **Problèmes Courants :**

1. **Carte ne s'affiche pas :**
   - Vérifiez la clé API
   - Vérifiez les restrictions de domaine
   - Consultez la console du navigateur

2. **Autocomplétion ne fonctionne pas :**
   - Vérifiez que Places API est activée
   - Vérifiez la clé API

3. **Itinéraire ne se calcule pas :**
   - Vérifiez que Directions API est activée
   - Vérifiez les coordonnées GPS

### **Console du Navigateur :**
```javascript
// Vérifiez les erreurs JavaScript
// Vérifiez les requêtes réseau
// Vérifiez les erreurs d'API
```

## 📞 **Support**

Pour toute question technique :
- Consultez la [documentation Google Maps](https://developers.google.com/maps)
- Vérifiez les [quotas et limites](https://developers.google.com/maps/documentation/javascript/usage-and-billing)
- Contactez l'équipe de développement RG Luxe Events

---

**Note :** Cette implémentation utilise l'API Google Maps v3 avec les dernières fonctionnalités disponibles. 