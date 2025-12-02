# Haptique RS90 Remote - Home Assistant Integration

Intégration Home Assistant pour la télécommande universelle Haptique RS90 via MQTT.

## Fonctionnalités

### Sensors
- **Battery Level** : Niveau de batterie de la télécommande (%)
- **Connection Status** : État de connexion (online/offline)
- **Last Key Pressed** : Dernier bouton physique pressé sur la télécommande
- **Running Macro** : Macro ou commande en cours d'exécution

### Boutons dynamiques
- **Boutons de macros** : Un bouton pour chaque macro configurée sur la télécommande
- **Boutons de commandes** : Un bouton pour chaque commande de chaque appareil

### Découverte automatique
L'intégration détecte automatiquement :
- Tous les appareils (devices) configurés sur la télécommande
- Toutes les macros disponibles
- Toutes les commandes pour chaque appareil

Les entités sont créées dynamiquement lors de la découverte.

## Prérequis

1. **MQTT** : Broker MQTT configuré dans Home Assistant (ex: Mosquitto)
2. **Télécommande Haptique RS90** : Connectée au même broker MQTT

## Installation

### Via HACS (recommandé)
1. Ouvrir HACS dans Home Assistant
2. Aller dans "Intégrations"
3. Cliquer sur les 3 points en haut à droite → "Dépôts personnalisés"
4. Ajouter l'URL du repository : `https://github.com/daangel27/haptique_rs90`
5. Catégorie : "Integration"
6. Rechercher "Haptique RS90" et installer

### Installation manuelle
1. Télécharger le dossier `haptique_rs90`
2. Copier dans `custom_components/haptique_rs90/` de votre installation Home Assistant
3. Redémarrer Home Assistant

## Configuration

### Via l'interface utilisateur (UI)
1. Aller dans **Paramètres** → **Appareils et services**
2. Cliquer sur **+ Ajouter une intégration**
3. Rechercher **Haptique RS90 Remote**
4. Entrer l'**ID de la télécommande** (Remote ID - UUID)
5. (Optionnel) Personnaliser le nom de la télécommande

### Obtenir le Remote ID
Le Remote ID est publié automatiquement par la télécommande sur le topic MQTT :
```
Haptique/{RemoteID}/status
```

Vous pouvez le trouver dans MQTT Explorer ou dans les logs Home Assistant.

Exemple : `4deba8d571ace2a0`

## Topics MQTT utilisés

### Topics subscribés automatiquement
```
Haptique/{RemoteID}/status                    # État de connexion
Haptique/{RemoteID}/device/list               # Liste des appareils
Haptique/{RemoteID}/macro/list                # Liste des macros
Haptique/{RemoteID}/battery/status            # Niveau de batterie
Haptique/{RemoteID}/keys                      # Événements des touches physiques
Haptique/{RemoteID}/test/status               # État d'exécution
Haptique/{RemoteID}/device/{device}/detail    # Détails des commandes d'un appareil
```

### Topics publiés lors des actions
```
Haptique/{RemoteID}/macro/{macro_name}/trigger        # Déclencher une macro
Haptique/{RemoteID}/device/{device_name}/trigger      # Déclencher une commande
```

## Utilisation

### Dans les automatisations

#### Déclencher une macro
```yaml
service: button.press
target:
  entity_id: button.rs90_macro_watch_tv_1
```

#### Déclencher une commande d'appareil
```yaml
service: button.press
target:
  entity_id: button.rs90_canal_g9_4k_power
```

#### Réagir à un bouton physique pressé
```yaml
trigger:
  - platform: state
    entity_id: sensor.rs90_last_key_pressed
action:
  - service: notify.notify
    data:
      message: "Bouton {{ trigger.to_state.state }} pressé !"
```

#### Vérifier l'état de connexion
```yaml
trigger:
  - platform: state
    entity_id: binary_sensor.rs90_connection
    to: "off"
action:
  - service: notify.notify
    data:
      message: "Télécommande RS90 déconnectée !"
```

### Dans le dashboard

#### Carte simple
```yaml
type: entities
title: Télécommande RS90
entities:
  - entity: binary_sensor.rs90_connection
  - entity: sensor.rs90_battery
  - entity: sensor.rs90_last_key_pressed
  - entity: sensor.rs90_running_macro
```

#### Carte avec boutons
```yaml
type: grid
columns: 2
square: false
cards:
  - type: button
    entity: button.rs90_macro_watch_tv_1
    name: Regarder la TV
    icon: mdi:television
  - type: button
    entity: button.rs90_canal_g9_4k_power
    name: Canal+ Power
    icon: mdi:power
```

## Support multi-télécommandes

L'intégration supporte plusieurs télécommandes RS90 :
1. Ajouter une nouvelle intégration pour chaque télécommande
2. Chaque télécommande aura ses propres entités avec des ID uniques

## Dépannage

### La télécommande n'apparaît pas
- Vérifier que MQTT est bien configuré et actif
- Vérifier que la télécommande publie sur les topics MQTT
- Consulter les logs : **Paramètres** → **Système** → **Logs**

### Les boutons ne fonctionnent pas
- Vérifier l'état de connexion (`binary_sensor.rs90_connection`)
- Vérifier que le broker MQTT reçoit les messages
- Tester manuellement avec MQTT Explorer

### Les entités ne se créent pas automatiquement
- Attendre quelques secondes après l'ajout de l'intégration
- Recharger l'intégration : **Paramètres** → **Appareils et services** → **Haptique RS90** → **⋮** → **Recharger**

## Exemples de données MQTT

### Device list
```json
[
  {
    "id": "6921b6f43382f447bc480854",
    "name": "Canal - G9 4K"
  },
  {
    "id": "6921b6823382f447bc480742",
    "name": "Panasonic - 3869"
  }
]
```

### Macro list
```json
[
  {
    "id": "69236c743382f447bc481367",
    "name": "Watch TV 1"
  }
]
```

### Battery status
```
85%
```

### Key event
```
button:13
```

## Développement

Pour contribuer au développement :
1. Fork le repository
2. Créer une branche feature
3. Tester vos modifications
4. Soumettre une Pull Request

## Licence

MIT License

## Auteur

Développé par [@daangel27](https://github.com/daangel27)

## Changelog

### Version 1.0.0 (2024)
- Version initiale
- Support complet des sensors (batterie, connexion, touche, macro en cours)
- Création dynamique des boutons pour macros et commandes
- Configuration via UI
- Support multi-télécommandes
- Traductions FR/EN
