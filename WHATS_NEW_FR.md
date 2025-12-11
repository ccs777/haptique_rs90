# Nouveautés de la v1.2.6

## 🔧 Version de maintenance

La version 1.2.6 est une version de maintenance axée sur les mises à jour de la documentation et les améliorations de cohérence pour 2025.

---

## 📚 Mises à jour de la documentation

### Mises à jour de l'année
- Toutes les dates de documentation mises à jour de 2024 à 2025
- Année de copyright mise à jour à 2025
- Badges de version actualisés dans tous les fichiers

### Améliorations de cohérence
- Amélioration du formatage dans toute la documentation
- Mise à jour des exemples pour refléter l'année actuelle
- Meilleure clarté dans les guides d'installation
- Meilleure cohérence entre les versions anglaise et française

---

## 🎯 Ce qui reste identique

### Fonctionnalités de base
- ✅ Toutes les fonctionnalités de la v1.2.5 restent inchangées
- ✅ Architecture MQTT 100% pilotée par événements
- ✅ Capteurs de commandes d'appareils
- ✅ Support multilingue (EN/FR)
- ✅ Communications optimisées QoS
- ✅ Fonctionnalité d'auto-découverte

### Aucun changement incompatible
- 🔄 Aucun changement de code
- 🔄 Aucune modification de configuration requise
- 🔄 Toutes les automatisations et scripts continuent de fonctionner
- 🔄 Toutes les entités restent identiques

---

## 💡 Pourquoi cette mise à jour ?

Cette version de maintenance garantit :
1. **Exactitude** : La documentation reflète l'année actuelle (2025)
2. **Cohérence** : Tous les fichiers utilisent la même numérotation de version
3. **Clarté** : Les exemples et les dates sont à jour
4. **Professionnalisme** : Documentation propre et bien maintenue

---

## 🚀 Mise à niveau

### Pour les utilisateurs HACS
La mise à jour apparaîtra automatiquement dans HACS. Il suffit de :
1. Aller dans HACS → Intégrations
2. Trouver "Haptique RS90"
3. Cliquer sur "Mettre à jour"
4. Redémarrer Home Assistant

### Pour les utilisateurs d'installation manuelle
1. Télécharger la v1.2.6 depuis [Releases](https://github.com/daangel27/haptique_rs90/releases)
2. Remplacer les fichiers dans `/config/custom_components/haptique_rs90/`
3. Redémarrer Home Assistant

### Aucune action requise
Comme il n'y a pas de changements fonctionnels, la mise à jour est optionnelle. Votre intégration continuera de fonctionner parfaitement sur la v1.2.5.

---

## 📖 Ensemble complet de fonctionnalités

Rappel de toutes les fonctionnalités disponibles dans la v1.2.6 (reprises de la v1.2.5) :

### Capteurs & Contrôles
- 🔋 Surveillance du niveau de batterie
- 🔌 État de connexion en temps réel
- 🎮 Détection de la dernière touche pressée
- 📱 Gestion de la liste des appareils
- 📋 Commandes disponibles par appareil
- 🎛️ Switches de macro avec états visuels

### Architecture
- ⚡ 100% pilotée par événements (pas de polling)
- 🎯 QoS optimisé (0 pour la surveillance, 1 pour les commandes)
- 🔄 Mises à jour MQTT en temps réel
- 🚀 Découverte automatique de la télécommande
- 🌍 Multilingue (anglais, français)

### Services
- `haptique_rs90.trigger_macro` - Contrôler les macros
- `haptique_rs90.trigger_device_command` - Envoyer des commandes aux appareils

---

## 📞 Support

Besoin d'aide ou vous avez trouvé un problème ?
- 🐛 [Signaler un bug](https://github.com/daangel27/haptique_rs90/issues)
- 💡 [Demander une fonctionnalité](https://github.com/daangel27/haptique_rs90/issues)
- 💬 [Rejoindre les discussions](https://github.com/daangel27/haptique_rs90/discussions)

---

**Version** : 1.2.6  
**Date de sortie** : 11 décembre 2025  
**Type** : Version de maintenance  
**Changements incompatibles** : Aucun  
**Recommandé** : Mise à jour optionnelle
