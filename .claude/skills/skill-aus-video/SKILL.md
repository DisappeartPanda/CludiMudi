---
name: skill-aus-video
description: Macht aus einem Tutorial-/Erklärvideo (YouTube oder Instagram) einen neuen Claude-Skill, damit Claude das Gezeigte künftig selbst anwenden kann. Verwenden bei "lern das aus diesem Video", "mach daraus einen Skill", "bring dir bei, was in diesem Video erklärt wird".
---

# Skill aus Video

1. **Transkript holen**: `python3 tools/research.py youtube <url>` bzw. `instagram-post <url>` (+ `transkribieren`). Bei mehreren Videos zum selben Thema alle holen.
2. **Prüfen, ob es das schon gibt**: bestehende Skills in `.claude/skills/` ansehen; ggf. Skill `find-skills` nutzen – ein etablierter Skill schlägt einen selbstgebauten.
3. **Wissen extrahieren**: Nur das Übertragbare – Schritte, Regeln, Formeln, Checklisten, Beispiele, typische Fehler. Füllwörter, Werbung und Selbstvermarktung weglassen. Unsicheres/Widersprüchliches markieren statt erfinden.
4. **Skill schreiben** unter `.claude/skills/<kurzer-name>/SKILL.md`:
   - Frontmatter `name` + `description` (wann der Skill greifen soll, mit typischen Formulierungen des Nutzers)
   - Kurze Anleitung im Imperativ, ggf. Beispiele; Quelle(n) am Ende verlinken
   - Für größere Projekte den Skill `anthropic-skills:skill-creator` zu Hilfe nehmen
5. **Dem Nutzer zeigen**, was der Skill kann, und auf Wunsch committen + pushen.
