# ADR-001 — Moteur en TypeScript, compilé avec Bun, en sidecar de Tauri

- **Date** : 2026-10-01
- **Statut** : proposé (reste à confirmer avec W1/W2 : mémoire totale du perchoir + moteur)
- **Questions liées** : Q1, Q14

## Contexte

Owlcy a besoin d'un moteur qui exécute les pipelines, héberge les intégrations MCP et parle aux LLM. Le shell Tauri est en Rust. Deux options : tout écrire en Rust, ou garder un Rust mince (fenêtres, Win32, secrets) et un moteur TypeScript dans un processus à part (sidecar), qui communique par JSON-RPC sur stdio.

## Options envisagées

1. **Rust pur** (moteur dans le binaire Tauri, MCP via `rmcp`) : aucun processus ni poids en plus. En contrepartie, le SDK MCP Rust est encore en bêta, il n'existe pas d'équivalent de l'AI SDK, et la boucle de développement est plus lente.
2. **Rust mince + sidecar TS compilé avec Bun** : on profite de l'écosystème LLM/MCP le plus complet (AI SDK, SDK MCP officiel v2) et on itère vite. Le prix : un processus et ~30 Mo d'installeur en plus.
3. Sidecar Python : SDK MCP bloqué sur la spec 2025-11-25 (T1), runtime lourd à embarquer. Écarté.

## Décision

**Option 2.** Les mesures montrent que le surcoût est acceptable et que la chaîne TS couvre tout ce qu'il faut dès aujourd'hui :

| Preuve | Résultat | Source |
|---|---|---|
| Binaire Bun **Windows** (compilé depuis WSL, `--target=bun-windows-x64`) | 84,7 Mo brut, **29,9 Mo en xz** | T4 Windows |
| Démarrage → 1re réponse sous Windows | **~24 ms** (96 ms au 1er lancement, analyse Defender) | T4 Windows |
| RAM du sidecar sous Windows | **75 Mo privés**, 26 Mo de working set | T4 Windows |
| RTT JSON-RPC stdio | 0,03 ms p50 | T4 Windows |
| AI SDK 7 + outils MCP stdio + `needsApproval` | la chaîne fonctionne : `move_file` bloqué jusqu'à l'approbation, puis exécuté | T5 (modèle simulé, Ollama réel à venir) |
| SDK MCP TS v2 (2.2.0), révision 2026-07-28 | `input_required` (MRTR) aller-retour OK ; le même handler sert aussi les clients 2025 | T7 |

Packaging (Q14) : **`bun build --compile`**, validé sous Windows.

Version du SDK LLM : **AI SDK 7**, et non la 6 prévue au départ. La v7 est `latest` depuis 2026, et les providers Ollama (`ai-sdk-ollama` 4.x, `ollama-ai-provider-v2` 4.x) exigent `ai@^7`. La v6 ne survit que sur une branche de maintenance (`ai-v6`).

## Conséquences

- Installeur estimé à ~35 Mo (Tauri + moteur) : 10 fois plus léger qu'Electron, mais loin des « 3 Mo » de Tauri seul.
- La RAM du moteur (~75 Mo) **s'ajoute** à celle du perchoir. Le critère global « < 150 Mo privés au repos » de W2 doit donc être vérifié avec le moteur lancé, pas seulement avec la fenêtre Tauri.
- Contrat Rust ↔ moteur : JSON-RPC 2.0 ligne par ligne sur stdio, sans socket ni port.
- Pièges de l'AI SDK 7 à connaître : pas de message `system` dans `messages` (il faut l'option `instructions`) ; après une approbation, le résultat de l'outil exécuté n'apparaît pas dans `steps` du tour suivant.
- **Repli** : si W2 montre que perchoir + moteur dépassent le budget RAM, porter le moteur en Rust avec `rmcp`, à réévaluer quand `rmcp` sortira de bêta.
