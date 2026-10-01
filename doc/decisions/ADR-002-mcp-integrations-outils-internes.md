# ADR-002 — MCP pour les intégrations tierces, outils de base dans le moteur

- **Date** : 2026-10-01
- **Statut** : proposé
- **Questions liées** : Q2, Q23

## Contexte

Les Owls ont besoin d'outils : ceux d'Owlcy (`owl.say`, `fs.*`, `llm.*`, `http.fetch`) et ceux de services tiers (Notion, RSS, Claude Code…). La question est de savoir si tout doit passer par MCP, avec un processus par intégration, ou si les outils de base doivent rester dans le moteur.

## Options envisagées

1. **Tout en MCP**, un processus par outil : un modèle unique, mais ~50 Mo de RAM par serveur (T1) et un démarrage de ~400 ms (Python).
2. **Hybride** : les outils de base sont des fonctions du moteur, exposées au LLM comme n'importe quel outil ; MCP stdio sert aux intégrations tierces et isolées ; MCP Apps sert aux cartes d'interface.
3. Format de plugin maison : écarté, car il couperait Owlcy de l'écosystème MCP et Agent Skills.

## Décision

**Option 2.**

| Preuve | Résultat | Source |
|---|---|---|
| Latence d'un appel MCP stdio | 2,7 ms p50 / 3,2 ms p95 : négligeable | T1 |
| RAM par serveur MCP (Python FastMCP) | **~54 Mo** : 10 intégrations ≈ 540 Mo, trop pour tout passer en MCP | T1 |
| Validation humaine | élicitation (spec 2025-11-25) OK ; **MRTR `input_required` (2026-07-28) OK** avec le SDK TS v2 | T1, T7 |
| Côté moteur, validation par l'AI SDK | `needsApproval` bloque l'outil MCP tant que l'utilisateur n'a pas répondu | T5 |
| MCP Apps (cartes UI) | sandbox iframe OK dans Chromium : DOM hôte, réseau et `localStorage` bloqués | T2 |

## Conséquences

- Intégrations MCP **démarrées à la demande et arrêtées après inactivité** : c'est obligatoire, pas une optimisation.
- Deux canaux de validation à unifier dans la bulle : `needsApproval` (outils du moteur et outils MCP vus par le LLM) et élicitation/MRTR (demandée par le serveur MCP lui-même).
- Côté serveur, utiliser `serveStdio(factory)` du SDK v2 (et non `server.connect(new StdioServerTransport())`) : c'est la seule façon de servir la révision 2026-07-28 en stdio. Côté client, activer `versionNegotiation: { mode: 'auto' }`, sinon le client reste en 2025-11-25 (T7).
- MRTR coûte ~80 ms par aller-retour, contre ~10 ms pour l'élicitation 2025 (T7). C'est invisible face au temps de réaction humain.
- **À vérifier dans Tauri** (W1.11–12, Q23) : une iframe `srcdoc` passe-t-elle avec une CSP stricte ? Sinon, servir les cartes depuis une origine dédiée. L'AppBridge officiel (`@modelcontextprotocol/ext-apps` 2.0.3) est désormais installable et reste l'option de référence.
