# icons-bauen.py — erzeugt die App-Symbole aus dem CSE-Logo.
# Aufruf:  python tools\icons-bauen.py
# Quelle:  bilder\logo-quelle.png (Logo von cse-service.net)
from pathlib import Path
from PIL import Image

BASIS = Path(__file__).resolve().parent.parent
QUELLE = BASIS / "bilder" / "logo-quelle.png"
HINTERGRUND = (255, 255, 255, 255)


def symbol(groesse: int, rand_anteil: float, ziel: Path) -> None:
    """Logo mittig auf eine weisse Quadratflaeche setzen."""
    logo = Image.open(QUELLE).convert("RGBA")
    platz = int(groesse * (1 - 2 * rand_anteil))
    faktor = min(platz / logo.width, platz / logo.height)
    logo = logo.resize((int(logo.width * faktor), int(logo.height * faktor)), Image.LANCZOS)

    blatt = Image.new("RGBA", (groesse, groesse), HINTERGRUND)
    blatt.alpha_composite(logo, ((groesse - logo.width) // 2, (groesse - logo.height) // 2))
    blatt.convert("RGB").save(ziel, "PNG", optimize=True)
    print(f"{ziel.name}: {groesse}x{groesse}")


if __name__ == "__main__":
    ordner = BASIS / "bilder"
    # Normale Symbole: schmaler Rand, damit das Logo gross wirkt
    symbol(192, 0.08, ordner / "icon-192.png")
    symbol(512, 0.08, ordner / "icon-512.png")
    # Apple legt selbst runde Ecken darueber
    symbol(180, 0.08, ordner / "icon-180.png")
    # Android schneidet Symbole zu Kreisen/Formen zu -> mehr Luft am Rand
    symbol(512, 0.22, ordner / "icon-maskable-512.png")
