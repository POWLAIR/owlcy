# Mise en place du GitHub Project

Tout est créé par script depuis [`gestion/backlog.yaml`](../../gestion/backlog.yaml). Durée : ~10 minutes.

## 1. Prérequis (une fois)

```powershell
winget install GitHub.cli          # si gh n'est pas installé
gh auth login
gh auth refresh -s project         # droit de gérer les GitHub Projects
python -m pip install pyyaml
```

## 2. Créer le dépôt

```powershell
cd $HOME\Documents\owlcy
python scripts/github_bootstrap.py install-templates   # modèles d'issues et de PR → .github/
git init -b main
git add . ; git commit -m "docs: conception initiale d'Owlcy"
gh repo create POWLAIR/owlcy --private --source . --push
```

## 3. Importer le backlog

```powershell
python scripts/github_bootstrap.py check        # valide le backlog
python scripts/github_bootstrap.py push --dry-run   # affiche tout ce qui va être créé
python scripts/github_bootstrap.py push         # crée labels, milestones, epics, issues, Project
```

Le script crée :

| Élément | Contenu |
|---|---|
| **Labels** | `type:*` (epic, us, spike, chore, bug, doc), `prio:P0-P3`, `area:*` (shell, engine, ui, design, integrations, pipelines, security, llm, devops, doc), `epic:E0-E14`, `status:blocked` |
| **Milestones** | Un par sprint (`Sprint N — objectif`), avec date d'échéance |
| **Issues** | 15 epics + 52 items, avec histoire, critères d'acceptation en cases à cocher et lien vers l'epic (en sous-issue quand l'API le permet) |
| **Project « Owlcy »** | Champs `Priority`, `Estimate`, `Epic`, `Sprint`, `Type`, remplis pour chaque item |

Relancer `push` est sans danger : l'état est gardé dans `gestion/.github-state.json` (à committer), et les issues existantes sont mises à jour au lieu d'être dupliquées.

## 4. Finaliser dans l'interface (l'API ne le permet pas)

Dans le Project → ⚙️ Settings :

1. **Status** : garder `Todo`, `In Progress`, `Done`, et ajouter `Ready`, `In Review`, `Blocked` → ordre : Todo · Ready · In Progress · In Review · Blocked · Done.
2. **Workflows** (onglet Workflows) : activer *Item added → Todo*, *Item closed → Done*, *Pull request merged → Done*.

Créer 3 vues :

| Vue | Type | Réglages |
|---|---|---|
| **Sprint en cours** | Board | Colonnes = Status ; filtre `milestone:"Sprint 0 — …"` (à changer à chaque sprint) ; champs affichés : Estimate, Priority, Epic |
| **Backlog** | Table | Group by `Sprint` ; tri par Priority ; somme de `Estimate` affichée par groupe |
| **Roadmap** | Roadmap | Dates = milestones ; group by `Epic` |

## 5. Au quotidien

- Modifier le **périmètre** (nouvelle US, estimation, sprint) → `backlog.yaml` → `docs` + `push`.
- Modifier le **statut** → directement sur le board (le script ne touche jamais au statut).
- Nouvelle idée non planifiée → issue avec le modèle « User story » et sans milestone, puis triage à la planification.
