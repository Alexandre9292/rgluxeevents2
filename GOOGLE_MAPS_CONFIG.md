# Configuration Google Maps API

## Étapes pour activer l'autocomplétion et le calcul de distance

### 1. Obtenir une clé API Google Maps
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez les APIs suivantes :
   - Maps JavaScript API
   - Places API
   - Directions API
4. Créez des identifiants (clé API)
5. Restreignez la clé API aux domaines autorisés

### 2. Remplacer la clé API dans le code
Dans le fichier `app/templates/app/transport.html`, remplacez :
```javascript
src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap"
```
par votre vraie clé API :
```javascript
src="https://maps.googleapis.com/maps/api/js?key=VOTRE_CLE_API&libraries=places&callback=initMap"
```

### 3. Fonctionnalités activées
- ✅ Autocomplétion des adresses avec Google Places
- ✅ Calcul automatique de la distance
- ✅ Calcul automatique du prix selon la grille tarifaire
- ✅ Affichage de l'itinéraire sur la carte
- ✅ Marqueurs de départ et d'arrivée
- ✅ Restriction géographique à La Réunion

### 4. Sécurité
- Restreignez votre clé API aux domaines autorisés
- Activez la facturation si nécessaire (Google offre des crédits gratuits)
- Surveillez l'utilisation de votre API

### 5. Test
Une fois configuré, testez :
1. Tapez une adresse dans le champ départ
2. Sélectionnez une suggestion de l'autocomplétion
3. Faites de même pour l'arrivée
4. Vérifiez que la distance et le prix se calculent automatiquement
5. Vérifiez que l'itinéraire s'affiche sur la carte 