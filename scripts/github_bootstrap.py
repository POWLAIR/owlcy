#!/usr/bin/env python3
"""Owlcy — backlog.yaml → documentation + GitHub (labels, milestones, issues, Project).

Prérequis : Python 3.10+, `pip install pyyaml`, GitHub CLI (`gh`) connecté :
    gh auth login
    gh auth refresh -s project          # droit de créer/modifier un GitHub Project

Commandes (depuis la racine du dépôt) :
    python scripts/github_bootstrap.py install-templates     # copie gestion/github-templates → .github/
    python scripts/github_bootstrap.py check                 # valide backlog.yaml (ids, epics, capacité, résultats)
    python scripts/github_bootstrap.py docs                  # régénère doc/gestion/02-backlog.md et 03-sprints.md
    python scripts/github_bootstrap.py clean-labels          # supprime les labels GitHub par défaut (bug, enhancement…)
    python scripts/github_bootstrap.py push --dry-run        # affiche ce qui serait créé sur GitHub
    python scripts/github_bootstrap.py push                  # crée / met à jour labels, milestones, issues, Project

Organisation GitHub :
    Sprint  = itération du Project (champ « Sprint »), titrée par son résultat : « S1 · La chouette apparaît sur mon bureau »
    Release = milestone GitHub (v0.1.0 → v0.4.0), qui regroupe les sprints jusqu'à la release
    Epic    = issue parente ; ses items en sont les sous-issues

Idempotent : l'état (id Owlcy → n° d'issue, Project) est gardé dans gestion/.github-state.json ;
relancer `push` met à jour les issues existantes au lieu d'en créer de nouvelles. Le statut n'est jamais modifié.
"""
from __future__ import annotations

import argparse, datetime as dt, json, pathlib, subprocess, sys
from collections import defaultdict

try:
    import yaml
except ImportError:
    sys.exit("PyYAML manquant : python -m pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "gestion" / "backlog.yaml"
STATE = ROOT / "gestion" / ".github-state.json"
DOC = ROOT / "doc" / "gestion"

TYPE_LABELS = {
    "epic": ("type:epic", "5319E7", "Grand bloc fonctionnel"),
    "us": ("type:us", "1D76DB", "User story"),
    "spike": ("type:spike", "FBCA04", "Exploration technique avec décision go / no-go"),
    "chore": ("type:chore", "C5DEF5", "Technique, outillage, dette"),
    "bug": ("type:bug", "D73A4A", "Anomalie"),
    "doc": ("type:doc", "0E8A16", "Documentation"),
}
PRIO_LABELS = {
    "P0": ("prio:P0", "B60205", "Bloquant pour le sprint"),
    "P1": ("prio:P1", "D93F0B", "Important"),
    "P2": ("prio:P2", "FBCA04", "Normal"),
    "P3": ("prio:P3", "C2E0C6", "Bonus"),
}
AREA_COLOR = "BFD4F2"
EXTRA_LABELS = [("status:blocked", "000000", "Bloqué — voir commentaire"), ("good first task", "7057FF", "Petite tâche pour démarrer")]
GITHUB_DEFAULT_LABELS = ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted",
                         "invalid", "question", "wontfix", "accessibility"]

# (nom, couleur, description) — l'ordre est celui des colonnes du board
STATUS_OPTIONS = [
    ("Todo", "GRAY", "Pas encore prêt (voir Definition of Ready)"),
    ("Ready", "BLUE", "Prêt à démarrer"),
    ("In Progress", "YELLOW", "En cours"),
    ("In Review", "PURPLE", "PR ouverte"),
    ("Blocked", "RED", "Bloqué — voir commentaire"),
    ("Done", "GREEN", "Definition of Done remplie"),
]
# (nom, layout, filtre, champs affichés)
VIEWS = [
    ("Sprint en cours", "BOARD_LAYOUT", 'sprint:@current -label:"type:epic"', ["Title", "Assignees", "Estimate", "Priority", "Epic"]),
    ("Prochain sprint", "BOARD_LAYOUT", 'sprint:@next -label:"type:epic"', ["Title", "Assignees", "Estimate", "Priority", "Epic"]),
    ("Backlog", "TABLE_LAYOUT", '-label:"type:epic"', ["Title", "Status", "Sprint", "Estimate", "Priority", "Labels", "Epic", "Release"]),
    ("Roadmap", "ROADMAP_LAYOUT", '-label:"type:epic"', []),  # une roadmap n'accepte pas de colonnes
    ("Epics", "TABLE_LAYOUT", 'label:"type:epic"', ["Title", "Status", "Epic", "Sub-issues progress"]),
]


# ───────────────────────── modèle ─────────────────────────
def load():
    data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    p = data["project"]
    start = p["first_sprint_start"]
    start = start if isinstance(start, dt.date) else dt.date.fromisoformat(str(start))
    rels = sorted(data["releases"], key=lambda r: r["sprint"])
    for r in rels:
        r["title"] = f"{r['version']} — {r['name']}"
    cur = start
    for s in data["sprints"]:
        s["days"] = s.get("days", p["sprint_length_days"])
        s["capacity"] = round(p["capacity_points"] * s["days"] / p["sprint_length_days"])
        s["start"] = cur
        s["end"] = cur + dt.timedelta(days=s["days"] - 3)  # finit un vendredi
        cur = cur + dt.timedelta(days=s["days"])
        s["title"] = f"S{s['n']} · {s.get('result', '?')}"
        s["release"] = next((r for r in rels if r["sprint"] >= s["n"]), None)
    return data


def check(data) -> list[str]:
    errs, warns = [], []
    ids = [s["id"] for s in data["stories"]]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errs.append(f"ids en double : {sorted(dup)}")
    epics = {e["id"] for e in data["epics"]}
    sprints = {s["n"] for s in data["sprints"]}
    areas = set(data["areas"])
    for sp in data["sprints"]:
        for k in ("result", "demo"):
            if not sp.get(k):
                errs.append(f"Sprint {sp['n']} : champ « {k} » manquant")
        if not sp["release"]:
            errs.append(f"Sprint {sp['n']} : après la dernière release")
    for s in data["stories"]:
        for k in ("id", "type", "title", "epic", "sprint", "points", "prio", "area", "story", "ac"):
            if k not in s:
                errs.append(f"{s.get('id')} : champ « {k} » manquant")
        if s.get("epic") not in epics:
            errs.append(f"{s['id']} : epic inconnue {s.get('epic')}")
        if s.get("sprint") not in sprints:
            errs.append(f"{s['id']} : sprint inconnu {s.get('sprint')}")
        if s.get("points") not in (1, 2, 3, 5, 8):
            errs.append(f"{s['id']} : points hors échelle (1,2,3,5,8)")
        if s.get("type") not in TYPE_LABELS:
            errs.append(f"{s['id']} : type inconnu {s.get('type')}")
        for a in s.get("area", []):
            if a not in areas:
                errs.append(f"{s['id']} : area inconnue {a}")
    caps = {s["n"]: s["capacity"] for s in data["sprints"]}
    for n, pts in points_by_sprint(data).items():
        if pts > caps[n]:
            warns.append(f"Sprint {n} : {pts} pts > capacité {caps[n]}")
    for w in warns:
        print("⚠️ ", w)
    return errs


def points_by_sprint(data):
    d = defaultdict(int)
    for s in data["stories"]:
        d[s["sprint"]] += s["points"]
    return dict(sorted(d.items()))


# ───────────────────────── documentation ─────────────────────────
def gen_docs(data):
    DOC.mkdir(parents=True, exist_ok=True)
    sprints = {s["n"]: s for s in data["sprints"]}
    by_epic = defaultdict(list)
    for s in data["stories"]:
        by_epic[s["epic"]].append(s)
    pts = points_by_sprint(data)
    stamp = "<!-- Fichier GÉNÉRÉ par scripts/github_bootstrap.py depuis gestion/backlog.yaml — ne pas modifier à la main -->\n\n"

    # 02-backlog.md
    out = [stamp, "# Backlog\n\n",
           f"{len(data['stories'])} items · {sum(pts.values())} points · {len(data['epics'])} epics. ",
           "Source : [`gestion/backlog.yaml`](../../gestion/backlog.yaml). Vocabulaire : [`lexique.md`](../lexique.md).\n\n",
           "| Epic | Titre | Items | Points | Sprints |\n|---|---|---|---|---|\n"]
    for e in data["epics"]:
        items = by_epic.get(e["id"], [])
        sp = sorted({i["sprint"] for i in items})
        out.append(f"| {e['id']} | {e['title']} | {len(items)} | {sum(i['points'] for i in items)} | {', '.join('S' + str(x) for x in sp)} |\n")
    for e in data["epics"]:
        out.append(f"\n## {e['id']} — {e['title']}\n\n{e['desc']}\n")
        for s in by_epic.get(e["id"], []):
            out.append(f"\n### {s['id']} · {s['title']}\n\n")
            out.append(f"`{s['type']}` · **{s['points']} pts** · {s['prio']} · {sprints[s['sprint']]['title']} · {', '.join(s['area'])}\n\n")
            out.append(f"> {s['story']}\n\n**Critères d'acceptation**\n\n")
            out.extend(f"- [ ] {a}\n" for a in s["ac"])
    (DOC / "02-backlog.md").write_text("".join(out), encoding="utf-8")

    # 03-sprints.md
    cap = data["project"]["capacity_points"]
    out = [stamp, "# Plan de sprints\n\n",
           "Un sprint = **un résultat** : ce que je peux voir et utiliser à la fin, de bout en bout. ",
           "Le résultat est le titre de l'itération dans le GitHub Project ; la démo est jouée à la revue.\n\n",
           f"Sprints de {data['project']['sprint_length_days']} jours (Sprint 0 : 3 semaines) · capacité supposée **{cap} points** / 2 semaines, à ajuster après le Sprint 1 selon la vélocité réelle.\n\n",
           "| Sprint | Dates | Résultat | Points / capacité | Release |\n|---|---|---|---|---|\n"]
    for n, s in sprints.items():
        p = pts.get(n, 0)
        flag = " ⚠️" if p > s["capacity"] else ""
        r = s["release"]
        rel = f"**{r['version']}**" if r["sprint"] == n else ""
        out.append(f"| S{n} | {s['start']:%d/%m} → {s['end']:%d/%m/%Y} | {s['result']} | {p} / {s['capacity']}{flag} | {rel} |\n")
    current = None
    for n, s in sprints.items():
        if s["release"] is not current:
            current = s["release"]
            out.append(f"\n## Vers {current['title']}\n")
        out.append(f"\n### S{n} · {s['result']}\n\n{s['start']:%d/%m/%Y} → {s['end']:%d/%m/%Y} · {pts.get(n, 0)} pts\n\n")
        out.append("**Démo de fin de sprint**\n\n")
        out.extend(f"- [ ] {d}\n" for d in s["demo"])
        out.append("\n| Item | Type | Pts | Prio | Epic |\n|---|---|---|---|---|\n")
        for st in [x for x in data["stories"] if x["sprint"] == n]:
            out.append(f"| {st['id']} · {st['title']} | {st['type']} | {st['points']} | {st['prio']} | {st['epic']} |\n")
        if s.get("retro"):
            out.append(f"\n**Rétro** : {s['retro']}\n")
        if current["sprint"] == n:
            out.append(f"\n🚀 **Release {current['title']}**\n")
    (DOC / "03-sprints.md").write_text("".join(out), encoding="utf-8")
    print(f"✓ {DOC / '02-backlog.md'}\n✓ {DOC / '03-sprints.md'}")


def project_readme(data):
    rows = "\n".join(f"| {s['title']} | {s['start']:%d/%m} → {s['end']:%d/%m/%Y} | {' ; '.join(s['demo'])} |" for s in data["sprints"])
    rels = "\n".join(f"- **{r['title']}** — fin du S{r['sprint']}" for r in data["releases"])
    base = f"https://github.com/{data['project']['repo']}/blob/main"
    return f"""Assistant personnel autonome pour Windows : une chouette sur le bureau.

## Comment lire ce Project

- **Un sprint = un résultat.** Chaque itération du champ *Sprint* est titrée par ce qu'on peut voir et utiliser à la fin (« S1 · La chouette apparaît sur mon bureau »).
- **Une milestone = une release** (v0.1.0 → v0.4.0). Sa barre de progression montre l'avancement vers la release.
- **Une epic = une issue parente.** Ses items en sont les sous-issues.
- Vues : *Sprint en cours* (le board du jour), *Prochain sprint* (pour la planification), *Backlog*, *Roadmap*, *Epics*.

## Sprints

| Sprint | Dates | Démo de fin de sprint |
|---|---|---|
{rows}

## Releases

{rels}

## Règles

Le backlog vit dans [`gestion/backlog.yaml`]({base}/gestion/backlog.yaml) et ce Project en est généré (`scripts/github_bootstrap.py push`). Seul le **statut** se modifie ici.
Méthode : [`00-methodologie.md`]({base}/doc/gestion/00-methodologie.md) · vocabulaire : [`lexique.md`]({base}/doc/lexique.md) · plan détaillé : [`03-sprints.md`]({base}/doc/gestion/03-sprints.md).
"""


# ───────────────────────── GitHub ─────────────────────────
class GH:
    def __init__(self, repo: str, dry: bool):
        self.repo, self.dry = repo, dry
        self.owner = repo.split("/")[0]

    def run(self, *args, fake: str = "", stdin: str | None = None) -> str:
        cmd = ["gh", *args]
        if self.dry:
            print("DRY  ", " ".join(a if " " not in a else repr(a) for a in cmd)[:220])
            return fake
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", input=stdin)
        if r.returncode != 0:
            raise RuntimeError(f"{' '.join(cmd[:4])}… → {r.stderr.strip()}")
        return r.stdout.strip()

    def api(self, path, *fields, method="GET", fake="[]"):
        args = ["api", "-X", method, path]
        for f in fields:
            args += ["-f", f]
        return self.run(*args, fake=fake)

    def graphql(self, query: str, fake: dict | None = None, **variables) -> dict:
        if self.dry:
            print("DRY   gh api graphql", query.split("(")[0].split("{")[0].strip()[:60], list(variables))
            return fake or {}
        out = self.run("api", "graphql", "--input", "-", stdin=json.dumps({"query": query, "variables": variables}))
        res = json.loads(out)
        if res.get("errors"):
            raise RuntimeError(f"graphql → {res['errors']}")
        return res["data"]


def issue_body(s, data, epic_num):
    e = next(x for x in data["epics"] if x["id"] == s["epic"])
    sp = next(x for x in data["sprints"] if x["n"] == s["sprint"])
    ep = f"#{epic_num}" if epic_num else s["epic"]
    lines = [f"**Sprint** : {sp['title']}  ",
             f"**Release** : {sp['release']['title']}  ",
             f"**Epic** : {ep} — {e['id']} {e['title']}  ",
             f"**Estimation** : {s['points']} pts · **Priorité** : {s['prio']} · **Domaine** : {', '.join(s['area'])}", "",
             "### Histoire", "", s["story"], "", "### Critères d'acceptation", ""]
    lines += [f"- [ ] {a}" for a in s["ac"]]
    lines += ["", "### Definition of Done", "",
              "Voir [`doc/gestion/00-methodologie.md`](../blob/main/doc/gestion/00-methodologie.md#definition-of-done). Vocabulaire : [`doc/lexique.md`](../blob/main/doc/lexique.md).",
              "", f"<!-- owlcy-id: {s['id']} -->"]
    return "\n".join(lines)


def epic_body(e, children, state, sprints):
    lines = [e["desc"], "", "### Items", ""]
    for s in children:
        num = state["issues"].get(s["id"])
        ref = f"#{num}" if num else s["id"]
        lines.append(f"- [ ] {ref} {s['id']} — {s['title']} ({sprints[s['sprint']]['title']}, {s['points']} pts)")
    lines += ["", f"<!-- owlcy-id: {e['id']} -->"]
    return "\n".join(lines)


def upsert_issue(gh, state, oid, title, body, labels, milestone):
    num = state["issues"].get(oid)
    if num:
        args = ["issue", "edit", str(num), "-R", gh.repo, "--title", title, "--body", body, "--add-label", ",".join(labels)]
        if milestone:
            args += ["--milestone", milestone]
        gh.run(*args)
        return num, False
    args = ["issue", "create", "-R", gh.repo, "--title", title, "--body", body, "--label", ",".join(labels)]
    if milestone:
        args += ["--milestone", milestone]
    url = gh.run(*args, fake=f"https://github.com/{gh.repo}/issues/{900 + len(state['issues'])}")
    num = int(url.rstrip("/").split("/")[-1])
    state["issues"][oid] = num
    return num, True


def clean_labels(repo):
    gh = GH(repo, False)
    have = {l["name"] for l in json.loads(gh.run("label", "list", "-R", repo, "--json", "name", "--limit", "200"))}
    for name in GITHUB_DEFAULT_LABELS:
        if name in have:
            gh.run("label", "delete", name, "-R", repo, "--yes")
            print("✗", name)
    print("✓ labels par défaut supprimés")


def push(data, repo, dry, with_project):
    gh = GH(repo, dry)
    state = json.loads(STATE.read_text()) if STATE.exists() else {"issues": {}, "project": None}
    sprints = {s["n"]: s for s in data["sprints"]}

    print("── Labels")
    labels = list(TYPE_LABELS.values()) + list(PRIO_LABELS.values()) + EXTRA_LABELS
    labels += [(f"area:{a}", AREA_COLOR, f"Domaine {a}") for a in data["areas"]]
    for name, color, desc in labels:
        gh.run("label", "create", name, "-R", repo, "--color", color, "--description", desc, "--force")

    print("── Milestones (releases)")
    existing = {m["title"] for m in json.loads(gh.api(f"repos/{repo}/milestones?state=all&per_page=100") or "[]")}
    for r in data["releases"]:
        if r["title"] in existing:
            continue
        last = sprints[r["sprint"]]
        desc = "Sprints : " + " · ".join(s["title"] for s in data["sprints"] if s["release"] is r)
        gh.api(f"repos/{repo}/milestones", f"title={r['title']}", f"description={desc}",
               f"due_on={last['end']}T23:59:59Z", method="POST", fake="{}")

    print("── Epics")
    epic_nums = {}
    for e in data["epics"]:
        num, _ = upsert_issue(gh, state, e["id"], f"[{e['id']}] {e['title']}", e["desc"], ["type:epic"], None)
        epic_nums[e["id"]] = num

    print("── User stories / spikes / chores")
    for s in data["stories"]:
        lbl = [TYPE_LABELS[s["type"]][0], PRIO_LABELS[s["prio"]][0]] + [f"area:{a}" for a in s["area"]]
        sp = sprints[s["sprint"]]
        num, created = upsert_issue(gh, state, s["id"], f"{s['id']} · {s['title']}", issue_body(s, data, epic_nums[s["epic"]]), lbl, sp["release"]["title"])
        if created and not dry:  # sous-issue de l'epic (API GitHub sub-issues ; ignorée si indisponible)
            try:
                iid = gh.run("api", f"repos/{repo}/issues/{num}", "--jq", ".id")
                gh.run("api", "-X", "POST", f"repos/{repo}/issues/{epic_nums[s['epic']]}/sub_issues", "-F", f"sub_issue_id={iid}")
            except RuntimeError as err:
                print("   (sous-issue ignorée :", err, ")")
        if not dry:
            STATE.write_text(json.dumps(state, indent=2))

    print("── Checklists des epics")
    by_epic = defaultdict(list)
    for s in data["stories"]:
        by_epic[s["epic"]].append(s)
    for e in data["epics"]:
        gh.run("issue", "edit", str(epic_nums[e["id"]]), "-R", repo, "--body", epic_body(e, by_epic[e["id"]], state, sprints))

    if with_project:
        project(gh, data, state)
    if not dry:
        STATE.write_text(json.dumps(state, indent=2))
    print("✓ Terminé" + (" (dry-run : rien n'a été modifié)" if dry else ""))


Q_FIELDS = """query($id: ID!) { node(id: $id) { ... on ProjectV2 {
  fields(first: 50) { nodes {
    ... on ProjectV2FieldCommon { id name dataType }
    ... on ProjectV2SingleSelectField { options { id name } }
    ... on ProjectV2IterationField { configuration { iterations { id title } completedIterations { id title } } }
  } }
  views(first: 30) { nodes { id name } } } } }"""


def project(gh, data, state):
    print("── GitHub Project")
    owner = gh.owner
    if not state.get("project"):
        out = gh.run("project", "create", "--owner", owner, "--title", data["project"]["name"], "--format", "json",
                     fake='{"number": 1, "id": "PVT_fake"}')
        state["project"] = json.loads(out)["number"]
        gh.run("project", "link", str(state["project"]), "--owner", owner, "--repo", gh.repo)
        if not gh.dry:
            STATE.write_text(json.dumps(state, indent=2))
    num = str(state["project"])
    pid = json.loads(gh.run("project", "view", num, "--owner", owner, "--format", "json", fake='{"id": "PVT_fake"}'))["id"]

    readme = project_readme(data)
    gh.run("project", "edit", num, "--owner", owner, "--readme", readme,
           "--description", "Un sprint = un résultat. Backlog généré depuis gestion/backlog.yaml.")

    def fetch():
        node = gh.graphql(Q_FIELDS, fake={"node": {"fields": {"nodes": []}, "views": {"nodes": []}}}, id=pid)["node"]
        return {f["name"]: f for f in node["fields"]["nodes"] if f}, {v["name"]: v for v in node["views"]["nodes"]}

    fields, views = fetch()

    # Champs à options : créés s'ils manquent (le type d'item reste un label type:* ; « Type » est un nom réservé par GitHub), options resynchronisées en gardant les ids existants
    selects = {
        "Status": STATUS_OPTIONS,
        "Priority": [("P0", "RED", "Bloquant pour le sprint"), ("P1", "ORANGE", "Important"), ("P2", "YELLOW", "Normal"), ("P3", "GRAY", "Bonus")],
        "Epic": [(f"{e['id']} {e['title']}", "GRAY", e["desc"]) for e in data["epics"]],
        "Release": [(r["version"], "GREEN", r["name"]) for r in data["releases"]],
    }
    for name, opts in selects.items():
        f = fields.get(name)
        if not f:
            gh.graphql("""mutation($p: ID!, $n: String!, $o: [ProjectV2SingleSelectFieldOptionInput!]) {
                createProjectV2Field(input: {projectId: $p, dataType: SINGLE_SELECT, name: $n, singleSelectOptions: $o}) { clientMutationId } }""",
                       p=pid, n=name, o=[{"name": n, "color": c, "description": d} for n, c, d in opts])
            continue
        have = {o["name"]: o["id"] for o in f.get("options", [])}
        if list(have) != [n for n, _, _ in opts]:
            gh.graphql("""mutation($f: ID!, $o: [ProjectV2SingleSelectFieldOptionInput!]) {
                updateProjectV2Field(input: {fieldId: $f, singleSelectOptions: $o}) { clientMutationId } }""",
                       f=f["id"], o=[{**({"id": have[n]} if n in have else {}), "name": n, "color": c, "description": d} for n, c, d in opts])
    if "Estimate" not in fields:
        gh.run("project", "field-create", num, "--owner", owner, "--name", "Estimate", "--data-type", "NUMBER")

    # Sprint = itérations, titrées par le résultat. Créées une fois : l'API ne garde pas les ids si on les réécrit.
    wanted = [{"title": s["title"], "startDate": str(s["start"]), "duration": s["days"]} for s in data["sprints"]]
    if "Sprint" not in fields:
        gh.graphql("""mutation($p: ID!, $c: ProjectV2IterationFieldConfigurationInput!) {
            createProjectV2Field(input: {projectId: $p, dataType: ITERATION, name: "Sprint", iterationConfiguration: $c}) { clientMutationId } }""",
                   p=pid, c={"startDate": wanted[0]["startDate"], "duration": data["project"]["sprint_length_days"], "iterations": wanted})

    fields, views = fetch()
    conf = (fields.get("Sprint") or {}).get("configuration") or {}
    iterations = {i["title"]: i["id"] for i in conf.get("iterations", []) + conf.get("completedIterations", [])}
    missing = [w["title"] for w in wanted if w["title"] not in iterations]
    if missing and not gh.dry:
        print("   ⚠️  itérations absentes du Project (résultat renommé ?) — à corriger à la main dans Settings → Sprint :", *missing, sep="\n      ")

    def opt(field, name):
        return next((o["id"] for o in (fields.get(field) or {}).get("options", []) if o["name"] == name), None)

    # Vues : la vue par défaut « View 1 » est réutilisée pour la première
    print("── Vues")
    for name, layout, flt, cols in VIEWS:
        vid = (views.get(name) or {}).get("id")
        if not vid and "View 1" in views:
            vid = views.pop("View 1")["id"]
        if not vid:
            res = gh.graphql("""mutation($p: ID!, $n: String!, $l: ProjectV2ViewLayout!) {
                createProjectV2View(input: {projectId: $p, name: $n, layout: $l}) { projectV2View { id } } }""",
                             fake={"createProjectV2View": {"projectV2View": {"id": "PVTV_fake"}}}, p=pid, n=name, l=layout)
            vid = res["createProjectV2View"]["projectV2View"]["id"]
        visible = [fields[c]["id"] for c in cols if c in fields]
        gh.graphql("""mutation($v: ID!, $n: String!, $l: ProjectV2ViewLayout!, $f: String!, $c: ProjectV2ViewConfigurationInput) {
            updateProjectV2View(input: {viewId: $v, name: $n, layout: $l, filter: $f, configuration: $c}) { clientMutationId } }""",
                   v=vid, n=name, l=layout, f=flt, c={"visibleFieldIds": visible} if visible else None)

    # Items : une seule mutation GraphQL par item pour tous ses champs (jamais le Status)
    print("── Items du Project")
    epics = {e["id"]: e for e in data["epics"]}
    sprints = {s["n"]: s for s in data["sprints"]}
    items = [{"id": e["id"], "type": "epic", "epic": e["id"]} for e in data["epics"]] + \
            [{"id": s["id"], "type": s["type"], "epic": s["epic"], "prio": s["prio"], "points": s["points"], "sprint": sprints[s["sprint"]]} for s in data["stories"]]
    for it in items:
        url = f"https://github.com/{gh.repo}/issues/{state['issues'][it['id']]}"
        item = json.loads(gh.run("project", "item-add", num, "--owner", owner, "--url", url, "--format", "json", fake='{"id": "PVTI_fake"}'))["id"]
        values = {"Epic": {"singleSelectOptionId": opt("Epic", f"{it['epic']} {epics[it['epic']]['title']}")}}
        if it["type"] != "epic":
            values["Priority"] = {"singleSelectOptionId": opt("Priority", it["prio"])}
            values["Estimate"] = {"number": it["points"]}
            values["Release"] = {"singleSelectOptionId": opt("Release", it["sprint"]["release"]["version"])}
            values["Sprint"] = {"iterationId": iterations.get(it["sprint"]["title"])}
        ops = []
        for i, (fname, val) in enumerate(values.items()):
            if fname in fields and all(val.values()):
                v = "{" + ", ".join(f"{k}: {json.dumps(x)}" for k, x in val.items()) + "}"
                ops.append(f'f{i}: updateProjectV2ItemFieldValue(input: {{projectId: "{pid}", itemId: "{item}", fieldId: "{fields[fname]["id"]}", value: {v}}}) {{ clientMutationId }}')
        if ops:
            gh.graphql("mutation {\n" + "\n".join(ops) + "\n}")
    print("   À faire à la main (l'API ne le permet pas) : voir doc/gestion/01-github-project.md §4")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("install-templates")
    sub.add_parser("check")
    sub.add_parser("docs")
    c = sub.add_parser("clean-labels")
    c.add_argument("--repo", default=None)
    p = sub.add_parser("push")
    p.add_argument("--repo", default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-project", action="store_true")
    a = ap.parse_args()
    if a.cmd == "install-templates":
        import shutil
        src, dst = ROOT / "gestion" / "github-templates", ROOT / ".github"
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"✓ modèles copiés dans {dst}")
        return
    data = load()
    errs = check(data)
    if errs:
        print("\n".join("✗ " + e for e in errs))
        sys.exit(1)
    repo = getattr(a, "repo", None) or data["project"]["repo"]
    if a.cmd == "check":
        print(f"✓ backlog valide : {len(data['stories'])} items, {sum(points_by_sprint(data).values())} pts")
    elif a.cmd == "docs":
        gen_docs(data)
    elif a.cmd == "clean-labels":
        clean_labels(repo)
    elif a.cmd == "push":
        push(data, repo, a.dry_run, not a.no_project)


if __name__ == "__main__":
    main()
