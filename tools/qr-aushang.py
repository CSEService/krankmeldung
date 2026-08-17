# qr-aushang.py — erzeugt QR-Code und Aushang (A4) fuer die Krankmeldungs-App.
# Aufruf:  python tools\qr-aushang.py
# Ergebnis: bilder\qr-krankmeldung.png, aushang-krankmeldung.png, aushang-krankmeldung.pdf
from pathlib import Path
import segno
from PIL import Image, ImageDraw, ImageFont

ADRESSE = "https://cse-krankmeldung.pages.dev/"
BASIS = Path(__file__).resolve().parent.parent

# A4 bei 300 dpi
BREITE, HOEHE = 2480, 3508
BLAU = (27, 110, 194)
DUNKEL = (26, 35, 48)
GRAU = (92, 103, 115)


def schrift(fett: bool, groesse: int) -> ImageFont.FreeTypeFont:
    for name in (["segoeuib.ttf", "arialbd.ttf"] if fett else ["segoeui.ttf", "arial.ttf"]):
        pfad = Path("C:/Windows/Fonts") / name
        if pfad.exists():
            return ImageFont.truetype(str(pfad), groesse)
    return ImageFont.load_default(groesse)


def mittig(zeichner: ImageDraw.ImageDraw, y: int, text: str, font, farbe) -> int:
    """Text mittig setzen, gibt die Unterkante zurueck."""
    links, oben, rechts, unten = zeichner.textbbox((0, 0), text, font=font)
    zeichner.text(((BREITE - (rechts - links)) / 2 - links, y), text, font=font, fill=farbe)
    return y + (unten - oben)


def qr_bauen(wunsch_kante: int) -> Image.Image:
    """QR-Code erzeugen. Die Kantenlaenge wird auf ein ganzes Vielfaches der
    Modulgroesse gerundet – nachtraegliches Skalieren wuerde die Kaestchen
    ungleich breit machen und den Code schlechter lesbar."""
    qr = segno.make(ADRESSE, error="h")
    rand = 2
    module = qr.symbol_size(scale=1, border=rand)[0]
    skala = max(1, round(wunsch_kante / module))
    roh = BASIS / "bilder" / "qr-krankmeldung.png"
    qr.save(roh, scale=skala, border=rand, dark="#000000", light="#ffffff")
    return Image.open(roh).convert("RGB")


def aushang() -> None:
    blatt = Image.new("RGB", (BREITE, HOEHE), "white")
    z = ImageDraw.Draw(blatt)

    # Blauer Balken oben
    z.rectangle([0, 0, BREITE, 40], fill=BLAU)

    # Logo
    logo = Image.open(BASIS / "bilder" / "logo-quelle.png").convert("RGBA")
    faktor = 760 / logo.width
    logo = logo.resize((760, int(logo.height * faktor)), Image.LANCZOS)
    blatt.paste(logo, ((BREITE - logo.width) // 2, 190), logo)

    y = 190 + logo.height + 180
    y = mittig(z, y, "Krank? Einfach melden.", schrift(True, 150), DUNKEL) + 95
    y = mittig(z, y, "Krankmeldung direkt vom Handy – ohne Anmeldung,", schrift(False, 68), GRAU) + 22
    y = mittig(z, y, "ohne Passwort, in unter einer Minute.", schrift(False, 68), GRAU) + 110

    # QR-Code mit dünnem Rahmen
    qr = qr_bauen(1150)
    kante = qr.width
    x = (BREITE - kante) // 2
    z.rectangle([x - 26, y - 26, x + kante + 26, y + kante + 26], outline=BLAU, width=8)
    blatt.paste(qr, (x, y))
    y += kante + 70

    y = mittig(z, y, ADRESSE.replace("https://", ""), schrift(False, 52), BLAU) + 120

    # Drei Schritte
    schritte = [
        "1.  QR-Code mit der Handy-Kamera scannen",
        "2.  Hinweis antippen: „Installieren“ (Android) bzw.",
        "     „Teilen“ → „Zum Home-Bildschirm“ (iPhone)",
        "3.  Fertig – ab jetzt genügt ein Fingertipp aufs Symbol",
    ]
    fs = schrift(False, 66)
    breiteste = max(z.textbbox((0, 0), s, font=fs)[2] for s in schritte)
    links = (BREITE - breiteste) // 2
    for s in schritte:
        z.text((links, y), s, font=fs, fill=DUNKEL)
        y += 100

    # Fusszeile
    z.rectangle([0, HOEHE - 130, BREITE, HOEHE], fill=BLAU)
    mittig(z, HOEHE - 100, "CSE Service GmbH  ·  Krankmeldung  ·  www.cse-service.net", schrift(False, 48), "white")

    blatt.save(BASIS / "aushang-krankmeldung.png", "PNG", optimize=True)
    blatt.save(BASIS / "aushang-krankmeldung.pdf", "PDF", resolution=300)
    print("aushang-krankmeldung.png / .pdf erzeugt")
    print("bilder/qr-krankmeldung.png erzeugt")


if __name__ == "__main__":
    aushang()
