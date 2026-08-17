# CSE-Krankmeldung-App

Handy-Hülle für das bestehende Krankmeldungsformular auf <https://cse-service.net/krankmeldung/>.

**Live:** <https://cse-krankmeldung.pages.dev/> (Cloudflare Pages, Projekt `cse-krankmeldung`)

**Zweck:** Mitarbeiter sollen ein Symbol „Krankmeldung" auf dem Handy haben und mit
einem Fingertipp krankmelden können — **ohne Anmeldung, ohne Passwort, ohne M365/Teams.**

## Was das ist (und was nicht)

- Eine sogenannte PWA: eine gewöhnliche Webseite, die sich auf dem Handy als App ablegen lässt.
- **Kein** App-Store, **keine** Installation im klassischen Sinn, **kein** Konto.
- Das Formular selbst bleibt unverändert auf der Firmen-Website (WordPress/Elementor).
  Diese App zeigt es nur im eigenen Fenster an und liefert Symbol, Name und Vollbildstart.
- An der Website wird **nichts** geändert — wir haben dort keinen Zugriff.

## Warum nicht GitHub Pages

War der erste Weg (Ablage `CSEService/krankmeldung` existiert weiter als Quelle).
Am 17.08.2026 ließ sich dort wegen einer GitHub-Störung stundenlang nichts
veröffentlichen (HTTP 503 aus der Pages-Schnittstelle). Pages ist deshalb wieder
abgeschaltet, damit es keine zweite, veraltete Adresse gibt. Wieder einschalten:

```
gh api --method POST repos/CSEService/krankmeldung/pages --input -
```

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die App: Kopfzeile, Formular im Rahmen, Installations-Hinweis |
| `manifest.json` | Name, Symbol, Farbe, Vollbildstart |
| `sw.js` | Hintergrunddienst; macht installierbar und meldet fehlendes Netz sauber |
| `_headers` | Cloudflare: Hülle und Dienst nicht zwischenspeichern |
| `bilder/icon-*.png` | App-Symbole, erzeugt aus dem CSE-Logo |
| `aushang-krankmeldung.pdf` | A4-Aushang mit QR-Code zum Aufhängen |
| `tools/icons-bauen.py` | Erzeugt die Symbole neu |
| `tools/qr-aushang.py` | Erzeugt QR-Code und Aushang neu |
| `tools/veroeffentlichen.ps1` | Lädt die App zu Cloudflare Pages hoch |

## Örtlich ansehen

```
python -m http.server 8455 --directory C:\KI-Projekte\CSE-Krankmeldung-App
```

Dann <http://localhost:8455> öffnen. In Edge/Chrome erscheint rechts in der Adressleiste
das Installieren-Symbol.

## Änderungen veröffentlichen

```
pwsh -File tools\veroeffentlichen.ps1
```

Lädt nur die Web-Dateien hoch (Aushang, QR und Werkzeuge bleiben draußen).
Einmalig nötig: `npx wrangler login` — die Anmeldung läuft über das Cloudflare-Konto.

Wichtig: Nach jeder Änderung in `sw.js` die Zahl in `const CACHE = 'krankmeldung-v1'`
hochzählen, sonst behalten schon installierte Geräte den alten Stand.

## Offen

- Absenden des Formulars **im Rahmen** einmal mit einem Testeintrag prüfen
  (Elementor-Formular; das Absenden läuft über die Website selbst).
- Schöner wäre `krank.cse-service.net` statt `cse-krankmeldung.pages.dev`.
  Dafür genügt ein DNS-Eintrag (CNAME), die Website selbst bleibt unangetastet.
