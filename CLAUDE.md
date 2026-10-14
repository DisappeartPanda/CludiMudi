# CludiMudi – Instagram-Manager

Dieses Repo ist die Zentrale für das Management eines oder mehrerer Instagram-**Business**-Konten.
Sprache mit dem Nutzer: Deutsch.

## Aufbau
- `accounts/<konto>/` – ein Ordner pro Instagram-Konto (Vorlage: `accounts/_vorlage/`)
  - `marke.md` – Zielgruppe, Tonalität, Content-Säulen, Do's & Don'ts
  - `ideen.md` – Ideen-Backlog (aus Research gespeist)
  - `plan.md` – Redaktionsplan (was wann gepostet wird, Status)
  - `posts/` – fertige Entwürfe (Caption, Hashtags, Skript, Asset-Hinweise)
  - `berichte/` – Performance-Auswertungen
- `research/` – Ergebnisse von `tools/research.py` (Metadaten + Transkripte; Videos unter `media/` werden nicht committet)
- `.claude/skills/` – Skills: `insta-manager`, `content-research`, `skill-aus-video`, `find-skills`

## Werkzeuge
- **Veröffentlichen, Kommentare, Insights:** Windsor.ai-Plugin (`windsor-ai:instagram`, `windsor-ai:social-media-create`, `windsor-ai:windsor-manage`, `windsor-ai:instagram-report`). Konto zuerst mit `windsor-ai:windsor-connect` verbinden.
- **Research:** `python3 tools/research.py --help` (yt-dlp für YouTube, instaloader für Instagram).

## Regeln
1. **Nie ohne ausdrückliche Bestätigung veröffentlichen**, Kommentare beantworten/löschen oder DMs senden. Immer erst den vollständigen Entwurf zeigen.
2. **Fremde Inhalte nur als Inspiration**: Videos anderer werden analysiert (Hook, Aufbau, Thema, Format), nie 1:1 wiederverwendet oder reposted. Eigene Umsetzung, eigene Worte.
3. **Instagram-Research schonend**: nur öffentliche Profile, kleine `--limit`-Werte, nie mit dem Business-Konto einloggen (separates Research-Konto via `IG_RESEARCH_USER`), sonst droht eine Sperre.
4. Bei mehreren Konten immer klären bzw. angeben, für welches Konto gearbeitet wird.
5. Ergebnisse (Ideen, Pläne, Berichte) in die Dateien unter `accounts/` schreiben, nicht nur in den Chat.
