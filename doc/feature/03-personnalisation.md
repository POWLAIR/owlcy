# Personnalisation & adaptabilité

Principe : **tout ce que l'utilisateur voit ou fait tourner est un fichier de config qu'il peut modifier.**

## Niveaux de personnalisation

| Niveau | Quoi | Comment |
|---|---|---|
| 1. Réglages | Owls actives, raccourcis, position du perchoir, modèle par défaut | Écran de réglages |
| 2. Paramètres | Les `params` d'une pipeline (sources, sujets, horaires) | Formulaire auto-généré |
| 3. Apparence | Skin de chaque Owl, thème de chaque pipeline, sons | Éditeur de skin |
| 4. Comportement | Prompt/personnalité d'une Owl, permissions, étapes de pipeline | YAML ou éditeur |
| 5. Extension | Nouvelles skills, nouvelles Owls | Code, ou via la Forgeronne |

## Arborescence utilisateur (proposition)

```
~/.owlcy/                 (ou %APPDATA%\Owlcy sous Windows)
├── config.yaml            réglages globaux
├── owls/<id>/owl.yaml
├── pipelines/<id>/pipeline.yaml
├── integrations/<id>/owlcy.yaml + serveur MCP
├── skills/<id>/SKILL.md   (standard Agent Skills)
├── skins/<id>/skin.yaml + sons optionnels
├── memory/                mémoire par Owl
├── runs/                  historique (SQLite)
└── packages/              paquets installés (partagés)
```

- Tout est **versionnable avec git** (hors secrets et runs).
- Les secrets ne sont jamais dans ces fichiers : on référence `secret-ref: notion` et la valeur est dans le coffre de l'OS (Windows Credential Manager / Keychain / libsecret).
- ⚠️ Les fichiers mémoire sont écrits **uniquement via l'API du moteur**, jamais directement par une intégration (leçon OpenClaw : keyloggers injectés dans la mémoire). Voir [`architecture/02-securite.md`](../architecture/02-securite.md).

## Formulaires générés (inspiration Home Assistant)

Home Assistant génère ses écrans de configuration (*config flows*) depuis le manifeste des intégrations. Même principe ici : les `params` d'une pipeline et les réglages d'une intégration sont en **JSON Schema** → formulaire généré automatiquement. Même schéma = validation + formulaire + aide pour l'IA qui génère des configs.

## Rechargement à chaud

Modifier un fichier → Owlcy le revalide (JSON Schema) et le recharge sans redémarrer. En cas d'erreur, la chouette affiche une pelote avec le message de validation.

## Profils

Possibilité de profils (« Pro », « Perso », « Week-end ») qui activent un sous-ensemble d'Owls et de pipelines.
