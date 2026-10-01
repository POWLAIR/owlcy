# 🦉 Owlcy

Assistant personnel autonome pour Windows, sous la forme d'une chouette qui vit sur le bureau. Extensible par fichiers : Owls (bots spécialisés), intégrations MCP, skills (`SKILL.md`), pipelines YAML.

**Statut : conception terminée, Sprint 0 (Labo) : tests techniques avant tout développement.**

| | |
|---|---|
| 📚 Documentation | [`doc/README.md`](doc/README.md) |
| 🗣️ Vocabulaire | [`doc/lexique.md`](doc/lexique.md) |
| 🧪 Tests (labo) | [`poc/README.md`](poc/README.md) · résultats : [`doc/techno/03-resultats-tests.md`](doc/techno/03-resultats-tests.md) |
| 🗓️ Sprints | [`doc/gestion/03-sprints.md`](doc/gestion/03-sprints.md) |
| 🧭 Méthodologie | [`doc/gestion/00-methodologie.md`](doc/gestion/00-methodologie.md) |
| 🛠️ Backlog (source) | [`gestion/backlog.yaml`](gestion/backlog.yaml) → `python scripts/github_bootstrap.py docs | push` |
| ⚖️ Licence | [MIT](LICENSE) |

## Arborescence

```
owlcy/
├── doc/            conception (idée, features, architecture, design, techno, gestion, décisions)
├── poc/            laboratoire : tests exécutés (cloud/) et kit à lancer sous Windows (windows/)
├── gestion/
│   ├── backlog.yaml        source de vérité du GitHub Project
│   └── github-templates/   modèles d'issues (user story, spike, bug) et de PR
└── scripts/        github_bootstrap.py : install-templates · check · docs · push
```
