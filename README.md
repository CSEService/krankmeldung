# CSE-Krankmeldung-App

Handy-Hülle für das bestehende Krankmeldungsformular auf <https://cse-service.net/krankmeldung/>.

**Zweck:** Mitarbeiter sollen ein Symbol „Krankmeldung" auf dem Handy haben und mit
einem Fingertipp krankmelden können — **ohne Anmeldung, ohne Passwort, ohne M365/Teams.**

## Was das ist (und was nicht)

- Eine sogenannte PWA: eine gewöhnliche Webseite, die sich auf dem Handy als App ablegen lässt.
- **Kein** App-Store, **keine** Installation im klassischen Sinn, **kein** Konto.
- Das Formular selbst bleibt unverändert auf der Firmen-Website (WordPress/Elementor).
  Diese App zeigt es nur im eigenen Fenster an und liefert Symbol, Name und Vollbildstart.
- An der Website wird **nichts** geändert — wir haben dort keinen Zugriff.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die App: Kopfzeile, Formular im Rahmen, Installations-Hinweis |
| `manifest.json` | Name, Symbol, Farbe, Vollbildstart |
| `sw.js` | Hintergrunddienst; macht installierbar und meldet fehlendes Netz sauber |
| `bilder/icon-*.png` | App-Symbole, erzeugt aus dem CSE-Logo |
| `tools/icons-bauen.py` | Erzeugt die Symbole neu (`python tools\icons-bauen.py`) |

## Örtlich ansehen

```
python -m http.server 8455 --directory C:\KI-Projekte\CSE-Krankmeldung-App
```

Dann <http://localhost:8455> öffnen. In Edge/Chrome erscheint rechts in der Adressleiste
das Installieren-Symbol.

## Veröffentlichen

Der Ordner ist rein statisch — er braucht **keinen** Server mit Programmcode und
**keine** Datenbank. Er kann auf jedem Web-Platz mit HTTPS liegen
(z. B. GitHub Pages, Cloudflare Pages, Netlify). HTTPS ist Pflicht,
sonst bieten die Handys die Installation nicht an.

Wichtig: Nach jeder Änderung in `sw.js` die Zahl in `const CACHE = 'krankmeldung-v1'`
hochzählen, sonst behalten schon installierte Geräte den alten Stand.

## Offen

- Absenden des Formulars **im Rahmen** einmal mit einem Testeintrag prüfen
  (Elementor-Formular; das Absenden läuft über die Website selbst).
