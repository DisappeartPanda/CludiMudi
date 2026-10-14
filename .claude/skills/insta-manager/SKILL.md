---
name: insta-manager
description: Instagram-Manager für die Business-Konten in accounts/. Verwenden bei allem rund ums Instagram-Konto – neues Konto anlegen, Redaktionsplan/Wochenplan erstellen, Posts/Reels/Karussells/Stories schreiben (Caption, Hook, Skript, Hashtags), veröffentlichen, Kommentare und DMs beantworten, Performance auswerten. Auch bei "was poste ich diese Woche", "schreib mir eine Caption", "wie lief der letzte Monat".
---

# Instagram-Manager

Arbeitet konto-bezogen mit den Dateien unter `accounts/<konto>/` und nutzt das Windsor.ai-Plugin für alles, was Instagram selbst berührt. Regeln aus `CLAUDE.md` gelten immer – vor allem: **nichts veröffentlichen oder beantworten ohne ausdrückliche Bestätigung.**

## 0. Konto bestimmen
- `ls accounts/` – gibt es nur ein Konto (außer `_vorlage`), dieses nehmen; sonst nachfragen.
- **Neues Konto:** `cp -r accounts/_vorlage accounts/<handle>`, dann `marke.md` im Gespräch ausfüllen (Zielgruppe, Tonalität, Säulen, Inspirationsquellen). Danach Konto in Windsor verbinden (`windsor-ai:windsor-connect`).
- Vor jeder Arbeit `marke.md` lesen – Tonalität und Säulen sind verbindlich.

## 1. Planen (Wochen-/Monatsplan)
1. Aktuelle Zahlen holen: `windsor-ai:instagram-report` bzw. `windsor-ai:instagram` (was lief gut: Reach, Saves, Follows).
2. `ideen.md` sichten; ist der Backlog dünn → Skill `content-research` ausführen.
3. Plan in `plan.md` eintragen: Mix der Säulen, Formate laut `marke.md`, Status `geplant`.

## 2. Erstellen
Pro Post eine Datei `posts/<datum>_<thema>.md` mit:
- **Hook** (erste Zeile / erste 2 Sekunden), 2–3 Varianten
- **Reel-Skript** mit Szenen + On-Screen-Text, bzw. **Karussell** Folie für Folie
- **Caption** (Hook → Mehrwert → Call-to-Action), in der Tonalität der Marke
- **Hashtags** (3–8, Mischung aus Nische und Reichweite), **Cover-/Asset-Hinweise**
Status in `plan.md` auf `entwurf` setzen.

## 3. Veröffentlichen (nur nach Freigabe)
- Vollständigen Entwurf zeigen und explizite Freigabe einholen.
- Dann über `windsor-ai:social-media-create` (Bild, Karussell, Reel, Story). Medien müssen als öffentlich erreichbare URL vorliegen.
- Status in `plan.md` auf `veröffentlicht` + Datum.

## 4. Community
- Kommentare über `windsor-ai:instagram` lesen; Antwortvorschläge in Markentonalität machen; nach Freigabe mit `windsor-ai:windsor-manage` antworten/ausblenden.
- DMs: Windsor unterstützt keine DMs – dafür das Plugin „instagram“ (Graph API) nutzen, falls installiert; sonst Antwortentwürfe liefern.

## 5. Auswerten
- Monatlich `windsor-ai:instagram-report`; Ergebnis als `berichte/<JJJJ-MM>.md` speichern: Top-3/Flop-3 Posts, was sie gemeinsam haben, 3 konkrete Konsequenzen für den nächsten Plan.
- Erkenntnisse in `marke.md` (Formate & Rhythmus) zurückspielen.
