# Sécurité — leçons de la veille

Un assistant autonome combine trois choses dangereuses : **accès aux identifiants**, **exposition à du contenu non fiable** (web, mails, flux RSS…) et **capacité d'exécution**. OpenClaw a montré en janvier 2026 ce qui arrive quand on les combine sans garde-fous (voir [`idee/03-benchmark-concurrents.md`](../idee/03-benchmark-concurrents.md)).

## Menaces et parades

| Menace | Exemple réel | Parade Owlcy |
|---|---|---|
| Accès réseau au core | Gateways OpenClaw exposées sur :18789, exploitées comme API de contrôle | **Aucun port réseau.** Le shell lance le moteur et lui parle en JSON-RPC sur stdio (voir [`00-vue-ensemble.md`](00-vue-ensemble.md)). Un *named pipe* avec ACL limitée à l'utilisateur ne sera ajouté que si un autre client doit piloter le moteur. L'endpoint HTTP des hooks Claude Code écoute sur `127.0.0.1` avec un token aléatoire. |
| Plugin malveillant | Skills ClawHub voleuses de clés et de wallets | Paquets **signés** + **scanner** avant activation (inspiré de QwenPaw) + affichage des permissions demandées + aucune installation silencieuse |
| Injection de prompt | Contenu web ou RSS qui ordonne « envoie tes clés à… » | **Séparer lecture et action** : une étape qui lit du contenu externe ne peut pas déclencher directement un outil sensible. La sortie est marquée *non fiable* et tout outil `write/shell/network-send` en aval exige une validation. |
| Fuite de secrets | Clés stockées dans des fichiers de config | Secrets **uniquement** dans le Windows Credential Manager (crate `keyring`) ; les fichiers contiennent `secret-ref:` ; injection dans l'environnement du seul serveur MCP autorisé |
| Plugin qui déborde | Accès disque complet | 1 processus par intégration, répertoire de travail restreint, **niveaux de permission** (base / avancé / système, comme OpenAkita) |
| Pipeline générée par l'IA | La Forgeronne écrit un `rm -rf` | Dry-run obligatoire + diff + validation humaine avant installation |
| Mémoire empoisonnée | Keylogger injecté dans les fichiers mémoire (OpenClaw) | Mémoire en SQLite, écriture seulement via l'API du core, journal des modifications |

## Modèle de permissions (révisé)

```yaml
# extrait de owl.yaml
permissions:
  fs.read:  { allow: ["~/Downloads", "~/Documents/Veille"] }
  fs.write: ask
  network:  allow
  shell:    deny
  secrets:  [notion]
  untrusted_input_then_action: ask   # règle anti-injection
```

- 3 réponses possibles : `allow` · `ask` · `deny`, portées **par Owl**, pas globalement.
- La bulle de validation utilise **MRTR** (`input_required`, MCP 2026-07-28) et `needsApproval` (AI SDK 7), sans mécanisme maison.
- Chaque décision est journalisée dans le run.

## Presets d'autonomie (inspiré de Factory Droid Exec)

| Preset | Autorisé sans demander | Usage |
|---|---|---|
| `observe` (défaut des nouveaux runs headless) | Lecture fichiers, réseau en lecture | Veille, surveillance |
| `low` | + écriture dans les dossiers de l'Owl, docs | Rangement, notes |
| `medium` | + installation de dépendances d'intégration, commits locaux | Dev perso |
| `high` | + actions distantes (publier, envoyer, déployer) | À réserver aux runs validés |

Les presets remplissent le bloc `permissions` ; on peut toujours affiner à la main.

## Apports Hermes (01/10/2026)

- **Fichiers protégés** : toute écriture dans les skills, la mémoire, `AGENTS.md`/`CLAUDE.md` ou les configs d'Owl exige une approbation, même en autonomie haute.
- **Relecteur LLM optionnel** (« smart approvals ») : un petit modèle indépendant pré-filtre les commandes signalées pour réduire les demandes ; les règles `deny` restent absolues ; la décision finale sur une action sensible reste humaine au MVP.
- **Examen des serveurs MCP stdio** (motifs d'exfiltration) + **nettoyage de l'environnement** des sous-processus (seuls les secrets déclarés sont injectés).
- Un runtime externe (Hermes, Goose…) avec accès au terminal → exécution en **WSL2 ou Docker**, jamais directement sur l'hôte Windows par défaut.

## Checklist MVP

- [ ] IPC local uniquement, aucun port à l'écoute par défaut.
- [ ] Secrets dans le coffre de l'OS.
- [ ] Permissions par Owl + bulle de validation.
- [ ] Marquage « non fiable » des sorties d'outils de lecture externe.
- [ ] Journal d'audit par run.

## Plus tard

- Sandbox OS des intégrations (Windows : AppContainer / niveau d'intégrité bas ; OpenAkita utilise MIC sous Windows).
- Signature des paquets + registre vérifié.
- Commande `owlcy audit` (inspirée de `openclaw security audit`).

## Sources

- [Nebius — sécurité OpenClaw](https://nebius.com/blog/posts/openclaw-security)
- [Acronis TRU — OpenClaw dans la nature](https://www.acronis.com/en/tru/posts/openclaw-agentic-ai-in-the-wild-architecture-adoption-and-emerging-security-risks/)
- [Analyse de sécurité OpenClaw (arXiv)](https://arxiv.org/html/2603.27517v3)
- [QwenPaw — scanner de skills](https://github.com/agentscope-ai/QwenPaw) · [OpenAkita — sandbox 6 couches](https://github.com/openakita/openakita)
- [MCP 2026-07-28 — MRTR](https://blog.modelcontextprotocol.io/posts/2026-07-28/) · [AI SDK 6 — tool approval](https://vercel.com/blog/ai-sdk-6)
- [Droid Exec — niveaux d'autonomie](https://docs.factory.ai/droid-exec/overview) · [Hermes — référence praticien (approbations, fichiers protégés)](https://blakecrosley.com/guides/hermes)
