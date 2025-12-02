# Guide d'installation - Haptique RS90 Remote

## Étape 1 : Prérequis

### 1.1 Vérifier MQTT
Avant d'installer l'intégration, assurez-vous que MQTT est configuré dans Home Assistant.

**Pour vérifier :**
1. Allez dans **Paramètres** → **Appareils et services**
2. Recherchez "MQTT" dans la liste des intégrations
3. Si MQTT n'est pas configuré, installez Mosquitto broker :
   - **Paramètres** → **Modules complémentaires** → **Boutique des modules complémentaires**
   - Recherchez "Mosquitto broker" et installez-le
   - Démarrez le module et activez "Démarrage au boot"

### 1.2 Identifier votre Remote ID
1. Ouvrez MQTT Explorer ou utilisez les outils de développement HA
2. Cherchez les topics commençant par `Haptique/`
3. Le Remote ID se trouve juste après : `Haptique/{RemoteID}/status`
4. Notez ce Remote ID (ex: `4deba8d571ace2a0`)

## Étape 2 : Installation de l'intégration

### Option A : Via HACS (recommandé)

1. **Installer HACS** (si pas déjà fait)
   - Suivez les instructions sur https://hacs.xyz/docs/setup/download

2. **Ajouter le dépôt personnalisé**
   - Ouvrez HACS
   - Cliquez sur les **3 points** en haut à droite
   - Sélectionnez **Dépôts personnalisés**
   - URL : `https://github.com/daangel27/haptique_rs90`
   - Catégorie : **Integration**
   - Cliquez **Ajouter**

3. **Installer l'intégration**
   - Dans HACS, recherchez "Haptique RS90"
   - Cliquez sur **Télécharger**
   - Choisissez la dernière version
   - Cliquez **Télécharger**

4. **Redémarrer Home Assistant**
   - **Paramètres** → **Système** → **Redémarrer**

### Option B : Installation manuelle

1. **Télécharger les fichiers**
   - Téléchargez la dernière version depuis GitHub
   - Dézippez l'archive

2. **Copier les fichiers**
   ```bash
   # Connectez-vous en SSH à votre Home Assistant
   cd /config
   mkdir -p custom_components/haptique_rs90
   
   # Copiez tous les fichiers du dossier haptique_rs90 vers :
   # /config/custom_components/haptique_rs90/
   ```

3. **Vérifier la structure**
   ```
   /config/custom_components/haptique_rs90/
   ├── __init__.py
   ├── manifest.json
   ├── const.py
   ├── coordinator.py
   ├── config_flow.py
   ├── sensor.py
   ├── binary_sensor.py
   ├── button.py
   ├── strings.json
   ├── services.yaml
   └── translations/
       ├── en.json
       └── fr.json
   ```

4. **Redémarrer Home Assistant**

## Étape 3 : Configuration

1. **Ajouter l'intégration**
   - **Paramètres** → **Appareils et services**
   - Cliquez sur **+ Ajouter une intégration**
   - Recherchez "Haptique RS90 Remote"
   - Cliquez dessus

2. **Remplir le formulaire**
   - **Remote ID** : Entrez le Remote ID noté à l'étape 1.2
   - **Nom personnalisé** (optionnel) : Par exemple "Télécommande salon"
   - Cliquez **Soumettre**

3. **Vérification**
   - L'intégration devrait apparaître dans vos appareils
   - Cliquez dessus pour voir toutes les entités créées

## Étape 4 : Vérification des entités

### Sensors créés automatiquement :
✅ `binary_sensor.rs90_connection` - État de connexion
✅ `sensor.rs90_battery` - Niveau de batterie
✅ `sensor.rs90_last_key_pressed` - Dernière touche pressée
✅ `sensor.rs90_running_macro` - Macro en cours

### Boutons créés dynamiquement :
✅ `button.rs90_macro_*` - Un par macro
✅ `button.rs90_*_*` - Un par commande de chaque appareil

**Note :** Les boutons peuvent prendre quelques secondes à apparaître après la configuration initiale.

## Étape 5 : Test

### Test 1 : Vérifier la connexion
1. Allez dans **Outils de développement** → **États**
2. Cherchez `binary_sensor.rs90_connection`
3. L'état devrait être **on**

### Test 2 : Vérifier la batterie
1. Cherchez `sensor.rs90_battery`
2. Vous devriez voir un pourcentage (ex: 85%)

### Test 3 : Tester un bouton
1. Dans **Outils de développement** → **Services**
2. Service : `button.press`
3. Entité : Choisissez un bouton de macro ou de commande
4. Cliquez **Appeler le service**
5. La commande devrait être envoyée

### Test 4 : Bouton physique
1. Appuyez sur un bouton physique de la télécommande
2. Vérifiez `sensor.rs90_last_key_pressed`
3. Il devrait afficher le numéro du bouton

## Étape 6 : Utilisation dans le dashboard

### Créer une carte simple :

```yaml
type: entities
title: Télécommande RS90
entities:
  - entity: binary_sensor.rs90_connection
    name: État
  - entity: sensor.rs90_battery
    name: Batterie
  - entity: sensor.rs90_last_key_pressed
    name: Dernière touche
  - entity: sensor.rs90_running_macro
    name: En cours
```

### Créer des boutons de contrôle :

```yaml
type: horizontal-stack
cards:
  - type: button
    entity: button.rs90_macro_watch_tv_1
    name: Regarder TV
    icon: mdi:television
    tap_action:
      action: call-service
      service: button.press
      target:
        entity_id: button.rs90_macro_watch_tv_1
```

## Dépannage

### Problème : L'intégration n'apparaît pas
**Solution :**
- Vérifiez que les fichiers sont dans `/config/custom_components/haptique_rs90/`
- Redémarrez Home Assistant complètement
- Vérifiez les logs : **Paramètres** → **Système** → **Logs**

### Problème : "MQTT not configured"
**Solution :**
- Installez et configurez MQTT Mosquitto broker
- Redémarrez Home Assistant
- Réessayez d'ajouter l'intégration

### Problème : Les boutons ne se créent pas
**Solution :**
- Attendez 30 secondes après l'ajout
- Vérifiez que la télécommande publie sur MQTT
- Utilisez MQTT Explorer pour voir les topics :
  ```
  Haptique/{RemoteID}/device/list
  Haptique/{RemoteID}/macro/list
  ```
- Si les topics sont vides, configurez des appareils/macros sur la télécommande

### Problème : Les commandes ne fonctionnent pas
**Solution :**
- Vérifiez `binary_sensor.rs90_connection` est **on**
- Vérifiez les logs MQTT pour voir si les messages sont publiés
- Testez manuellement avec MQTT Explorer :
  ```
  Topic: Haptique/{RemoteID}/device/{device_name}/trigger
  Payload: {command_name}
  ```

### Problème : "Device already configured"
**Solution :**
- Ce Remote ID est déjà configuré
- Pour reconfigurer : supprimez d'abord l'ancienne intégration
- Ou utilisez un Remote ID différent pour une autre télécommande

## Support

Pour obtenir de l'aide :
1. Consultez la documentation complète dans le README.md
2. Vérifiez les exemples dans `example_configuration.yaml`
3. Ouvrez une issue sur GitHub : https://github.com/daangel27/haptique_rs90/issues

## Mise à jour

### Via HACS :
1. HACS → Intégrations
2. Recherchez "Haptique RS90"
3. Cliquez **Mettre à jour** si disponible
4. Redémarrez Home Assistant

### Manuellement :
1. Téléchargez la nouvelle version
2. Remplacez les fichiers dans `/config/custom_components/haptique_rs90/`
3. Redémarrez Home Assistant

## Désinstallation

1. **Supprimer l'intégration**
   - **Paramètres** → **Appareils et services**
   - Trouvez "Haptique RS90"
   - Cliquez sur les **3 points** → **Supprimer**

2. **Supprimer les fichiers** (optionnel)
   ```bash
   rm -rf /config/custom_components/haptique_rs90
   ```

3. **Redémarrer Home Assistant**
