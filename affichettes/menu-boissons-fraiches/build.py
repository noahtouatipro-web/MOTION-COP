"""Menu « Boissons fraîches » Galzin, 40 x 60 cm — version charte (bandeau vague, logo, Impact + Eroika Slab,
turquoise réservé au froid). Tarifs 2026 (fichier NOUVEAUX_TARIF_2026.xlsx, onglets
« BSA - BOISSONS FROIDES » et « BA - BIERES »).

Usage : python3 build.py  ->  galzin-menu-boissons-fraiches.svg (à ouvrir dans Illustrator,
puis Fichier > Enregistrer sous > Adobe Illustrator (.ai)).
Dessiné sur une grille 1024 x 1536 puis mis à l'échelle 40 x 60 cm.
Calques : FOND, VAGUES, PHOTO, LOGO, TITRE, CARTE (un groupe par ligne : nom + contenances + prix), MENTIONS.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg_illustrator, text, image  # noqa: E402

GW, GH = 1024, 1536        # grille
CH, CF, CR, CA, TQ = C["chocolat"], C["chocolat_fonce"], C["creme"], C["caramel"], "#3E8F90"


def prix(p):
    return f"{p:.2f}".replace(".", ",") + "€"


# (famille, [(nom, [(contenance, prix), ...]), ...])  — tarifs 2026, contenances de la plus petite à la plus grande
CARTE = [
    ("SODAS", [
        ("Coca-Cola", [("33 cl", 2.25), ("50 cl", 2.85), ("1,25 l", 4.15)]),
        ("Coca-Cola Zéro", [("33 cl", 2.25), ("50 cl", 2.85)]),
        ("Coca-Cola Cherry", [("33 cl", 2.25), ("50 cl", 2.85)]),
        ("Fanta", [("33 cl", 2.25), ("50 cl", 2.85)]),
        ("Fanta Dragon", [("33 cl", 2.25)]),
        ("Sprite", [("33 cl", 2.25), ("50 cl", 2.85)]),
    ]),
    ("THÉS GLACÉS & JUS", [
        ("Fuzetea", [("33 cl", 2.25), ("40 cl", 2.85)]),
        ("Tropico", [("mini", 1.75), ("33 cl", 2.25), ("40 cl", 2.85)]),
        ("Minute Maid orange", [("33 cl", 2.25)]),
        ("Minute Maid pomme", [("33 cl", 2.25)]),
        ("Limonade", [("27,5 cl", 2.85)]),
    ]),
    ("ÉNERGISANTS", [
        ("Monster mangue", [("50 cl", 3.25)]),
        ("Red Bull", [("25 cl", 3.25)]),
    ]),
    ("EAUX", [
        ("Eau", [("50 cl", 1.85), ("1,5 l", 2.95)]),
        ("Volvic fraise ou citron", [("50 cl", 2.85)]),
        ("San Pellegrino", [("50 cl", 2.55)]),
        ("Perrier", [("50 cl", 2.85)]),
    ]),
    ("BIÈRES", [
        ("Heineken", [("33 cl", 2.90)]),
        ("Desperados", [("33 cl", 3.90)]),
        ("Bière artisanale", [("", 3.90)]),
    ]),
]

X0, X1 = 360, 994                 # colonne carte
COLS = [994, 862, 730]            # bord droit des colonnes de prix (de droite à gauche)


def vagues():
    haut = "M0 0H1024V222C880 268 760 212 600 234C430 258 250 280 0 246Z"
    lis = "M0 258C250 292 430 270 600 246C760 224 880 280 1024 234"
    bas = "M0 1474C200 1446 380 1494 600 1470C800 1448 900 1426 1024 1436V1536H0Z"
    lis_b = "M0 1462C200 1434 380 1482 600 1458C800 1436 900 1414 1024 1424"
    return (f'<g id="VAGUES"><path fill="{CH}" d="{haut}"/>'
            f'<path fill="none" stroke="{CA}" stroke-width="7" d="{lis}"/>'
            f'<path fill="{CH}" d="{bas}"/><path fill="none" stroke="{CA}" stroke-width="7" d="{lis_b}"/></g>')


def titre():
    px, py, pw, ph = 650, 200, 340, 92
    return ('<g id="TITRE">'
            + text(642, 168, "BOISSONS", 150, CR, IMPACT, spacing=2)
            + f'<g transform="rotate(-3 {px + pw / 2} {py + ph / 2})">'
              f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="30" fill="url(#Turquoise)"/>'
            + text(px + pw / 2, py + 66, "fraîches", 66, CR, HEROICA, italic=True, bold=True)
            + '</g></g>')


def carte():
    o, y = [], 312
    for famille, lignes in CARTE:
        o.append(f'<g id="famille-{famille.split()[0].lower()}">'
                 + text(X0, y + 34, famille, 36, TQ, IMPACT, "start", spacing=1)
                 + f'<path d="M{X0} {y + 46}H{X1}" stroke="{C["turquoise"]}" stroke-width="3.5"/></g>')
        y += 52
        for nom, cases in lignes:
            yb = y + 30                                    # ligne de base du nom et des prix
            g = [text(X0, yb, nom, 29, CH, HEROICA, "start", bold=True)]
            for (lab, p), xd in zip(reversed(cases), COLS):
                g.append(text(xd, yb, prix(p), 29, CH, HEROICA, "end", bold=True))
                if lab:
                    g.append(text(xd - 84, yb - 1, lab, 17, CA, IMPACT, "end"))
            g.append(f'<path d="M{X0} {yb + 11}H{X1}" stroke="{CA}" stroke-width="1.8" '
                     f'stroke-dasharray="0.1 6" stroke-linecap="round"/>')
            o.append(f'<g id="ligne-{nom.lower().replace(" ", "-")}">' + "".join(g) + '</g>')
            y += 40
        y += 12
    return '<g id="CARTE">' + "".join(o) + '</g>'


def menu():
    L = [f'<g id="FOND"><rect width="{GW}" height="{GH}" fill="{CR}"/></g>', vagues(),
         '<g id="PHOTO">' + image(HERE / "images/photo-coca-net.png", 14, 380, 330, 1072, 1400, id="photo-coca") + '</g>',
         '<g id="LOGO">' + image(HERE / "images/galzin-logo.png", 30, 20, 204, 204, 900, id="galzin-logo") + '</g>',
         titre(), carte(),
         '<g id="MENTIONS">'
         + text(GW / 2, GH - 40, "L'abus d'alcool est dangereux pour la santé, à consommer avec modération.",
                17, CR, HEROICA, italic=True, bold=True)
         + text(GW / 2, GH - 16, "Dans la limite des stocks disponibles · Photos non contractuelles",
                17, CR, HEROICA, italic=True, bold=True)
         + '</g>']
    # coordonnées aplaties en points : textes à leur vraie taille dans Illustrator, groupes nommés de 1er niveau
    return svg_illustrator(400, 600, "\n".join(L), GW, "Galzin - Menu boissons fraîches")


if __name__ == "__main__":
    s = menu()
    (HERE / "galzin-menu-boissons-fraiches.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
