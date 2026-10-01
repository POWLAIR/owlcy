<!-- Fichier GÉNÉRÉ par scripts/github_bootstrap.py depuis gestion/backlog.yaml — ne pas modifier à la main -->

# Plan de sprints

Sprints de 14 jours (Sprint 0 : 3 semaines) · capacité supposée **12 points** / 2 semaines, à ajuster après le Sprint 1 selon la vélocité réelle.

| Sprint | Dates | Objectif | Points / capacité | Release |
|---|---|---|---|---|
| S0 | 05/10 → 23/10/2026 | Labo : prouver les points risqués et décider (go / no-go) | 16 / 18 |  |
| S1 | 26/10 → 06/11/2026 | Fondations : dépôt, CI, squelette Tauri + moteur qui se parlent | 12 / 12 |  |
| S2 | 09/11 → 20/11/2026 | Perchoir : la chouette vit sur le bureau Windows | 12 / 12 |  |
| S3 | 23/11 → 04/12/2026 | Moteur : configuration, bus d'événements, hôte MCP | 12 / 12 |  |
| S4 | 07/12 → 18/12/2026 | Pipelines : exécuter une pipeline YAML avec étape humaine et LLM | 12 / 12 |  |
| S5 | 21/12 → 01/01/2027 | MVP : la Veilleuse publie ma veille chaque matin | 12 / 12 | v0.1.0 — MVP — la Veilleuse |
| S6 | 04/01 → 15/01/2027 | Dashboard : voir, comprendre et relancer les runs | 11 / 12 |  |
| S7 | 18/01 → 29/01/2027 | Factory & déclencheurs | 10 / 12 |  |
| S8 | 01/02 → 12/02/2027 | Mode agent, skills et presets d'autonomie | 12 / 12 | v0.2.0 — Extensible — factory, déclencheurs, mode agent |
| S9 | 15/02 → 26/02/2027 | Mécano : piloter les validations Claude Code depuis la chouette | 6 / 12 |  |
| S10 | 01/03 → 12/03/2027 | Skins & personnalité visuelle | 8 / 12 |  |
| S11 | 15/03 → 26/03/2027 | Éditeur de pipelines & mode vivant | 11 / 12 | v0.3.0 — Vivant — Mécano, skins, éditeur de pipelines |
| S12 | 29/03 → 09/04/2027 | Runtimes externes (Hermes) | 8 / 12 |  |
| S13 | 12/04 → 23/04/2027 | Mémoire & Forgeronne | 10 / 12 |  |
| S14 | 26/04 → 07/05/2027 | Mode nuit & paquets partageables | 8 / 12 | v0.4.0 — Autonome — runtimes externes, apprentissage, paquets |

## Sprint 0 — Labo : prouver les points risqués et décider (go / no-go)

05/10/2026 → 23/10/2026 · 16 pts

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

## Sprint 1 — Fondations : dépôt, CI, squelette Tauri + moteur qui se parlent

26/10/2026 → 06/11/2026 · 12 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-010 · Monorepo et conventions de code | chore | 2 | P0 | E1 |
| US-011 · CI GitHub Actions (Windows) — lint, tests, build | chore | 3 | P0 | E1 |
| US-012 · Le shell lance le moteur et ils se parlent | us | 5 | P0 | E1 |
| US-013 · Journalisation unifiée (shell + moteur) | chore | 2 | P1 | E1 |

## Sprint 2 — Perchoir : la chouette vit sur le bureau Windows

09/11/2026 → 20/11/2026 · 12 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-020 · Voir la chouette sur mon bureau sans qu'elle me gêne | us | 5 | P0 | E2 |
| US-021 · Une chouette vivante (respiration, clignements, regard) | us | 3 | P0 | E2 |
| US-022 · Des emotes qui reflètent ce qui se passe | us | 2 | P1 | E2 |
| US-023 · Bulle avec demande de validation | us | 2 | P0 | E2 |

## Sprint 3 — Moteur : configuration, bus d'événements, hôte MCP

23/11/2026 → 04/12/2026 · 12 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-030 · Configuration en fichiers YAML validés et rechargés à chaud | us | 3 | P0 | E3 |
| US-031 · Bus d'événements moteur -> shell -> UI | us | 2 | P0 | E3 |
| US-032 · Hôte MCP (démarrage à la demande, arrêt après inactivité) | us | 5 | P0 | E3 |
| US-033 · Outils internes de base | us | 2 | P1 | E3 |

## Sprint 4 — Pipelines : exécuter une pipeline YAML avec étape humaine et LLM

07/12/2026 → 18/12/2026 · 12 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-040 · Exécuter une pipeline YAML séquentielle | us | 5 | P0 | E4 |
| US-041 · Étape humaine dans une pipeline | us | 2 | P0 | E4 |
| US-042 · Étapes LLM avec Ollama et Claude | us | 3 | P0 | E4 |
| US-043 · Historique des runs en SQLite | us | 2 | P1 | E4 |

## Sprint 5 — MVP : la Veilleuse publie ma veille chaque matin

21/12/2026 → 01/01/2027 · 12 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-050 · Intégration RSS | us | 2 | P0 | E5 |
| US-051 · Publication dans Notion | us | 2 | P0 | E5 |
| US-052 · Pipeline « Veille du matin » + skill veille-techno | us | 3 | P0 | E5 |
| US-053 · Déclencheur planifié | us | 2 | P0 | E5 |
| US-054 · Permissions par Owl (allow / ask / deny) | us | 2 | P0 | E6 |
| US-055 · Release v0.1.0 (installeur + notes) | chore | 1 | P0 | E1 |

🚀 **Release v0.1.0 — MVP — la Veilleuse**

## Sprint 6 — Dashboard : voir, comprendre et relancer les runs

04/01/2027 → 15/01/2027 · 11 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-060 · Liste et détail des runs | us | 5 | P1 | E7 |
| US-061 · Pelote : rapport d'erreur lisible et relance | us | 3 | P1 | E7 |
| US-062 · Réglages et gestion des secrets | us | 3 | P1 | E6 |

## Sprint 7 — Factory & déclencheurs

18/01/2027 → 29/01/2027 · 10 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-070 · Instancier une pipeline depuis un modèle | us | 5 | P1 | E8 |
| US-071 · Déclencheurs hotkey, drop et file_watch | us | 3 | P1 | E8 |
| US-072 · skip_if_unchanged et continuity | us | 2 | P2 | E4 |

## Sprint 8 — Mode agent, skills et presets d'autonomie

01/02/2027 → 12/02/2027 · 12 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-080 · Mode agent (ToolLoopAgent) borné aux outils de l'Owl | us | 5 | P1 | E9 |
| US-081 · Chargement des Skills (SKILL.md) | us | 2 | P1 | E9 |
| US-082 · Presets d'autonomie et anti-injection | us | 3 | P1 | E6 |
| US-083 · Étapes plan et validate | us | 2 | P2 | E4 |

🚀 **Release v0.2.0 — Extensible — factory, déclencheurs, mode agent**

## Sprint 9 — Mécano : piloter les validations Claude Code depuis la chouette

15/02/2027 → 26/02/2027 · 6 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-090 · Recevoir les hooks Claude Code | us | 3 | P2 | E10 |
| US-091 · Valider les permissions Claude Code depuis la bulle | us | 3 | P2 | E10 |

## Sprint 10 — Skins & personnalité visuelle

01/03/2027 → 12/03/2027 · 8 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-100 · Skins paramétriques + éditeur live | us | 5 | P2 | E11 |
| US-101 · Sons et humeur contextuelle | us | 3 | P3 | E11 |

## Sprint 11 — Éditeur de pipelines & mode vivant

15/03/2027 → 26/03/2027 · 11 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-110 · Éditeur visuel de pipelines (React Flow) | us | 8 | P2 | E11 |
| US-111 · Mode vivant | us | 3 | P3 | E11 |

🚀 **Release v0.3.0 — Vivant — Mécano, skins, éditeur de pipelines**

## Sprint 12 — Runtimes externes (Hermes)

29/03/2027 → 09/04/2027 · 8 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-120 · W6 — Spike Owl Hermes (TUI Gateway dans WSL) | spike | 3 | P2 | E12 |
| US-121 · Interface Runtime + adaptateur Hermes | us | 5 | P3 | E12 |

## Sprint 13 — Mémoire & Forgeronne

12/04/2027 → 23/04/2027 · 10 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-130 · Carnet et archive par Owl | us | 5 | P2 | E13 |
| US-131 · La Forgeronne génère une intégration | us | 5 | P3 | E13 |

## Sprint 14 — Mode nuit & paquets partageables

26/04/2027 → 07/05/2027 · 8 pts

| Item | Type | Pts | Prio | Epic |
|---|---|---|---|---|
| US-140 · Mode nuit : consolidation et propositions de skills | us | 3 | P3 | E14 |
| US-141 · Paquets partageables signés | us | 5 | P3 | E14 |

🚀 **Release v0.4.0 — Autonome — runtimes externes, apprentissage, paquets**
