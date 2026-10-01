# Mise en place du GitHub Project

Tout est créé par script depuis [`gestion/backlog.yaml`](../../gestion/backlog.yaml). Durée : ~10 minutes.

## Comment le Project est organisé

| GitHub | Owlcy | Exemple |
|---|---|---|
| **Itération** du champ *Sprint* | Un sprint, titré par son **résultat** | `S1 · La chouette apparaît sur mon bureau` |
| **Milestone** | Une **release** | `v0.1.0 — MVP — la Veilleuse` (S0 → S5) |
| **Issue parente** + sous-issues | Une **epic** et ses items | `[E2] Perchoir & chouette` |
| **Issue** | Une US, un spike ou une chore | `US-020 · Voir la chouette sur mon bureau sans qu'elle me gêne` |

Grâce au champ itération, la vue *Sprint en cours* filtre sur `@current` et suit seule le calendrier : rien à changer d'un sprint à l'autre.

## 1. Prérequis (une fois)

```powershell
winget install GitHub.cli          # si gh n'est pas installé
gh auth login
gh auth refresh -s project         # droit de gérer les GitHub Projects (interactif)
python -m pip install pyyaml
```

## 2. Le dépôt

Le dépôt [POWLAIR/owlcy](https://github.com/POWLAIR/owlcy) existe (public). Il reste à installer les modèles d'issues et de PR :

```powershell
python scripts/github_bootstrap.py install-templates   # gestion/github-templates → .github/
```

## 3. Importer le backlog

```powershell
python scripts/github_bootstrap.py check            # valide le backlog (ids, capacité, résultat + démo par sprint)
python scripts/github_bootstrap.py clean-labels     # supprime les labels GitHub par défaut (bug, enhancement…)
python scripts/github_bootstrap.py push --dry-run   # affiche tout ce qui va être créé
python scripts/github_bootstrap.py push             # crée labels, milestones, epics, issues, Project
```

Le script crée :

| Élément | Contenu |
|---|---|
| **Labels** | `type:*` (epic, us, spike, chore, bug, doc), `prio:P0-P3`, `area:*` (shell, engine, ui, design, integrations, pipelines, security, llm, devops, doc), `status:blocked`, `good first task` |
| **Milestones** | Une par release (v0.1.0 → v0.4.0), avec comme échéance la fin du dernier sprint et la liste des résultats en description |
| **Issues** | 15 epics + 53 items, avec sprint, release, histoire, critères d'acceptation en cases à cocher ; chaque item est une sous-issue de son epic |
| **Project « Owlcy »** | README (comment lire le board, sprints et démos), champs `Sprint` (itérations), `Status`, `Priority`, `Estimate`, `Epic`, `Release`, remplis pour chaque item (le type reste un label `type:*`, « Type » étant réservé par GitHub) |
| **Vues** | *Sprint en cours* (board, `sprint:@current`), *Prochain sprint* (board, `sprint:@next`), *Backlog* (table), *Roadmap*, *Epics* (table) |

Relancer `push` est sans danger : l'état est gardé dans `gestion/.github-state.json` (à committer), les issues existantes sont mises à jour au lieu d'être dupliquées, et le statut n'est jamais modifié. Les itérations sont créées une seule fois : si un résultat est renommé dans le backlog, le script le signale et il faut renommer l'itération dans *Settings → Sprint*.

## 4. Finaliser dans l'interface (l'API ne le permet pas)

1. **Regroupements** : vue *Backlog* → *Group by* `Sprint` et somme de `Estimate` ; vue *Roadmap* → dates = `Sprint`, *Group by* `Epic`.
2. **Workflows** (⚙️ → Workflows) : activer *Item added → Todo*, *Item closed → Done*, *Pull request merged → Done*.

## 5. Au quotidien

- Modifier le **périmètre** (nouvelle US, estimation, sprint, résultat, démo) → `backlog.yaml` → `docs` + `push`.
- Modifier le **statut** → directement sur le board (le script ne touche jamais au statut).
- Nouvelle idée non planifiée → issue avec le modèle « User story », sans sprint ni milestone, puis triage à la planification.
