# Nouveautés v1.7.0

**Date de sortie :** Janvier 2026  
**Type :** Version majeure avec nouvelles fonctionnalités  
**Changements incompatibles :** Aucun ✅

---

## 🎯 Fonctionnalités principales

### 1. Détection des boutons basée sur événements ⚡

**Problème résolu :** Appuyer deux fois sur le même bouton ne déclenchait pas les automatisations.

**Maintenant :** Chaque appui de bouton déclenche un événement, même les appuis répétés !

```yaml
automation:
  trigger:
    - platform: event
      event_type: haptique_rs90_key_pressed
      event_data:
        button: 13
```

**Avantages :**
- ✅ Fonctionne avec les appuis répétés
- ✅ Double fonctionnalité : macro RS90 + automatisation HA simultanément
- ✅ Données complètes : remote_id, device_id, button, timestamp

---

### 2. Déclencheurs d'appareil (Sans YAML !) 🎮

**Créez des automatisations visuellement** dans l'interface Home Assistant :

1. Ajouter une automatisation → Ajouter un déclencheur → **Appareil**
2. Sélectionnez **RS90 Remote**
3. Choisissez **Button pressed** → Sélectionnez le bouton (1-24)
4. Ajoutez des actions → Enregistrez

**C'est tout !** Pas de YAML, pas de complexité.

**Avantages :**
- ✅ 24 boutons disponibles dans le menu déroulant
- ✅ Constructeur d'automatisations natif Home Assistant
- ✅ Parfait pour les débutants

---

### 3. Synchronisation de l'état des macros 🔄

**Problème résolu :** Les switches ne se mettaient pas à jour quand déclenchés depuis la télécommande RS90.

**Maintenant :** Les switches affichent l'état correct quelle que soit la source !

**Technique :**
- Nouveau topic MQTT : `macro/{nom}/status` (publié par RS90)
- Séparation propre commande/état
- Nécessite une mise à jour firmware RS90 à venir

**⚠️ Note :** Contactez le support Haptique pour la disponibilité du firmware.

---

### 4. Rafraîchissement intelligent de la batterie 🔋

**Plusieurs améliorations :**

**Rafraîchissement automatique à la reconnexion :**
- RS90 se réveille → Niveau de batterie demandé immédiatement
- Jusqu'à 6x plus de mises à jour fréquentes hors socle

**Protection anti-spam :**
- Minimum 5 minutes entre les rafraîchissements
- Évite le spam lors de connexions instables

**Intervalle réduit :**
- Rafraîchissement périodique : Toutes les 30 minutes (au lieu de 60)

**Fréquence de rafraîchissement :**
- Sur socle (toujours en ligne) : Toutes les 30 min
- Hors socle (veille/réveil ~10 min) : Toutes les ~10 min au réveil
- Instable (<5 min reconnexion) : Max 1 par 5 min (limité)

---

### 5. RemoteID MQTT exposé 📍

**Accès facile pour le débogage :**

```yaml
sensor.rs90_info_summary:
  rs90_id: "9b974..."              # ID Appareil HA
  rs90_remote_id: "3d5d95aa3a7f7b20"  # RemoteID MQTT ✨
```

Trouvez instantanément votre RemoteID MQTT pour les opérations manuelles.

---

## 🎉 Révolution : Double fonctionnalité

**Un seul appui de bouton RS90 fait DEUX choses :**

1. ✅ **Exécute la macro RS90** (contrôle IR/RF)
2. ✅ **Déclenche l'automatisation Home Assistant** (contrôle maison intelligente)

**Exemple :** Appui Bouton 13
- 📺 Allume la TV via IR (macro RS90)
- 💡 Tamise les lumières (automatisation HA)
- 🔊 Configure Sonos (automatisation HA)
- 🌡️ Ajuste le thermostat (automatisation HA)

**Tout depuis UN SEUL appui !**

---

## 🔧 Autres améliorations

- ✅ Rafraîchissement batterie ajouté au service `refresh_lists`
- ✅ Logs améliorés pour les mises à jour de batterie
- ✅ Coordinateur amélioré avec suivi device_id
- ✅ Meilleurs messages d'erreur

---

## ⚠️ Changements incompatibles

**Aucun !** Cette version est entièrement rétrocompatible avec v1.5.1.

Toutes les automatisations, scripts et configurations existants continuent de fonctionner.

---

## 📋 Prérequis

- **Home Assistant :** 2024.1.0 ou plus récent
- **MQTT :** Configuré et fonctionnel
- **Firmware RS90 :** Dernière version recommandée
  - Sync état macros nécessite MAJ firmware à venir
  - Toutes les autres fonctionnalités fonctionnent avec le firmware actuel

---

## 🚀 Étapes de mise à jour

### Si vous utilisez HACS :

1. Ouvrez **HACS** → **Intégrations**
2. Trouvez **Haptique RS90**
3. Cliquez sur **Mettre à jour**
4. Redémarrez Home Assistant

### Si vous utilisez l'installation manuelle :

1. Téléchargez [v1.7.0](https://github.com/daangel27/haptique_rs90/releases/tag/v1.7.0)
2. Extrayez dans `/config/custom_components/haptique_rs90/`
3. Redémarrez Home Assistant

**C'est tout !** Aucun changement de configuration nécessaire.

---

## 💡 Commencer avec les nouvelles fonctionnalités

### Essayez les déclencheurs d'appareil (Facile)

1. **Paramètres** → **Automatisations** → **Ajouter une automatisation**
2. **Ajouter un déclencheur** → **Appareil** → Sélectionnez RS90
3. **Button pressed** → Choisissez le numéro de bouton
4. Ajoutez une action → Enregistrez
5. Appuyez sur le bouton du RS90 → L'automatisation se déclenche ! 🎉

### Essayez les événements (Avancé)

```yaml
automation:
  - alias: "Bouton multi-actions"
    trigger:
      - platform: event
        event_type: haptique_rs90_key_pressed
        event_data:
          button: 13
    action:
      - service: light.toggle
        target:
          entity_id: light.salon
      - service: notify.mobile_app
        data:
          message: "Bouton 13 appuyé !"
```

### Surveillez mieux la batterie

La batterie se met à jour maintenant :
- ✅ Toutes les 30 minutes (automatique)
- ✅ Au réveil du RS90 (automatique)
- ✅ Via appel de service (manuel)

Aucune action nécessaire - profitez simplement des mises à jour plus fréquentes !

---

## 📚 Documentation

- **[README_FR.md](README_FR.md)** - Guide complet de l'intégration
- **[CHANGELOG_FR.md](CHANGELOG_FR.md)** - Changements techniques détaillés
- **[Versions GitHub](https://github.com/daangel27/haptique_rs90/releases)** - Téléchargement et notes de version

---

## 🙏 Remerciements

Merci à :
- **Support Haptique** pour l'implémentation du topic `/status` et l'excellente collaboration
- **@Benz63Amg** pour avoir signalé l'issue #35 et validé la solution
- **Communauté Home Assistant** pour les retours et tests

---

## 🆘 Besoin d'aide ?

- 📖 [Documentation complète](README_FR.md)
- 🐛 [Signaler des problèmes](https://github.com/daangel27/haptique_rs90/issues)
- 💬 [Discussions](https://github.com/daangel27/haptique_rs90/discussions)

---

**Profitez de la v1.7.0 !** 🎉
