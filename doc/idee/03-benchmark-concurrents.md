# Benchmark des projets proches

Veille réalisée le 30/09/2026. Objectif : savoir ce qui existe, ce qu'on peut réutiliser, et où Owlcy se différencie.

## Vue d'ensemble

| Projet | Type | Stack | Extension | Mascotte / design | Licence | Popularité |
|---|---|---|---|---|---|---|
| **Coucou** | Compagnon Claude Code (macOS) | Swift 6, SwiftUI, 0 dépendance | Intégrations = poller + pill + carte | ★★★ Mochi procédural, 28 sons, émotions | MIT | Jeune |
| **OpenClaw** | Assistant perso « agent OS » | Gateway Node, WebSocket :18789 | Skills `SKILL.md` + registre ClawHub | ✗ (chat via WhatsApp/Telegram/…) | Open source | Viral (≈21 000 instances publiques en une semaine, janv. 2026) |
| **QwenPaw** | Assistant perso self-hosted | Python + console React, app Tauri (bêta) | Skills, plugins, MCP, scanner de skills | ✗ | Apache 2.0 | ≈35 k ★ |
| **OpenAkita** | Multi-agents « entreprise IA » | Python + Tauri 2 / React / TS | Plugins `plugin.json`, 3 niveaux de permissions, marketplace, MCP | ✗ (dashboard) | AGPL-3.0 | ≈2 k ★ |
| **NekoAI** | Desktop pet + chat IA | Tauri v2 + Rust + React | Pas encore de plugins | ★★ sprites pixel 32 px, humeur, bulles | MIT | Petit (13 ★), actif |
| **py-gpt** | Client IA desktop tout-en-un | Python / Qt | Plugins, MCP, agents | ✗ | Open source | Mature |
| **OpenPets / Shimeji** | Desktop pets | Natif / Java | Spritesheet + JSON/XML | ★★ très grande communauté de skins | MIT / BSD | Large |
| **n8n** | Automatisation de workflows | Node | Nœuds, énorme catalogue | Éditeur de graphe | *Sustainable Use License* (fair-code, pas libre d'embarquer) | Très large |
| **Node-RED** | Flux événementiels | Node | Nœuds npm | Éditeur de graphe | Apache 2.0 | Très large |
| **Home Assistant** | Domotique | Python | Intégrations `manifest.json` + config flow, YAML | Dashboards | Apache 2.0 | Référence |

## Enseignements

### 1. Le créneau est libre
- Les **agents perso** (OpenClaw, QwenPaw, OpenAkita) sont puissants mais sans âme : chat, dashboard, messageries.
- Les **desktop pets** (NekoAI, OpenPets, Shimeji) ont l'âme mais aucune automatisation sérieuse.
- **Coucou** fait le pont, mais uniquement pour Claude Code et sur macOS.
- ➜ **Owlcy = mascotte desktop + pipelines déterministes + Owls spécialisées + skins**, sur Windows d'abord. Personne ne coche toutes ces cases.

### 2. La convergence technique est nette
- **Tauri 2 + React/TS** revient partout (OpenAkita, NekoAI, app QwenPaw) → choix validé par l'écosystème.
- **MCP** est supporté par tous les agents récents → ne pas inventer de protocole.
- **`SKILL.md`** (standard Agent Skills) est adopté par OpenClaw et plus de 40 outils → à réutiliser.

### 3. La sécurité est LE point faible du secteur
OpenClaw a subi en janvier 2026 :
- des gateways exposées sur Internet exploitées comme API de contrôle ;
- des skills malveillantes sur ClawHub (vol de clés API et de wallets, keyloggers injectés dans la mémoire) ;
- des extensions et domaines typosquattés.

Et un audit Snyk cité en 2026 estime que 36 % des skills communautaires ont des failles.
➜ Voir [`architecture/02-securite.md`](../architecture/02-securite.md). La sécurité doit être un argument de vente d'Owlcy, pas une rustine.

### 4. Ce qu'on reprend concrètement

| À qui | Quoi |
|---|---|
| Coucou | Mascotte procédurale, hooks non bloquants, invisible au repos |
| OpenClaw | Format `SKILL.md`, mémoire SQLite hybride (plein texte + vecteurs) |
| QwenPaw | **Scanner de skills** avant activation, portes d'approbation composables |
| OpenAkita | Permissions à 3 niveaux, isolation des plugins, bac à sable OS |
| NekoAI | Humeur liée à l'heure et à l'inactivité, détection de la fenêtre active, redimensionnement dynamique pour les bulles |
| Home Assistant | Config YAML + formulaires (config flow) générés depuis un schéma |
| OpenPets / Shimeji | Skins communautaires = format simple (JSON + assets) |

### 5. Ce qu'on évite
- Exposer un port réseau (erreur d'OpenClaw) → IPC local uniquement.
- Des marketplaces sans vérification.
- Embarquer n8n (licence) → au mieux, n8n comme skill externe via son API.
- Tout miser sur le mode agent (voir `feature/01-owls.md` : fiabilité des modèles locaux).

## Sources

- [Coucou](https://github.com/Louis-CFM/coucou)
- [OpenClaw — sécurité (Nebius)](https://nebius.com/blog/posts/openclaw-security) · [Acronis TRU](https://www.acronis.com/en/tru/posts/openclaw-agentic-ai-in-the-wild-architecture-adoption-and-emerging-security-risks/) · [arXiv](https://arxiv.org/html/2603.27517v3)
- [QwenPaw](https://github.com/agentscope-ai/QwenPaw)
- [OpenAkita](https://github.com/openakita/openakita)
- [NekoAI](https://github.com/nucket/NekoAI)
- [py-gpt](https://github.com/szczyglis-dev/py-gpt)
- [OpenPets — alternatives à Shimeji](https://openpets.dev/alternatives/shimeji)
- [Licence n8n expliquée](https://www.ssdnodes.com/learn/n8n-sustainable-use-license-explained) · [Node-RED](https://en.wikipedia.org/wiki/Node-RED)
- [Home Assistant — structure d'intégration](https://developers.home-assistant.io/docs/creating_integration_file_structure/)
- [Agent Skills — adoption et audits](https://atlan.com/know/ai-agent/ai-agent-skills/what-are-agent-skills/)
