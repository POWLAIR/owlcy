# Questions ouvertes

Priorité : 🔴 bloquant pour démarrer · 🟠 avant le MVP · 🟢 plus tard
Recommandations issues de la veille — **à valider par Paul**, puis à transformer en ADR (US-008, Sprint 0). Mise à jour v5 (01/10/2026) : T4 Windows, T5-T7 lancés, ADR-001 à 004 rédigés au statut « proposé » (📝). Paul les passe à « accepté » après relecture.

| # | Question | Prio | Recommandation | Source |
|---|---|---|---|---|
| Q1 | Core en Rust pur, ou Rust + sidecar TS ? | 🔴 | 📝 [ADR-001](ADR-001-moteur-ts-sidecar.md) proposé : **Rust mince + moteur TS (Bun) en sidecar**, AI SDK **7**. Windows : 30 Mo xz, 24 ms, 75 Mo privés. Reste W2 (RAM totale) | techno/03 T4-T7 |
| Q2 | MCP comme protocole unique ? | 🔴 | 📝 [ADR-002](ADR-002-mcp-integrations-outils-internes.md) proposé : **MCP pour les tiers, outils de base dans le moteur** ; MRTR validé (T7) | techno/03 T1, T2, T5, T7 |
| Q3 | Svelte ou React ? | 🔴 | **React** (écosystème, AI SDK, React Flow) | techno/01 §7 |
| Q4 | Rendu mascotte : SVG ou Rive ? | 🟠 | **SVG pour le MVP**, Rive en spike comparatif ; `skin.yaml` indépendant du moteur de rendu | design/01 |
| Q5 | Routage de l'Owl principale | 🟠 | Règles explicites + classifieur local (1 appel) | feature/01 |
| Q6 | Syntaxe d'expressions | 🟠 | ✅ **JSONata** (T6 : ~25 µs, pas de `$flatten`, `undefined` = échec de l'étape) — dans ADR-004 | techno/03 T6 |
| Q7 | Windows ou WSL ? | 🔴 | 📝 [ADR-003](ADR-003-windows-natif-wsl.md) proposé : **Windows natif** + `target: wsl` via `wsl.exe`. **En attente de W1 et W3** | techno/01 §8 |
| Q8 | Vocabulaire chouette dans le code ? | 🟢 | Non, UI seulement | feature/00 |
| Q9 | Open source ? Licence ? | 🟢 | MIT (comme Coucou, NekoAI) ; éviter l'AGPL si on veut des contributions larges | idee/03 |
| Q10 | Nom définitif « Owlcy » ? | 🟢 | Vérifier la disponibilité (GitHub, domaine) | — |
| Q11 | Mémoire long terme | 🟠 | SQLite plein texte au MVP, vecteurs (sqlite-vec) plus tard — même approche qu'OpenClaw | idee/03 |
| Q12 | Plafonds de coût LLM par Owl | 🟠 | Oui : budget tokens/jour par Owl, alerte dans la bulle | — |
| Q13 | **Nouveau** — Moteur de pipelines maison ou Mastra ? | 🔴 | 📝 [ADR-004](ADR-004-moteur-pipelines-maison.md) proposé : **maison + AI SDK 7 + JSONata** ; réexamen fin Sprint 4 si > ~1 000 lignes | techno/03 T5-T7 |
| Q14 | Packaging du sidecar : Bun compile, Node SEA ou pkg ? | 🟠 | ✅ **Bun compile**, build Windows validé : 84,7 Mo brut / 29,9 Mo xz, 24 ms (T4 Windows) — dans ADR-001 | techno/03 T4 |
| Q15 | **Nouveau** — Reprise des runs après redémarrage dès le MVP ? | 🟠 | Persister l'état par étape, reprise manuelle | feature/02 |
| Q16 | **Nouveau** — Sandbox OS des intégrations (AppContainer) : quand ? | 🟢 | Après le MVP ; processus séparés + permissions d'abord | architecture/02 |
| Q17 | **v3** — Hermes : cerveau central ou moteur optionnel par Owl ? | 🟠 | **Moteur optionnel** (adaptateur de runtime) ; Owlcy doit fonctionner sans Hermes | architecture/03 |
| Q18 | **v3** — Apprentissage auto (skills créées par l'IA) : dès quand ? | 🟢 | Phase 4, toujours en brouillon + revue humaine | feature/04 |
| Q19 | **v3** — Presets d'autonomie (`observe/low/medium/high`) ? | 🟠 | Oui, `observe` par défaut pour les runs planifiés | architecture/02 |
| Q20 | **v3** — Format Markdown « à la Droid » pour les Owls simples ? | 🟢 | Oui, en plus du YAML | feature/01 |
| Q21 | **v3** — Intégrer Factory ? | 🟢 | Non (fermé, payant, orienté code) ; s'en inspirer | idee/04 |
| Q22 | **v4** — RAM réelle de Tauri sous Windows (14 ou 317 Mo ?) | 🔴 | Mesurer processus + enfants WebView2 (W2). NO-GO si > 150 Mo privés au repos | techno/01 §1 |
| Q23 | **v4** — Cartes MCP Apps et CSP de Tauri : une iframe `srcdoc` passe-t-elle ? | 🟠 | Tester W1.11-12 ; sinon origine dédiée (proxy sandbox) | techno/03 T2 |
| Q24 | **v4** — Capacité réelle (points par sprint) | 🟠 | 12 points par défaut, recalculée après le Sprint 1 | gestion/00 |
| Q25 | **v4** — Sprint 5 sur les fêtes de fin d'année : décaler ? | 🟢 | À décider au planning du Sprint 4 | gestion/03 |
| Q26 | **v5** — Modèle par défaut des étapes `llm:` et du mode agent | 🔴 | W4 : `qwen3:4b` local juste (simple/choix 100 %) mais ~1,5 min par appel sur 4 Go de VRAM ; chaîné en timeout → **agent en cloud par défaut**, local pour les étapes planifiées. Choix du fournisseur cloud à faire (ADR) | techno/03 W4 |
