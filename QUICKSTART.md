# 🚀 DÉMARRAGE RAPIDE - Haptique RS90

## ⚡ Installation en 5 minutes

### 1️⃣ Copier les fichiers
```bash
# Via SSH ou File Editor
cd /config
mkdir -p custom_components
cd custom_components

# Copier le dossier haptique_rs90 ici
# Ou décompresser haptique_rs90.tar.gz
tar -xzf haptique_rs90.tar.gz
```

### 2️⃣ Redémarrer Home Assistant
```
Paramètres → Système → Redémarrer
```

### 3️⃣ Trouver votre Remote ID
```bash
# Méthode 1 : MQTT Explorer
# Chercher le topic : Haptique/{RemoteID}/status

# Méthode 2 : mosquitto_sub
mosquitto_sub -h localhost -t "Haptique/+/status" -v

# Exemple de résultat :
# Haptique/4deba8d571ace2a0/status online
#          ^^^^^^^^^^^^^^^^
#          C'est votre Remote ID !
```

### 4️⃣ Ajouter l'intégration
```
Paramètres → Appareils et services → + Ajouter une intégration
→ Rechercher "Haptique RS90"
→ Entrer le Remote ID : 4deba8d571ace2a0
→ (Optionnel) Nom : Télécommande Salon
→ Soumettre
```

### 5️⃣ Vérifier les entités
```
Outils de développement → États → Rechercher "rs90"

Vous devriez voir :
✅ binary_sensor.rs90_connection
✅ sensor.rs90_battery
✅ sensor.rs90_last_key_pressed
✅ sensor.rs90_running_macro
✅ button.rs90_macro_*
✅ button.rs90_*_*
```

## 🎯 Premier test

### Test d'une macro
```yaml
# Outils de développement → Services
service: button.press
data:
  entity_id: button.rs90_macro_watch_tv_1
```

### Test d'une commande
```yaml
service: button.press
data:
  entity_id: button.rs90_canal_g9_4k_power
```

## 📱 Carte Dashboard minimale

```yaml
type: vertical-stack
cards:
  - type: entities
    title: RS90 Salon
    entities:
      - binary_sensor.rs90_connection
      - sensor.rs90_battery
  - type: horizontal-stack
    cards:
      - type: button
        entity: button.rs90_macro_watch_tv_1
        name: TV
        icon: mdi:television
```

## 🔧 Dépannage express

### ❌ "mqtt_not_configured"
```bash
# Installer Mosquitto
Paramètres → Modules complémentaires → Boutique → Mosquitto broker
→ Installer → Démarrer → Démarrage au boot
```

### ❌ Pas de boutons
```bash
# Attendre 30 secondes après l'ajout
# Puis recharger l'intégration :
Paramètres → Appareils et services → Haptique RS90 → ⋮ → Recharger
```

### ❌ "Device already configured"
```bash
# Ce Remote ID est déjà ajouté
# Pour reconfigurer : supprimer puis réajouter
```

## 📚 Fichiers importants

- **README.md** - Documentation complète
- **INSTALLATION.md** - Guide détaillé
- **example_configuration.yaml** - Exemples d'utilisation
- **PROJECT_SUMMARY.md** - Résumé technique

## 💡 Astuce

Activez les logs pour le débogage :

```yaml
# configuration.yaml
logger:
  logs:
    custom_components.haptique_rs90: debug

# Puis redémarrer et consulter :
# Paramètres → Système → Logs
```

## ✅ C'est prêt !

Votre intégration Haptique RS90 est maintenant fonctionnelle.
Consultez les autres fichiers pour des exemples avancés.

Bon contrôle ! 🎮
