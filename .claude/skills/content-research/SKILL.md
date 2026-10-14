---
name: content-research
description: Recherchiert Content-Ideen aus Instagram- und YouTube-Videos (scrapen von Metadaten, Transkripten, optional Videos) und macht daraus Ideen für die eigenen Konten. Verwenden bei "finde neue Content-Ideen", "was machen erfolgreiche Accounts in meiner Nische", "analysier dieses Reel/Video/diesen Kanal", oder wenn ideen.md leer ist.
---

# Content-Research

Werkzeug: `python3 tools/research.py` (falls Module fehlen: `pip install -r requirements.txt`). Ergebnisse landen in `research/`.

## Ablauf
1. **Konto + Ziel klären**: Für welches Konto (`accounts/<konto>/marke.md` lesen), welche Säule/welches Thema?
2. **Quellen wählen**: Inspirationsquellen aus `marke.md`, vom Nutzer genannte URLs, oder per Websuche passende Kanäle/Profile finden.
3. **Top-Performer finden**
   - YouTube-Kanal: `python3 tools/research.py youtube-kanal <kanal-url> --limit 50`
   - Instagram-Profil: `python3 tools/research.py instagram <profil> --limit 20` (klein halten!)
4. **Die besten 3–5 tief analysieren**
   - YouTube: `python3 tools/research.py youtube <url>` → `transkript.txt`
   - Instagram-Reel: `python3 tools/research.py instagram-post <url>`; für Transkript `--media` bzw. Video laden und `transkribieren`
5. **Analyse je Video** (in `research/<ordner>/analyse.md`): Hook (wörtlich), Aufbau/Dramaturgie, Länge, Format, Thema, warum es funktioniert, Kommentar-Signale.
6. **Ideen ableiten** – auf die eigene Marke übertragen, *nicht kopieren*. Jede Idee als Zeile in `accounts/<konto>/ideen.md` mit Quelle.
7. Kurze Zusammenfassung an den Nutzer: Muster, die sich wiederholen, + die 5 stärksten Ideen.

## Grenzen
- Fremde Videos nur zur Analyse; nie reposten oder 1:1 nachbauen (Urheberrecht).
- Instagram blockt aggressives Scraping: kleine Limits, Pausen, separates Research-Login (`IG_RESEARCH_USER`), nie das Business-Konto.
- Schlägt ein Abruf mit Netzwerkfehler/403 fehl: Domains `youtube.com`, `googlevideo.com`, `instagram.com`, `cdninstagram.com` müssen in den Netzwerk-Einstellungen der Umgebung erlaubt sein – dem Nutzer sagen, nicht umgehen.
