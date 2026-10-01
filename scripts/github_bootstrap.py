#!/usr/bin/env python3
"""Owlcy — backlog.yaml → documentation + GitHub (labels, milestones, issues, Project).

Prérequis : Python 3.10+, `pip install pyyaml`, GitHub CLI (`gh`) connecté :
    gh auth login
    gh auth refresh -s project          # droit de créer/modifier un GitHub Project

Commandes (depuis la racine du dépôt) :
    python scripts/github_bootstrap.py install-templates     # copie gestion/github-templates → .github/
    python scripts/github_bootstrap.py check                 # valide backlog.yaml (ids, epics, capacité)
    python scripts/github_bootstrap.py docs                  # régénère doc/gestion/02-backlog.md et 03-sprints.md
    python scripts/github_bootstrap.py push --dry-run        # affiche ce qui serait créé sur GitHub
    python scripts/github_bootstrap.py push                  # crée / met à jour labels, milestones, issues, Project

Idempotent : l'état (id Owlcy → n° d'issue) est gardé dans gestion/.github-state.json ;
relancer `push` met à jour les issues existantes au lieu d'en créer de nouvelles.
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


# ───────────────────────── modèle ─────────────────────────
def load():
    data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    p = data["project"]
    start = p["first_sprint_start"]
    start = start if isinstance(start, dt.date) else dt.date.fromisoformat(str(start))
    cur = start
    for s in data["sprints"]:
        s["days"] = s.get("days", p["sprint_length_days"])
        s["capacity"] = round(p["capacity_points"] * s["days"] / p["sprint_length_days"])
        s["start"] = cur
        s["end"] = cur + dt.timedelta(days=s["days"] - 3)  # finit un vendredi
        cur = cur + dt.timedelta(days=s["days"])
        s["title"] = f"Sprint {s['n']} — {s['goal']}"
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
    epics = {e["id"]: e for e in data["epics"]}
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
            out.append(f"`{s['type']}` · **{s['points']} pts** · {s['prio']} · Sprint {s['sprint']} · {', '.join(s['area'])}\n\n")
            out.append(f"> {s['story']}\n\n**Critères d'acceptation**\n\n")
            out.extend(f"- [ ] {a}\n" for a in s["ac"])
    (DOC / "02-backlog.md").write_text("".join(out), encoding="utf-8")

    # 03-sprints.md
    cap = data["project"]["capacity_points"]
    rel = {r["sprint"]: r for r in data["releases"]}
    out = [stamp, "# Plan de sprints\n\n",
           f"Sprints de {data['project']['sprint_length_days']} jours (Sprint 0 : 3 semaines) · capacité supposée **{cap} points** / 2 semaines, à ajuster après le Sprint 1 selon la vélocité réelle.\n\n",
           "| Sprint | Dates | Objectif | Points / capacité | Release |\n|---|---|---|---|---|\n"]
    for n, s in sprints.items():
        p = pts.get(n, 0)
        flag = " ⚠️" if p > s["capacity"] else ""
        r = rel.get(n)
        out.append(f"| S{n} | {s['start']:%d/%m} → {s['end']:%d/%m/%Y} | {s['goal']} | {p} / {s['capacity']}{flag} | {r['version'] + ' — ' + r['name'] if r else ''} |\n")
    for n, s in sprints.items():
        out.append(f"\n## Sprint {n} — {s['goal']}\n\n{s['start']:%d/%m/%Y} → {s['end']:%d/%m/%Y} · {pts.get(n, 0)} pts\n\n")
        out.append("| Item | Type | Pts | Prio | Epic |\n|---|---|---|---|---|\n")
        for st in [x for x in data["stories"] if x["sprint"] == n]:
            out.append(f"| {st['id']} · {st['title']} | {st['type']} | {st['points']} | {st['prio']} | {st['epic']} |\n")
        if n in rel:
            out.append(f"\n🚀 **Release {rel[n]['version']} — {rel[n]['name']}**\n")
    (DOC / "03-sprints.md").write_text("".join(out), encoding="utf-8")
    print(f"✓ {DOC / '02-backlog.md'}\n✓ {DOC / '03-sprints.md'}")


# ───────────────────────── GitHub ─────────────────────────
class GH:
    def __init__(self, repo: str, dry: bool):
        self.repo, self.dry = repo, dry
        self.owner = repo.split("/")[0]

    def run(self, *args, fake: str = "") -> str:
        cmd = ["gh", *args]
        if self.dry:
            print("DRY  ", " ".join(a if " " not in a else repr(a) for a in cmd)[:220])
            return fake
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise RuntimeError(f"{' '.join(cmd[:4])}… → {r.stderr.strip()}")
        return r.stdout.strip()

    def api(self, path, *fields, method="GET", fake="[]"):
        args = ["api", "-X", method, path]
        for f in fields:
            args += ["-f", f]
        return self.run(*args, fake=fake)


def issue_body(s, data, epic_num):
    e = next(x for x in data["epics"] if x["id"] == s["epic"])
    sp = next(x for x in data["sprints"] if x["n"] == s["sprint"])
    ep = f"#{epic_num}" if epic_num else s["epic"]
    lines = [f"**Epic** : {ep} — {e['id']} {e['title']}  ",
             f"**Sprint** : {sp['title']}  ",
             f"**Estimation** : {s['points']} pts · **Priorité** : {s['prio']} · **Domaine** : {', '.join(s['area'])}", "",
             "### Histoire", "", s["story"], "", "### Critères d'acceptation", ""]
    lines += [f"- [ ] {a}" for a in s["ac"]]
    lines += ["", "### Definition of Done", "",
              "Voir [`doc/gestion/00-methodologie.md`](../blob/main/doc/gestion/00-methodologie.md#definition-of-done). Vocabulaire : [`doc/lexique.md`](../blob/main/doc/lexique.md).",
              "", f"<!-- owlcy-id: {s['id']} -->"]
    return "\n".join(lines)


def epic_body(e, children, state):
    lines = [e["desc"], "", "### Items", ""]
    for s in children:
        num = state["issues"].get(s["id"])
        ref = f"#{num}" if num else s["id"]
        lines.append(f"- [ ] {ref} {s['id']} — {s['title']} (S{s['sprint']}, {s['points']} pts)")
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


def push(data, repo, dry, with_project):
    gh = GH(repo, dry)
    state = json.loads(STATE.read_text()) if STATE.exists() else {"issues": {}, "project": None}

    print("── Labels")
    labels = list(TYPE_LABELS.values()) + list(PRIO_LABELS.values()) + EXTRA_LABELS
    labels += [(f"area:{a}", AREA_COLOR, f"Domaine {a}") for a in data["areas"]]
    labels += [(f"epic:{e['id']}", "EDEDED", e["title"]) for e in data["epics"]]
    for name, color, desc in labels:
        gh.run("label", "create", name, "-R", repo, "--color", color, "--description", desc, "--force")

    print("── Milestones (sprints)")
    existing = {m["title"] for m in json.loads(gh.api(f"repos/{repo}/milestones?state=all&per_page=100") or "[]")}
    for s in data["sprints"]:
        if s["title"] not in existing:
            gh.api(f"repos/{repo}/milestones", f"title={s['title']}", f"description=Du {s['start']:%d/%m/%Y} au {s['end']:%d/%m/%Y}",
                   f"due_on={s['end']}T23:59:59Z", method="POST", fake="{}")

    print("── Epics")
    epic_nums = {}
    for e in data["epics"]:
        num, _ = upsert_issue(gh, state, e["id"], f"[{e['id']}] {e['title']}", e["desc"], ["type:epic", f"epic:{e['id']}"], None)
        epic_nums[e["id"]] = num

    print("── User stories / spikes / chores")
    sprint_title = {s["n"]: s["title"] for s in data["sprints"]}
    for s in data["stories"]:
        lbl = [TYPE_LABELS[s["type"]][0], PRIO_LABELS[s["prio"]][0], f"epic:{s['epic']}"] + [f"area:{a}" for a in s["area"]]
        num, created = upsert_issue(gh, state, s["id"], f"{s['id']} · {s['title']}", issue_body(s, data, epic_nums[s["epic"]]), lbl, sprint_title[s["sprint"]])
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
        gh.run("issue", "edit", str(epic_nums[e["id"]]), "-R", repo, "--body", epic_body(e, by_epic[e["id"]], state))

    if with_project:
        project(gh, data, state)
    if not dry:
        STATE.write_text(json.dumps(state, indent=2))
    print("✓ Terminé" + (" (dry-run : rien n'a été modifié)" if dry else ""))


def project(gh, data, state):
    print("── GitHub Project")
    owner = gh.owner
    if not state.get("project"):
        out = gh.run("project", "create", "--owner", owner, "--title", data["project"]["name"], "--format", "json",
                     fake='{"number": 1, "id": "PVT_fake"}')
        state["project"] = json.loads(out)["number"]
        gh.run("project", "link", str(state["project"]), "--owner", owner, "--repo", gh.repo)
    num = str(state["project"])
    pid = json.loads(gh.run("project", "view", num, "--owner", owner, "--format", "json", fake='{"id": "PVT_fake"}'))["id"]
    fields_wanted = {
        "Priority": ("SINGLE_SELECT", ["P0", "P1", "P2", "P3"]),
        "Estimate": ("NUMBER", None),
        "Epic": ("SINGLE_SELECT", [f"{e['id']} {e['title']}" for e in data["epics"]]),
        "Sprint": ("SINGLE_SELECT", [f"S{s['n']}" for s in data["sprints"]]),
        "Type": ("SINGLE_SELECT", ["us", "spike", "chore", "bug", "doc", "epic"]),
    }
    fl = json.loads(gh.run("project", "field-list", num, "--owner", owner, "--format", "json", "--limit", "50", fake='{"fields": []}'))["fields"]
    have = {f["name"] for f in fl}
    for name, (typ, opts) in fields_wanted.items():
        if name not in have:
            args = ["project", "field-create", num, "--owner", owner, "--name", name, "--data-type", typ]
            if opts:
                args += ["--single-select-options", ",".join(opts)]
            gh.run(*args)
    fl = json.loads(gh.run("project", "field-list", num, "--owner", owner, "--format", "json", "--limit", "50", fake='{"fields": []}'))["fields"]
    fields = {f["name"]: f for f in fl}

    def opt(field, name):
        f = fields.get(field)
        return next((o["id"] for o in (f or {}).get("options", []) if o["name"] == name), None) if f else None

    epics = {e["id"]: e for e in data["epics"]}
    items = [(e["id"], "epic", None, None, e["id"]) for e in data["epics"]] + \
            [(s["id"], s["type"], s["prio"], s["points"], s["epic"], s["sprint"]) for s in data["stories"]]
    for it in items:
        oid, typ = it[0], it[1]
        url = f"https://github.com/{gh.repo}/issues/{state['issues'][oid]}"
        out = gh.run("project", "item-add", num, "--owner", owner, "--url", url, "--format", "json", fake='{"id": "PVTI_fake"}')
        item = json.loads(out)["id"]

        def set_select(field, value):
            o = opt(field, value)
            if o and field in fields:
                gh.run("project", "item-edit", "--id", item, "--project-id", pid, "--field-id", fields[field]["id"], "--single-select-option-id", o)

        set_select("Type", typ)
        set_select("Epic", f"{it[4]} {epics[it[4]]['title']}")
        if typ != "epic":
            set_select("Priority", it[2])
            set_select("Sprint", f"S{it[5]}")
            if "Estimate" in fields:
                gh.run("project", "item-edit", "--id", item, "--project-id", pid, "--field-id", fields["Estimate"]["id"], "--number", str(it[3]))
    print("   Vues à créer à la main (2 min, l'API ne le permet pas) : voir doc/gestion/01-github-project.md")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("install-templates")
    sub.add_parser("check")
    sub.add_parser("docs")
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
    if a.cmd == "check":
        print(f"✓ backlog valide : {len(data['stories'])} items, {sum(points_by_sprint(data).values())} pts")
    elif a.cmd == "docs":
        gen_docs(data)
    elif a.cmd == "push":
        push(data, a.repo or data["project"]["repo"], a.dry_run, not a.no_project)


if __name__ == "__main__":
    main()
