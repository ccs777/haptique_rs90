# Changelog - Haptique RS90 Integration

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [1.1.4] - 2024-12-02

### 🔥 Correction Critique - Persistance États Macros

**Problème :**
- Après redémarrage HA, états macros perdus
- Switches passent à OFF
- sensor.rs90_running_macro = "Idle"
- Topics MQTT non-retained disparaissent

**Solution - Triple approche :**

1. **Fichier de sauvegarde persistant**
   - États sauvegardés dans `.storage/haptique_rs90_{RemoteID}_states.json`
   - Chargés au démarrage
   - Sauvegardés à chaque changement
   
2. **MQTT Retained activé**
   - `retain=True` dans tous les publish de macros
   - Topics persistent sur le broker MQTT
   - Reçus automatiquement au subscribe
   
3. **Mise à jour immédiate locale**
   - État stocké localement dès le trigger
   - Pas d'attente du callback MQTT
   - Double sécurité

### 🔧 Détails techniques

**Nouveau fichier de stockage :**
```
/config/.storage/haptique_rs90_3d5d95aa3a7f7b20_states.json
```

**Contenu :**
```json
{
  "macro_states": {
    "Watch TV": "on",
    "Cinema Mode": "off"
  }
}
```

**Workflow au démarrage :**
```
1. Coordinator __init__
2. Charge .storage/...states.json
3. Restaure macro_states
4. Subscribe aux topics
5. Reçoit retained messages (si broker les a)
6. États restaurés ✅
```

**Workflow au trigger :**
```
1. User appuie switch
2. Publish avec retain=True
3. Update local immédiat
4. Save to file
5. Async update data
→ État visible immédiatement ✅
```

### 📝 Méthodes ajoutées

**coordinator.py :**
```python
def _load_macro_states(self) -> None:
    """Load saved states from JSON file."""

def _save_macro_states(self) -> None:
    """Save current states to JSON file."""
```

**Modifications :**
- `async_trigger_macro`: retain=True + update local
- `_subscribe_macro_trigger`: _save_macro_states() appelé
- `__init__`: _load_macro_states() au démarrage

### ⚠️ Notes importantes

**Broker MQTT retained :**
Si le broker MQTT conserve les messages retained, les états seront automatiquement restaurés au subscribe. Le fichier .storage est une double sécurité.

**Suppression fichier :**
Pour réinitialiser tous les états :
```bash
rm /config/.storage/haptique_rs90_*_states.json
```

**Logs à surveiller :**
```
Loaded saved macro states: {'Watch TV': 'on'}
Saved macro states to file
```

---

## [1.1.3] - 2024-12-02

### 🎯 Correction FINALE Battery - Topics Corrects

- **2 topics distincts identifiés**
  - **Trigger** : `Haptique/{RemoteID}/battery/status` (publish vide)
  - **Value** : `Haptique/{RemoteID}/battery_level` (subscribe)

### 🔧 Fonctionnement

```
1. Publish "" sur battery/status
   → Déclenche mise à jour

2. Télécommande répond
   → Publie sur battery_level
   → Payload direct: "85"

3. Subscribe battery_level reçoit
   → Parse: 85
   → Sensor: 85%
```

### 📝 Formats supportés (battery_level)

```
85          ← Format principal (juste le nombre)
85%         ← Fallback
"text 85"   ← Fallback
```

### 🔧 Changements techniques

**const.py :**
- `TOPIC_BATTERY_STATUS = "battery/status"` (pour publish)
- `TOPIC_BATTERY_LEVEL = "battery_level"` (pour subscribe)

**coordinator.py :**
- Subscribe sur `{base}/battery_level`
- Publish sur `{base}/battery/status`
- Parser simplifié (valeur directe)

### 📊 Topics MQTT

```
Publish (trigger):
  Haptique/3d5d95aa3a7f7b20/battery/status
  Payload: ""

Subscribe (value):
  Haptique/3d5d95aa3a7f7b20/battery_level
  Payload: "85"
```

---

## [1.1.2] - 2024-12-02

### 🎯 Correction DÉFINITIVE Battery

- **Topic correct identifié : `battery/status`**
  - ❌ Pas `battery/get` (n'existe pas)
  - ✅ **Publish sur `battery/status`** avec payload vide
  - ✅ **Subscribe sur `battery/status`** pour recevoir
  - Topic unique pour request ET response

### 📝 Format de réponse

**Format attendu :**
```
battery_level=85
```

**Parsing supporté :**
1. `battery_level=85` (format principal)
2. `battery_level = 85` (avec espaces)
3. `85%` (fallback)
4. `85` (fallback)
5. N'importe quel texte avec un nombre (fallback)

### 🔧 Fonctionnement

```python
# Au démarrage et périodiquement
Publish: Haptique/{RemoteID}/battery/status (payload: "")
  ↓
Subscribe: Haptique/{RemoteID}/battery/status
  ↓
Receive: "battery_level=85"
  ↓
Parse: 85%
  ↓
Sensor: sensor.rs90_battery = 85
```

### 📊 Logs attendus

```
Publishing to Haptique/.../battery/status to request battery level
✓ Battery level request published successfully
Raw battery payload: 'battery_level=85'
Battery level updated: 85%
```

---

## [1.1.1] - 2024-12-02

### 🐛 Correction Critique - Battery

- **Battery PUBLISH correctement implémenté**
  - Subscribe sur `battery/status` ✅ (réactivé)
  - **PUBLISH sur `battery/get` au démarrage** ✅
  - **PUBLISH périodique** (toutes les minutes) ✅
  - Logs détaillés du publish
  - Gestion erreur publish

### 🔧 Détails techniques

**Au démarrage (_subscribe_topics) :**
```python
await mqtt.async_publish(
    hass,
    f"{base_topic}/battery/get",
    "",  # Empty payload
    qos=1
)
```

**Périodiquement (_async_update_data) :**
- Publish `battery/get` toutes les minutes (scan_interval)
- Subscribe `battery/status` reçoit la réponse
- Sensor mis à jour automatiquement

### 📝 Logs à surveiller

```
Publishing to Haptique/.../battery/get to request battery level
✓ Battery level request published successfully
```

Si vous ne voyez PAS ces logs :
- Vérifier logs debug activés
- Vérifier MQTT configuré
- Vérifier topic exact dans MQTT Explorer

---

## [1.1.0] - 2024-12-02

### 🎉 Changements Majeurs

- **SWITCH au lieu de BUTTON** pour les macros
  - Les macros sont maintenant des **switches** (on/off)
  - État visible directement : ON = macro active, OFF = macro inactive
  - `switch.rs90_macro_watch_tv` au lieu de `button.rs90_macro_watch_tv`
  - Méthodes `turn_on` et `turn_off` au lieu de `press`

### ❌ Suppressions

- **Battery sensor supprimé** - Topic MQTT inexistant
  - sensor.rs90_battery retiré
  - Subscribe battery/status désactivé
  - Méthode async_request_battery_level supprimée
  - Le topic battery n'existe pas sur la télécommande

### 🔧 Améliorations

- **Nouveau fichier** : `switch.py`
- **État visible** : `is_on` property pour voir si macro active
- **Icône dynamique** : Play quand OFF, Stop quand ON
- **Attributs** : current_state, macro_name, macro_id

### ⚠️ Breaking Changes

**Migration requise :**

Ancienne entité (v1.0.x):
```yaml
button.rs90_macro_watch_tv
service: button.press
```

Nouvelle entité (v1.1.0):
```yaml
switch.rs90_macro_watch_tv
service: switch.turn_on  # ou turn_off
```

---

## [1.0.5] - 2024-12-02

### 🐛 Corrections Critiques

- **Battery Level - PUBLISH au lieu de Subscribe** : CORRECTION MAJEURE
  - Changement de méthode : maintenant on DEMANDE le niveau de batterie
  - Publish sur `battery/get` dans `_async_update_data()`
  - Subscribe à `battery/status` pour recevoir la réponse
  - Update périodique toutes les minutes (SCAN_INTERVAL)

### 📚 Documentation Mise à Jour

- **GESTION_VEILLE.md - Réalité corrigée**
  - ⚠️ Device VRAIMENT déconnecté (offline) en veille
  - ❌ Keep-Alive NE FONCTIONNE PAS (device déconnecté)
  - ❌ Wake-Up par MQTT NE FONCTIONNE PAS (device déconnecté)
  - ✅ Solutions réalistes : Accepter limitation, conditions, notifications
  - ✅ Boutons automatiquement désactivés quand offline
  - ✅ Alternative matérielle : IR Blaster toujours alimenté

### 🔧 Changements Techniques

- `_async_update_data()` : Publish sur `battery/get` au lieu de simplement retourner data
- Logs améliorés : "Requested battery level update"
- Gestion erreurs lors du publish

### 💡 Clarifications

- La télécommande en veille = Status MQTT offline
- Impossible d'envoyer des commandes quand offline
- Boutons HA automatiquement grisés (déjà implémenté)
- Solution : Action physique nécessaire ou IR Blaster alternatif

---

## [1.0.4] - 2024-12-02

### 🐛 Corrections

- **Battery Parsing amélioré** : Support de multiples formats
  - "85%", "85 %", "85", "battery_level 85"
  - Utilisation de regex pour extraire n'importe quel nombre
  - Logs améliorés avec payload brut

### 📚 Documentation

- **VISUALISATION_MACROS.md** : Guide complet pour colorer les boutons
  - 5 solutions détaillées (Mushroom, Button Card, Template, etc.)
  - Comparaison et recommandations
  - Exemples de code prêts à l'emploi

- **GESTION_VEILLE.md** : Solutions pour la mise en veille
  - 6 solutions détaillées (Keep-Alive, Wake-Up, Détection, etc.)
  - Comparaison impact batterie
  - Scripts et automatisations prêts à l'emploi
  - Tips avancés (monitoring batterie, mode éco nuit)

### 🔧 Améliorations techniques

- Logs plus détaillés pour le battery parsing
- Import `re` pour expressions régulières
- Meilleure gestion des erreurs

---

## [1.0.3] - 2024-12-02

### ✨ Nouveautés majeures

- **Auto-découverte du Remote ID** : Plus besoin de saisir manuellement l'ID
  - Détection automatique de la télécommande sur MQTT
  - L'utilisateur donne juste un nom (optionnel)
  - Configuration simplifiée en 1 clic

- **Bouton Toggle ON/OFF** : Un seul bouton qui change d'état
  - Appuyer une fois → ON (▶️)
  - Appuyer de nouveau → OFF (⏹️)
  - Icône dynamique selon l'état actuel
  - Attribut `current_state` pour connaître l'état

- **Running Macro amélioré** : Détection intelligente
  - Récupère la macro avec état "on" depuis MQTT
  - Subscribe au topic `macro/{name}/trigger`
  - Affiche la macro actuellement en cours
  - Attributs `macro_states` et `active_macros`

### 🔧 Modifications

- **Config Flow simplifié** : Découverte automatique au lieu de saisie manuelle
- **Sensor Running Macro** : Utilise les états MQTT réels au lieu du topic test/status
- **Boutons Macro** : Un seul bouton toggle au lieu de 2 boutons séparés

### 📝 Changements d'entités

**Avant (v1.0.2) :**
- `button.rs90_macro_watch_tv_start`
- `button.rs90_macro_watch_tv_stop`

**Maintenant (v1.0.3) :**
- `button.rs90_macro_watch_tv` (toggle ON/OFF)

---

## [1.0.2] - 2024-12-02

### ✨ Nouveautés
- **Sensor Device List** : Nouveau sensor affichant la liste des devices
  - Affiche le nombre total de devices
  - Liste tous les noms de devices dans les attributs
  - Chaque device accessible via `device_1`, `device_2`, etc.

- **Boutons Macro ON/OFF** : Gestion complète des macros
  - Bouton "Start" pour déclencher une macro (ON)
  - Bouton "Stop" pour arrêter une macro (OFF)
  - Icônes distinctes (play/stop)

- **Service refresh_data** : Actualisation manuelle des données
  - Force la mise à jour des devices et macros
  - Utile après ajout/suppression de macros sur la télécommande

### 🔧 Modifications
- **Interval de refresh** : Réduit de 5 minutes à 1 minute
  - Détection plus rapide des changements
  - Meilleure réactivité

- **Suppression des boutons de commandes devices**
  - Plus de création automatique des boutons de commandes
  - Utiliser le service `trigger_device_command` à la place
  - Simplification de l'intégration

### 🐛 Corrections
- **Config Flow** : Correction de la dépréciation
  - `self.config_entry` → `self._config_entry`
  - Compatible avec Home Assistant 2025.12+

### 📝 Documentation
- Instructions mises à jour pour la v1.0.2
- Exemples d'utilisation des nouveaux boutons ON/OFF
- Guide d'utilisation du nouveau sensor device_list

---

## [1.0.1] - 2024-12-01

### 🐛 Corrections
- **Normalisation des ID** : Gestion des clés JSON "id" ET "Id" (majuscule/minuscule)
  - Les devices avec `"Id"` sont maintenant correctement détectés
  - Les macros avec `"Id"` sont maintenant correctement détectées
  - Les commandes avec `"Id"` sont maintenant correctement détectées

- **Amélioration des logs** : Messages plus détaillés pour le débogage
  - Logs INFO pour les subscriptions réussies avec symbole ✓
  - Logs ERROR pour les échecs avec symbole ✗
  - Logs détaillés lors de la normalisation des données
  - Logs lors du stockage des commandes

- **Gestion d'erreurs améliorée** : Try-catch sur les subscriptions MQTT
  - Capture des erreurs de subscription
  - Messages d'erreur plus explicites

### ✨ Nouveautés
- **Service de diagnostic** : `haptique_rs90.get_diagnostics`
  - Affiche l'état complet du coordinator dans les logs
  - Liste des devices trouvés
  - Liste des macros trouvées
  - Nombre de commandes par device
  - Nombre de subscriptions actives

- **Documentation** : Nouveau guide de dépannage
  - `TROUBLESHOOTING_BUTTONS.md` : Guide complet pour diagnostiquer les boutons manquants
  - Checklist étape par étape
  - Solutions pour chaque problème courant

### 🔧 Améliorations techniques
- Normalisation systématique des données JSON reçues
- Logs structurés avec niveaux appropriés (INFO, DEBUG, ERROR)
- Méthode `get_diagnostics()` dans le coordinator
- Gestion robuste des variations de format JSON

---

## [1.0.0] - 2024-12-01

### 🎉 Version initiale

#### ✨ Fonctionnalités principales
- Configuration via l'interface utilisateur (UI)
- Support MQTT avec messages retained
- Découverte automatique des devices et macros
- Création dynamique des entités

#### 📊 Sensors
- `sensor.rs90_battery` : Niveau de batterie avec icône dynamique
- `binary_sensor.rs90_connection` : État de connexion (online/offline)
- `sensor.rs90_last_key_pressed` : Dernier bouton physique pressé
- `sensor.rs90_running_macro` : Macro en cours d'exécution

#### 🔘 Boutons
- Boutons dynamiques pour chaque macro
- Boutons dynamiques pour chaque commande de device
- Création automatique lors de la découverte

#### ⚙️ Services
- `haptique_rs90.trigger_macro` : Déclencher une macro
- `haptique_rs90.trigger_device_command` : Déclencher une commande

#### 🌐 Traductions
- Interface complète en français
- Interface complète en anglais

#### 📚 Documentation
- README.md complet
- Guide d'installation détaillé (INSTALLATION.md)
- Guide de démarrage rapide (QUICKSTART.md)
- Résumé technique (PROJECT_SUMMARY.md)
- Exemples d'utilisation (example_configuration.yaml)
- Structure du projet (STRUCTURE.txt)

#### 🔧 Technique
- Compatible HACS
- Architecture coordinator/entity
- QoS 1 pour MQTT
- Support multi-télécommandes
- Gestion des erreurs et logs

---

## Format du changelog

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

### Types de changements
- `Added` (Ajouté) pour les nouvelles fonctionnalités
- `Changed` (Modifié) pour les changements dans les fonctionnalités existantes
- `Deprecated` (Déprécié) pour les fonctionnalités qui seront bientôt supprimées
- `Removed` (Retiré) pour les fonctionnalités supprimées
- `Fixed` (Corrigé) pour les corrections de bugs
- `Security` (Sécurité) en cas de vulnérabilités
