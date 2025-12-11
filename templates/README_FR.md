# Template de Carte Boutons pour Appareils

Générez une magnifique carte télécommande avec toutes les commandes disponibles pour n'importe quel appareil contrôlé par votre Haptique RS90.

![Exemple de carte boutons](../documentation/screenshots/device_buttons_card.png)
*Exemple : Télécommande complète pour Canal Plus*

---

## 🎯 Ce que fait ce template

Ce template génère automatiquement une **carte en grille** contenant **un bouton pour chaque commande** disponible sur votre appareil. Quand vous appuyez sur un bouton :

1. 🖱️ **Bouton pressé** dans le dashboard Home Assistant
2. 📡 **Service appelé** : `haptique_rs90.trigger_device_command`
3. 📤 **Message MQTT envoyé** vers votre télécommande Haptique RS90
4. 📻 **Commande IR transmise** du RS90 vers votre appareil réel

**Résultat** : Votre TV, ampli ou tout appareil IR répond instantanément !

---

## 📋 Prérequis

Avant d'utiliser ce template, vous devez avoir :

1. ✅ **Intégration Haptique RS90** installée et configurée
2. ✅ **Capteur de commandes** disponible (créé automatiquement par l'intégration)
3. ✅ **card-mod** installé (pour le style 3D des boutons)

### Installation de card-mod (Optionnel mais recommandé)

Le template utilise **card-mod** pour le bel effet 3D des boutons. Sans lui, les boutons fonctionneront mais auront un style basique.

Installation via HACS :
1. Ouvrez HACS → Frontend
2. Recherchez "card-mod"
3. Installez et redémarrez Home Assistant

**Note** : Le template fonctionne sans card-mod, mais les boutons n'auront pas l'effet 3D.

---

## 🔍 Trouver les informations requises

Vous avez besoin de **3 informations** pour utiliser ce template :

### 1. Capteur de commandes de l'appareil

**Où le trouver** :
- Allez dans **Paramètres** → **Appareils et services**
- Cliquez sur **Haptique RS90**
- Cliquez sur votre télécommande RS90
- Regardez dans la section **Diagnostic**
- Trouvez les capteurs nommés : `Commands - {Nom Appareil}`

**Exemple** : `sensor.commands_canal_g9_4k`

**Format** : `sensor.commands_{nom_appareil}` (espaces remplacés par underscores, minuscules)

### 2. ID du RS90 (Home Assistant)

**Où le trouver** :
- Même page appareil que ci-dessus
- Regardez l'URL du navigateur : `http://homeassistant.local:8123/config/devices/device/6f99751e78b5a07de72d549143e2975c`
- Copiez le long ID à la fin : `6f99751e78b5a07de72d549143e2975c`

**Méthode alternative** : Utilisez le sélecteur UI dans Services (voir [GUIDE_DEVICE_ID.md](../documentation/GUIDE_DEVICE_ID.md))

### 3. Nom de l'appareil (Exact)

**Où le trouver** :
- Allez sur le capteur de commandes (de l'étape 1)
- Cliquez dessus pour voir les détails
- Regardez la section **Attributs**
- Trouvez **Device name** : `Canal - G9 4K`

**Important** : Utilisez le **nom exact** incluant espaces, majuscules et caractères spéciaux !

---

## 🚀 Guide étape par étape

### Étape 1 : Copier le template

Copiez le code du template depuis [`templates/device_buttons_card.yaml`](device_buttons_card.yaml)

### Étape 2 : Remplacer les valeurs

Vous devez remplacer **3 valeurs** dans le template :

```yaml
{% for cmd in state_attr('sensor.commands_your_device_name', 'commands') %}
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                              1️⃣ Remplacez par VOTRE nom de capteur
```

```yaml
device_id: "YOUR_RS90_DEVICE_ID_HERE"
            ^^^^^^^^^^^^^^^^^^^^^^^^^
            2️⃣ Remplacez par VOTRE ID d'appareil
```

```yaml
device_name: "Your Device Name"
              ^^^^^^^^^^^^^^^^^
              3️⃣ Remplacez par VOTRE nom exact d'appareil
```

**Exemple avec des vraies valeurs** :

```yaml
# Avant (template avec placeholders)
{% for cmd in state_attr('sensor.commands_your_device_name', 'commands') %}
  device_id: "YOUR_RS90_DEVICE_ID_HERE"
  device_name: "Your Device Name"

# Après (avec vos vraies valeurs)
{% for cmd in state_attr('sensor.commands_canal_g9_4k', 'commands') %}
  device_id: "6f99751e78b5a07de72d549143e2975c"
  device_name: "Canal - G9 4K"
```

### Étape 3 : Générer le code de la carte

1. Allez dans **Outils de développement** → **Template** (URL : `/developer-tools/template`)
2. **Collez votre template modifié** dans l'éditeur de gauche
3. Attendez que le résultat apparaisse dans le panneau **Result** à droite
4. **Copiez tout le code résultat** (il sera beaucoup plus long que le template)

![Éditeur de template](../documentation/screenshots/template_editor.png)
*L'éditeur de template génère le code final de la carte*

### Étape 4 : Ajouter à votre dashboard

1. Allez sur n'importe quel dashboard
2. Cliquez sur **Modifier le tableau de bord** (en haut à droite)
3. Cliquez sur **Ajouter une carte**
4. Descendez et sélectionnez **Manuel** (en bas)
5. **Collez le code** que vous avez copié du Résultat du Template
6. Cliquez sur **Enregistrer**

Terminé ! 🎉 Vous avez maintenant une belle carte télécommande !

---

## 🎨 Personnalisation

### Changer la disposition de la grille

Modifiez la valeur `columns` pour changer la disposition des boutons :

```yaml
columns: 4  # 4 colonnes (par défaut, bon pour mobile)
columns: 5  # 5 colonnes (plus compact)
columns: 3  # 3 colonnes (boutons plus grands)
```

### Changer les couleurs

Modifiez les variables CSS :

```yaml
--mdc-theme-primary: #1e3a8a;      # Couleur principale du bouton (bleu)
--mdc-theme-secondary: #0f172a;    # Fin du dégradé (bleu foncé)
```

**Schémas de couleurs populaires** :

**Thème rouge** (pour appareils média/power) :
```yaml
--mdc-theme-primary: #dc2626;
--mdc-theme-secondary: #7f1d1d;
```

**Thème vert** (pour appareils éco/maison) :
```yaml
--mdc-theme-primary: #16a34a;
--mdc-theme-secondary: #14532d;
```

**Thème violet** (pour divertissement) :
```yaml
--mdc-theme-primary: #9333ea;
--mdc-theme-secondary: #581c87;
```

### Supprimer l'effet 3D

Si vous n'avez pas card-mod ou voulez des boutons plats, supprimez simplement toute la section `card_mod:` du template.

---

## 🔧 Dépannage

### Les boutons n'apparaissent pas

**Problème** : Le template génère un résultat vide
**Solution** :
- Vérifiez que le nom du capteur est correct (doit commencer par `sensor.commands_`)
- Vérifiez que le capteur existe dans **Outils de développement** → **États**

### Les boutons ne fonctionnent pas

**Problème** : Cliquer sur les boutons ne fait rien
**Solution** :
- Vérifiez que `device_id` est correct (vérifiez l'URL dans la page appareil)
- Vérifiez que `device_name` est **exact** (sensible à la casse, incluez espaces/tirets)
- Vérifiez que votre RS90 est en ligne (Capteur Connection = ON)

### Les boutons ont un style basique (Pas d'effet 3D)

**Problème** : Les boutons fonctionnent mais sont plats
**Solution** : Installez **card-mod** via HACS → Frontend

### Mauvaises commandes affichées

**Problème** : Les boutons montrent les commandes d'un mauvais appareil
**Solution** : Vous avez utilisé le mauvais nom de capteur. Chaque appareil a son propre `sensor.commands_{appareil}`.

---

## 📸 Captures d'écran

### Exemples de cartes générées

<table>
<tr>
<td width="50%">
<img src="../documentation/screenshots/device_buttons_card.png" alt="Télécommande Canal Plus" />
<p align="center"><em>Canal Plus - Télécommande complète avec 31 boutons</em></p>
</td>
<td width="50%">
<p><strong>Fonctionnalités :</strong></p>
<ul>
<li>✅ Grille 4 colonnes</li>
<li>✅ Effet 3D des boutons</li>
<li>✅ Animation de pression</li>
<li>✅ Auto-généré depuis le capteur</li>
<li>✅ Fonctionne avec n'importe quel appareil</li>
</ul>
</td>
</tr>
</table>

---

## 💡 Conseils et bonnes pratiques

### Organiser plusieurs appareils

Créez **une carte par appareil** et organisez-les en **onglets** ou **piles verticales** :

```yaml
type: vertical-stack
title: Divertissement Salon
cards:
  - type: markdown
    content: "## Télécommande TV"
  - # Votre carte boutons TV ici
  
  - type: markdown
    content: "## Système Audio"
  - # Votre carte boutons audio ici
```

### Ajouter un titre à la carte

Enveloppez votre carte dans une pile verticale avec un titre :

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: "# 📺 Canal Plus"
    card_mod:
      style: |
        ha-card {
          background: none;
          box-shadow: none;
          text-align: center;
        }
  - # Votre carte boutons ici
```

### Utiliser des cartes conditionnelles

Affichez différentes télécommandes selon ce qui est en cours de lecture :

```yaml
type: conditional
conditions:
  - entity: media_player.tv
    state: "on"
card:
  # Votre carte télécommande TV ici
```

---

## 🎬 Exemple : Configuration complète

Voici un exemple complet pour un appareil "Canal - G9 4K" :

**1. Mes informations** :
- Capteur : `sensor.commands_canal_g9_4k`
- ID appareil : `6f99751e78b5a07de72d549143e2975c`
- Nom appareil : `Canal - G9 4K`

**2. Template avec mes valeurs** (coller dans l'Éditeur de Template) :

```yaml
type: grid
columns: 4
square: false
cards:
  {% for cmd in state_attr('sensor.commands_canal_g9_4k', 'commands') %}
  - type: button
    name: "{{ cmd.replace('_', ' ') }}"
    tap_action:
      action: call-service
      service: haptique_rs90.trigger_device_command
      data:
        device_id: "6f99751e78b5a07de72d549143e2975c"
        device_name: "Canal - G9 4K"
        command_name: "{{ cmd }}"
    # ... reste du style ...
  {% endfor %}
```

**3. Résultat** : Copiez le code généré 

**4. Ajoutez au dashboard** : Collez dans une carte Manuel

**5. Terminé !** 🎉

---

## 📦 Fichiers

- **Template** : [`device_buttons_card.yaml`](device_buttons_card.yaml)
- **Exemple** : [`example_canal_plus.yaml`](example_canal_plus.yaml) (avec vraies valeurs)
- **Screenshot** : [device_buttons_card.png](../documentation/screenshots/device_buttons_card.png)

---

## 🆘 Besoin d'aide ?

- 📖 [Documentation principale](../README_FR.md)
- 🔍 [Comment trouver le Device ID](../documentation/GUIDE_DEVICE_ID.md)
- 🐛 [Signaler un problème](https://github.com/daangel27/haptique_rs90/issues)
- 💬 [Discussions](https://github.com/daangel27/haptique_rs90/discussions)

---

**Version du Template** : 1.0  
**Compatible avec** : Haptique RS90 Integration v1.2.5+  
**Dernière mise à jour** : Décembre 2025
