# Système de mascottes (skins)

## Objectif

Chaque Owl a sa propre chouette, **dans la même DA**. On ne dessine pas une nouvelle mascotte à chaque fois : on **paramètre** la chouette de base.

## Un skin = des paramètres, pas des images

```yaml
# skins/veilleuse-nuit/skin.yaml
id: veilleuse-nuit
base: owl                    # gabarit procédural (owl, plus tard : effraie, petit-duc…)
shape:
  body_roundness: 0.8        # 0 = carré, 1 = rond
  width_ratio: 1.0
  tufts: { size: 0.6, angle: 20 }
  eye_size: 1.1
palette:
  body:  "#2E3A59"
  belly: "#C9D6F2"
  eye:   "#FFD166"
  beak:  "#F4A261"
pattern: stars               # none | feathers | stars | stripes
accessories: [glasses]       # glasses | scarf | hat | headset | …
emotes:
  happy: { eyes: crescent, bounce: 1.2 }
sounds: sounds/night-pack
voice: { tts: fr-FR-calm }   # si synthèse vocale activée
```

## Paramètres exposés

| Famille | Paramètres |
|---|---|
| Forme | rondeur, proportions, taille des aigrettes, taille des yeux, longueur du bec |
| Couleurs | corps, plastron, yeux, bec, pattes, motif |
| Motif | aucun, plumes, étoiles, rayures, taches |
| Accessoires | lunettes, écharpe, casque audio, chapeau, badge d'icône de l'Owl |
| Animation | vitesse de respiration, fréquence de clignement, amplitude des rebonds |
| Sons | pack de sons, volume |

## Éditeur de skin

- Aperçu live de la chouette avec toutes les emotes.
- Curseurs pour chaque paramètre + bouton « aléatoire harmonieux ».
- Génération par IA : « une chouette pirate un peu grincheuse » → proposition de paramètres.
- Export/partage du `skin.yaml`.

## Garde-fous de cohérence

Pour que tout reste « dans la DA » même avec des réglages extrêmes :

- Paramètres **bornés** (pas de rondeur négative, yeux jamais plus petits qu'un seuil).
- Contraste minimum vérifié entre corps, yeux et plastron.
- Les accessoires se posent sur des **points d'ancrage** définis par le gabarit (tête, cou, yeux).

## Choix technique après benchmark (30/09/2026)

| Option | Verdict |
|---|---|
| **SVG procédural** | ✅ **MVP** : chaque paramètre du `skin.yaml` = un attribut SVG. Générable par IA, zéro dépendance. |
| **Rive (hybride)** | 🟡 **Spike comparatif.** Plus viable qu'on ne pensait : le *data binding* accepte **couleurs, nombres, enums, triggers, et échange d'artboards/images** au runtime → un gabarit Rive peut recevoir le skin. Runtime **MIT**, éditeur gratuit pour un individu (payant ≈32-49 $/mois pour les fonctions avancées). Force : state machines d'émotions visuelles. Faiblesse : l'éditeur est un SaaS propriétaire, et l'IA ne peut pas créer de nouvelle forme, seulement modifier des paramètres. |
| Sprites | ❌ Une planche par skin, pas paramétrable. |
| Lottie | ❌ Animations figées. |

**Contrat stable** : quel que soit le moteur de rendu, le `skin.yaml` reste le même. Le moteur de rendu est un adaptateur (`renderer: svg | rive`).

Sources : [Rive data binding](https://rive.app/docs/runtimes/web/data-binding) · [Runtime Rive (MIT)](https://github.com/rive-app/rive-runtime) · [Tarifs Rive](https://www.spotsaas.com/product/rive/pricing)
