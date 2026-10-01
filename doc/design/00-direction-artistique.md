# Direction artistique

## Intention

Reprendre **l'esprit** de Coucou — un petit compagnon doux, procédural, vivant, qui disparaît quand on n'en a pas besoin — avec **une chouette originale** qui devient l'identité d'Owlcy.

Mots-clés : *doux · rond · nocturne · malicieux · calme · artisanal*.

## La chouette de base

Construction procédurale (dessinée en code, pas d'images) à partir de formes simples :

```
      ▲       ▲          ← 2 aigrettes (tufts) : triangles arrondis, bougent avec l'émotion
    ╭───────────╮
   │  ◉       ◉  │       ← grands yeux ronds, disques faciaux clairs autour
   │      ▾      │       ← petit bec triangulaire
   │   ╭─────╮   │       ← plastron (zone ventrale plus claire, motif plumes optionnel)
    ╰───────────╯        ← corps : « squircle » (carré très arrondi), léger évasement bas
       ╹     ╹           ← pattes minimales (optionnelles, visibles au perchoir)
```

Règles :

- **Silhouette lisible à 32 px** : corps + aigrettes + yeux suffisent à la reconnaître.
- **Les yeux font le personnage** : ils suivent le curseur, clignent, changent de forme selon l'émotion.
- **Rotation de tête** : une chouette tourne la tête — signature forte à exploiter (regarder la fenêtre concernée, tête à 180° quand elle est « perdue »).
- **Pas de contour dur** : aplats doux, ombres internes légères.
- **Animation idle** : respiration (échelle ± 2 %), clignements aléatoires, léger balancement sur le perchoir.

## Émotions / emotes (liste initiale)

| Emote | Déclencheur | Signes visuels |
|---|---|---|
| `idle` | Rien à faire | Respire, cligne, yeux mi-clos parfois |
| `curious` | Survol, fichier approché | Tête penchée, aigrettes dressées |
| `thinking` | Step LLM en cours | Yeux qui regardent en haut, petite animation de plumes |
| `working` | Step skill en cours | Balancement rythmé |
| `ask` | Permission / étape humaine | Regarde l'utilisateur, bulle, aigrettes en alerte |
| `happy` | Run réussi | Yeux en croissant, petit sautillement |
| `dizzy` | Erreur | Tête qui tourne, yeux en spirale, recrache une pelote |
| `sleepy` | Longue inactivité / nuit | Yeux fermés, « z » |
| `annoyed` | Clics répétés dessus | Sourcils des disques faciaux froncés |

## Sons

Petits sons courts et doux (hou-hou, froissement de plumes, « pop » de bulle). Désactivables. Un pack de sons = partie du skin.

## Palette de base (proposition, à valider)

| Token | Usage | Valeur provisoire |
|---|---|---|
| `owl.body` | Corps | `#6B5B95` violet nuit |
| `owl.belly` | Plastron / disques faciaux | `#E8DFF5` |
| `owl.eye` | Iris | `#F5B841` ambre |
| `owl.beak` | Bec | `#E89B3C` |
| `ui.bg` | Fond des bulles | `#1E1B2E` (sombre) / `#FAF7FF` (clair) |
| `ui.accent` | Accent | `#7C6CF2` |

## L'UI autour

- **Perchoir** : sous Windows pas d'encoche → une branche fine en bord d'écran (au-dessus de la barre des tâches par défaut, position réglable). Les chouettes s'y posent.
- **Invisible au repos** : option « masquée », la chouette ne dépasse que le haut de la tête ; survol → elle se montre.
- **Bulles** : forme de phylactère arrondi, actions inline (Autoriser / Refuser / Voir).
- **Dashboard** : même langage (arrondis, douceur), thème sombre « nuit » par défaut.

## Benchmark design (30/09/2026)

| Projet | Approche mascotte | À retenir |
|---|---|---|
| Coucou (Mochi) | Procédural, Canvas 60 fps, 28 sons, yeux qui suivent le curseur | Le niveau de finition visé |
| NekoAI | Sprites pixel 32 px ×2/×3/×4, humeur (heure, inactivité, appli active), bulles au texte « brouillé » | Humeur contextuelle, bulle qui agrandit la fenêtre dynamiquement |
| OpenPets / Shimeji | Spritesheets + JSON/XML, 1 300+ skins communautaires | Un format de skin simple = communauté |
| Desktop Goose | Personnage qui « dérange » | Montre le risque : un compagnon trop intrusif agace → garder « invisible au repos » |

**Positionnement** : procédural + paramétrique (comme Coucou), contrairement aux sprites, pour que chaque Owl ait sa variante sans dessinateur. Le vrai différenciateur : **la mascotte reflète l'état réel des pipelines** (aucun desktop pet ne le fait).

## Contraintes techniques du perchoir (Windows)

- La fenêtre overlay est **petite et dimensionnée au contenu** (jamais une bande ou un écran entier : Focus Assist, cf. `architecture/00`) ; **seules la chouette et ses bulles captent la souris** (hit-test ~60 Hz + `set_ignore_cursor_events`).
- Ne jamais voler le focus de l'utilisateur au clic.
- Animation stoppée (`requestAnimationFrame` coupé) quand la chouette est cachée → 0 % CPU.
- Coût mesuré du rendu SVG (test T3, Chromium) : 3 chouettes à 60 fps ≈ 37 ms/s de thread principal ; **0,1 ms/s en pause**. RAM réelle de l'overlay : à mesurer (W2), les chiffres publics vont de 14 à 317 Mo selon ce qui est compté.
- Prototype jouable : `poc/cloud/t3-chouette-svg/owl.html` (3 skins, emotes).

Sources : [Coucou](https://github.com/Louis-CFM/coucou) · [NekoAI](https://github.com/nucket/NekoAI) · [OpenPets](https://openpets.dev/alternatives/shimeji) · [Manasight](https://blog.manasight.gg/why-i-chose-tauri-v2-for-a-desktop-overlay/)

## À faire

- [ ] Planche de recherche : 3 à 5 variantes de silhouette (chouette ronde, effraie, petit-duc).
- [ ] Prototype de rendu procédural (web Canvas ou SVG) avec idle + suivi des yeux.
- [ ] Tester la lisibilité à 32 / 48 / 96 px.
