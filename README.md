# Fit Essentials – Übersicht

Alles, was zu deinem Pinterest-Business gehört, auf einen Blick.

## 1. Was wo ist

| Was | Wo | Wofür |
|---|---|---|
| Pinterest-Profil | pinterest.com/Lildesports | Deine Pins und Boards |
| Website | https://leonhaupt08-ui.github.io/fit-pins/ | Produktkatalog + Blog, verlinkt im Profil |
| Produkte | https://leonhaupt08-ui.github.io/fit-pins/products/ | Alle Produkte mit Amazon-Links |
| Blog | https://leonhaupt08-ui.github.io/fit-pins/blog/ | Ratgeber-Artikel mit Produkten |
| Impressum | https://leonhaupt08-ui.github.io/fit-pins/legal-notice/ | Pflicht in Deutschland |
| Datenschutz | https://leonhaupt08-ui.github.io/fit-pins/privacy/ | Pflicht in Deutschland + Pinterest-App |
| Dieses GitHub-Projekt | github.com/leonhaupt08-ui/fit-pins | Speichert Website, Pin-Bilder und Warteschlange |
| Amazon-Partner-ID | `lilmedia-21` | Steckt in jedem Amazon-Link |

## 2. Die Boards (alle auf Englisch)

| Board | Was rein gehört |
|---|---|
| Women's Gym Outfits \| Workout Fits | Sets und komplette Outfits für Frauen |
| Gym Leggings Outfits for Women | Leggings |
| Women's Gym Tops & Sports Bras | Tops, Crop Tops, Sport-BHs |
| Women's Gym Shorts \| Workout Shorts | Shorts für Frauen |
| Men's Gym Outfits & Athleisure | Alles an Kleidung für Männer |
| Men's Gym & Running Shoes | Schuhe für Männer |
| Women's Gym & Running Shoes | Schuhe für Frauen |
| Gym Equipment, Recovery & Home Gym | Taschen, Shaker, Hanteln, Bänder, Zubehör **und** Recovery (Faszienrolle, Massageball, Magnesium) |
| Muscle Recovery & Sleep Essentials | leer – in der App löschen (Board → … → Bearbeiten → Löschen) |

Regel: **Kleidung nach Frau/Mann, Zubehör nach Zweck.**

## 3. Automatische Pins

- Jeden Tag um **9:00, 15:00 und 19:00 Uhr** postet Claude neue Pins (2 + 2 + 1 = 5 pro Tag).
- Die Pins warten in `queue.json`, die Bilder liegen im Ordner `pins/`.
- Regeln für die Pins stehen in `PLAYBOOK.md` (Englisch, Werbe-Kennzeichnung, keine Gesundheitsversprechen).
- **Neue Produkte:** Amazon-Partnerlink + Screenshot im Claude-Chat schicken. Ohne neue Produkte wird nichts gepostet.
- **Stoppen:** im Claude-Chat „stopp die Pins“ schreiben.

## 4. Zugänge

| Dienst | Wofür | Achtung |
|---|---|---|
| Zapier | Verbindung Claude ↔ Pinterest | Testphase läuft ca. bis 1. Dezember, danach kostenpflichtig |
| Pinterest-App „Fit Essentials Pin Manager“ | Kostenloser Ersatz für Zapier | Wartet auf Freigabe durch Pinterest, danach Standard-Zugang beantragen |
| GitHub | Website und Pin-Bilder | Projekt ist öffentlich (keine Passwörter hier speichern) |

## 5. Was du selbst in der Pinterest-App machen musst

Pinterest erlaubt das nicht über Apps, nur von Hand:

- [ ] **Bio** ändern (Profil → Profil bearbeiten → Über dich):
      `Gym outfits, activewear & fitness essentials for women and men 🖤 New finds daily. Affiliate links. IG: @fit.finds.de`
- [ ] **Name** ändern: `Fit Essentials | Gym Outfits & Fitness Finds`
- [ ] **Board-Reihenfolge** (Profil → Gespeichert → Sortieren → Eigene Reihenfolge), Reihenfolge wie in der Tabelle oben
- [ ] **Leeres Board löschen**: „Muscle Recovery & Sleep Essentials“ → … → Board bearbeiten → Löschen
- [ ] Optional: **Sauna Vest** aus „Women's Gym Outfits“ nach „Gym Equipment, Recovery & Home Gym“ verschieben
- [ ] Optional: **Website bestätigen** (Einstellungen → Konten beanspruchen → Website → HTML-Tag) und den Tag an Claude schicken

## 6. Wenn etwas nicht geht

- Pins kommen nicht mehr → Zapier-Testphase vorbei oder Verbindung abgelaufen → Claude fragen
- Website-Änderung → Claude fragen (Quelltext liegt in `site-build/`)
- Neue Produkte auf der Website → Claude fragen (Kategorien und Titel stehen in `data/catalog.json`)
