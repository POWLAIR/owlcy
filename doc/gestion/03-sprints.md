<!-- Fichier GÉNÉRÉ par scripts/github_bootstrap.py depuis gestion/backlog.yaml — ne pas modifier à la main -->

# Plan de sprints

Un sprint = **un résultat** : ce que je peux voir et utiliser à la fin, de bout en bout. Le résultat est le titre de l'itération dans le GitHub Project ; la démo est jouée à la revue.

Sprints de 14 jours (Sprint 0 : 3 semaines) · capacité supposée **12 points** / 2 semaines, à ajuster après le Sprint 1 selon la vélocité réelle.

| Sprint | Dates | Résultat | Points / capacité | Release |
|---|---|---|---|---|
| S0 | 05/10 → 23/10/2026 | Je sais si Owlcy est faisable (GO / NO-GO) | 16 / 18 |  |
| S1 | 26/10 → 06/11/2026 | La chouette apparaît sur mon bureau | 12 / 12 |  |
| S2 | 09/11 → 20/11/2026 | La chouette vit et me demande la permission | 12 / 12 |  |
| S3 | 23/11 → 04/12/2026 | Je lance une pipeline YAML et la chouette me répond | 12 / 12 |  |
| S4 | 07/12 → 18/12/2026 | La chouette lit mes flux et me les résume, avec mon accord | 12 / 12 |  |
| S5 | 21/12 → 01/01/2027 | La Veilleuse publie ma veille chaque matin | 12 / 12 | **v0.1.0** |
| S6 | 04/01 → 15/01/2027 | Je vois ce qu'ont fait mes Owls et je relance une erreur | 11 / 12 |  |
| S7 | 18/01 → 29/01/2027 | Je crée une pipeline depuis un modèle et je la déclenche comme je veux | 10 / 12 |  |
| S8 | 01/02 → 12/02/2027 | Je confie une tâche libre à une Owl, qui reste dans ses limites | 12 / 12 | **v0.2.0** |
| S9 | 15/02 → 26/02/2027 | Je valide les commandes de Claude Code depuis la chouette | 6 / 12 |  |
| S10 | 01/03 → 12/03/2027 | Chaque Owl a sa propre apparence | 8 / 12 |  |
| S11 | 15/03 → 26/03/2027 | Je vois mes pipelines en schéma et la chouette suit le run | 11 / 12 | **v0.3.0** |
| S12 | 29/03 → 09/04/2027 | Une Owl peut utiliser Hermes comme cerveau | 8 / 12 |  |
| S13 | 12/04 → 23/04/2027 | Mes Owls se souviennent, et la Forgeronne crée des intégrations | 10 / 12 |  |
| S14 | 26/04 → 07/05/2027 | Owlcy apprend la nuit et je partage mes Owls | 8 / 12 | **v0.4.0** |

## Vers v0.1.0 — MVP — la Veilleuse

### S0 · Je sais si Owlcy est faisable (GO / NO-GO)

05/10/2026 → 23/10/2026 · 16 pts

**Démo de fin de sprint**

- [ ] Les tests W1 à W5 et T5-T7 ont un résultat chiffré dans doc/techno/03-resultats-tests.md
- [ ] Les 4 décisions bloquantes ont leur ADR

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-001 · Créer le dépôt, le GitHub Project et importer le backlog | chore | 1 | P0 | E0 |
| US-002 · W1 — Perchoir Tauri sous Windows (overlay, focus, click-through) | spike | 5 | P0 | E0 |
| US-003 · W2 — Mesurer la mémoire réelle (processus + WebView2) | spike | 1 | P0 | E0 |
| US-004 · W3 — Intégrations WSL via wsl.exe (latence stdio, /mnt/c) | spike | 1 | P1 | E0 |
| US-005 · W4 — Fiabilité des appels d'outils des modèles locaux (RTX 500 Ada, 4 Go de VRAM) | spike | 2 | P0 | E0 |
| US-006 · W5 — Secrets dans le Windows Credential Manager | spike | 1 | P1 | E0 |
| US-007 · T5-T7 — AI SDK 7 + Ollama + MCP, JSONata, SDK MCP TS v2 | spike | 3 | P0 | E0 |
| US-008 · Écrire les ADR des décisions bloquantes (Q1, Q2, Q7, Q13) | chore | 2 | P0 | E0 |

### S1 · La chouette apparaît sur mon bureau

26/10/2026 → 06/11/2026 · 12 pts

**Démo de fin de sprint**

- [ ] J'installe Owlcy depuis l'artefact de la CI
- [ ] La chouette apparaît en bas de l'écran ; je clique à travers et le focus ne bouge pas
- [ ] La fenêtre de debug affiche le ping shell <-> moteur

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-010 · Monorepo et conventions de code | chore | 2 | P0 | E1 |
| US-011 · CI GitHub Actions (Windows) — lint, tests, build | chore | 3 | P0 | E1 |
| US-012 · Le shell lance le moteur et ils se parlent | us | 5 | P0 | E1 |
| US-020 · Voir la chouette sur mon bureau sans qu'elle me gêne | us | 2 | P0 | E2 |

### S2 · La chouette vit et me demande la permission

09/11/2026 → 20/11/2026 · 12 pts

**Démo de fin de sprint**

- [ ] La chouette respire, cligne des yeux et suit mon curseur
- [ ] Depuis la fenêtre de debug, j'envoie approval.requested ; la bulle s'affiche et ma réponse revient en approval.answered
- [ ] Je change de coin et je masque la chouette depuis le tray

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-031 · Bus d'événements moteur -> shell -> UI | us | 2 | P0 | E3 |
| US-021 · Une chouette vivante (respiration, clignements, regard) | us | 3 | P0 | E2 |
| US-022 · Des emotes qui reflètent ce qui se passe | us | 2 | P1 | E2 |
| US-023 · Bulle avec demande de validation | us | 2 | P0 | E2 |
| US-024 · Placer la chouette et la contrôler depuis le tray | us | 3 | P1 | E2 |

### S3 · Je lance une pipeline YAML et la chouette me répond

23/11/2026 → 04/12/2026 · 12 pts

**Démo de fin de sprint**

- [ ] Je pose pipelines/bonjour.yaml (http.fetch -> owl.say) et je la lance
- [ ] La chouette passe en working, puis parle dans sa bulle
- [ ] Je modifie le fichier ; il est rechargé sans redémarrer

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-030 · Configuration en fichiers YAML validés et rechargés à chaud | us | 3 | P0 | E3 |
| US-033 · Outils internes de base | us | 2 | P1 | E3 |
| US-040 · Exécuter une pipeline YAML séquentielle | us | 5 | P0 | E4 |
| US-013 · Journalisation unifiée (shell + moteur) | chore | 2 | P1 | E1 |

### S4 · La chouette lit mes flux et me les résume, avec mon accord

07/12/2026 → 18/12/2026 · 12 pts

**Démo de fin de sprint**

- [ ] Une pipeline lit 3 flux RSS, les résume avec un modèle Ollama et me demande validation dans la bulle
- [ ] J'accepte, la chouette affiche le résumé ; je refuse, le run s'arrête proprement

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-032 · Hôte MCP (démarrage à la demande, arrêt après inactivité) | us | 5 | P0 | E3 |
| US-042 · Étapes LLM avec Ollama et Claude | us | 3 | P0 | E4 |
| US-041 · Étape humaine dans une pipeline | us | 2 | P0 | E4 |
| US-050 · Intégration RSS | us | 2 | P0 | E5 |

### S5 · La Veilleuse publie ma veille chaque matin

21/12/2026 → 01/01/2027 · 12 pts

**Démo de fin de sprint**

- [ ] J'installe la v0.1.0 depuis la GitHub Release
- [ ] À 8 h, le digest de 5 points avec sources est dans ma base Notion, après ma validation
- [ ] Cinq jours ouvrés d'affilée sans intervention

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-051 · Publication dans Notion | us | 2 | P0 | E5 |
| US-052 · Pipeline « Veille du matin » + skill veille-techno | us | 3 | P0 | E5 |
| US-053 · Déclencheur planifié | us | 2 | P0 | E5 |
| US-054 · Permissions par Owl (allow / ask / deny) | us | 2 | P0 | E6 |
| US-043 · Historique des runs en SQLite | us | 2 | P1 | E4 |
| US-055 · Release v0.1.0 (installeur + notes) | chore | 1 | P0 | E1 |

🚀 **Release v0.1.0 — MVP — la Veilleuse**

## Vers v0.2.0 — Extensible — factory, déclencheurs, mode agent

### S6 · Je vois ce qu'ont fait mes Owls et je relance une erreur

04/01/2027 → 15/01/2027 · 11 pts

**Démo de fin de sprint**

- [ ] Je retrouve le run de ce matin et le détail de chaque étape
- [ ] Je provoque une erreur, je clique sur la chouette étourdie et je relance depuis l'étape fautive

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-060 · Liste et détail des runs | us | 5 | P1 | E7 |
| US-061 · Pelote : rapport d'erreur lisible et relance | us | 3 | P1 | E7 |
| US-062 · Réglages et gestion des secrets | us | 3 | P1 | E6 |

### S7 · Je crée une pipeline depuis un modèle et je la déclenche comme je veux

18/01/2027 → 29/01/2027 · 10 pts

**Démo de fin de sprint**

- [ ] Je crée une pipeline depuis un modèle en remplissant un formulaire, sans écrire de YAML
- [ ] Je la lance par raccourci, en glissant un fichier sur la chouette, puis quand un fichier arrive dans Téléchargements

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-070 · Instancier une pipeline depuis un modèle | us | 5 | P1 | E8 |
| US-071 · Déclencheurs hotkey, drop et file_watch | us | 3 | P1 | E8 |
| US-072 · skip_if_unchanged et continuity | us | 2 | P2 | E4 |

### S8 · Je confie une tâche libre à une Owl, qui reste dans ses limites

01/02/2027 → 12/02/2027 · 12 pts

**Démo de fin de sprint**

- [ ] Je demande une tâche libre ; l'Owl choisit ses outils et me demande validation avant une action sensible
- [ ] Un flux RSS piégé ne déclenche aucune action sans validation

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-080 · Mode agent (ToolLoopAgent) borné aux outils de l'Owl | us | 5 | P1 | E9 |
| US-081 · Chargement des Skills (SKILL.md) | us | 2 | P1 | E9 |
| US-082 · Presets d'autonomie et anti-injection | us | 3 | P1 | E6 |
| US-083 · Étapes plan et validate | us | 2 | P2 | E4 |

🚀 **Release v0.2.0 — Extensible — factory, déclencheurs, mode agent**

## Vers v0.3.0 — Vivant — Mécano, skins, éditeur de pipelines

### S9 · Je valide les commandes de Claude Code depuis la chouette

15/02/2027 → 26/02/2027 · 6 pts

**Démo de fin de sprint**

- [ ] Une session Claude Code demande une permission ; je réponds dans la bulle et Claude Code continue
- [ ] Owlcy éteint, Claude Code n'est pas bloqué

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-090 · Recevoir les hooks Claude Code | us | 3 | P2 | E10 |
| US-091 · Valider les permissions Claude Code depuis la bulle | us | 3 | P2 | E10 |

### S10 · Chaque Owl a sa propre apparence

01/03/2027 → 12/03/2027 · 8 pts

**Démo de fin de sprint**

- [ ] Je modifie le skin d'une Owl dans l'éditeur et je vois toutes ses emotes en direct

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-100 · Skins paramétriques + éditeur live | us | 5 | P2 | E11 |
| US-101 · Sons et humeur contextuelle | us | 3 | P3 | E11 |

### S11 · Je vois mes pipelines en schéma et la chouette suit le run

15/03/2027 → 26/03/2027 · 11 pts

**Démo de fin de sprint**

- [ ] J'ouvre la Veille du matin en schéma, je déplace une étape, le YAML est à jour
- [ ] Pendant un run, la chouette avance d'étape en étape

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-110 · Éditeur visuel de pipelines (React Flow) | us | 8 | P2 | E11 |
| US-111 · Mode vivant | us | 3 | P3 | E11 |

🚀 **Release v0.3.0 — Vivant — Mécano, skins, éditeur de pipelines**

## Vers v0.4.0 — Autonome — runtimes externes, apprentissage, paquets

### S12 · Une Owl peut utiliser Hermes comme cerveau

29/03/2027 → 09/04/2027 · 8 pts

**Démo de fin de sprint**

- [ ] Une Owl en runtime hermes fait une tâche ; sa progression et ses approbations passent par la bulle

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-120 · W6 — Spike Owl Hermes (TUI Gateway dans WSL) | spike | 3 | P2 | E12 |
| US-121 · Interface Runtime + adaptateur Hermes | us | 5 | P3 | E12 |

### S13 · Mes Owls se souviennent, et la Forgeronne crée des intégrations

12/04/2027 → 23/04/2027 · 10 pts

**Démo de fin de sprint**

- [ ] Une Owl réutilise une préférence notée dans son carnet la semaine d'avant
- [ ] La Forgeronne génère une intégration, je relis le diff et je l'accepte

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-130 · Carnet et archive par Owl | us | 5 | P2 | E13 |
| US-131 · La Forgeronne génère une intégration | us | 5 | P3 | E13 |

### S14 · Owlcy apprend la nuit et je partage mes Owls

26/04/2027 → 07/05/2027 · 8 pts

**Démo de fin de sprint**

- [ ] Le matin, je trouve des propositions de skills issues du mode nuit
- [ ] J'installe le paquet signé d'une Owl après avoir vu ses permissions

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-140 · Mode nuit : consolidation et propositions de skills | us | 3 | P3 | E14 |
| US-141 · Paquets partageables signés | us | 5 | P3 | E14 |

🚀 **Release v0.4.0 — Autonome — runtimes externes, apprentissage, paquets**
