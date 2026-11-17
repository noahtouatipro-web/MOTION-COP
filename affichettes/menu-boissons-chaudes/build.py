"""Menu « Boissons chaudes » Galzin, A4 — version charte (bandeau vague, logo, Impact + Eroika Slab,
ovales de prix cuivrés). Tarifs 2026 (fichier NOUVEAUX_TARIF_2026.xlsx, onglet « BSA - BOISSONS CHAUDES »).

Usage : python3 build.py  ->  galzin-menu-boissons-chaudes.svg (à ouvrir dans Illustrator,
puis Fichier > Enregistrer sous > Adobe Illustrator (.ai)).
Dessiné sur une grille 1024 x 1448 (proportions A4) puis mis à l'échelle 21 x 29,7 cm.
Calques : FOND, VAGUES, PHOTO, LOGO, TITRE, CARTE (un groupe par ligne : nom + prix), MENTIONS.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg_illustrator, text, image, ovale_prix  # noqa: E402

GW, GH = 1024, 1448        # grille
CH, CF, CR, CA = C["chocolat"], C["chocolat_fonce"], C["creme"], C["caramel"]


def prix(p):
    return f"{p:.2f}".replace(".", ",") + "€"


# (famille, [(nom, [(étiquette, prix), ...]), ...])  — tarifs 2026
CARTE = [
    ("CAFÉS", [
        ("Café ou déca", [("SIMPLE", 1.65), ("DOUBLE", 2.55)]),
        ("Café crème", [("", 2.85)]),
        ("Cappuccino", [("", 2.85)]),
    ]),
    ("CHOCOLAT CHAUD", [
        ("Chocolat chaud", [("PETIT", 2.35), ("GRAND", 2.85)]),
    ]),
    ("THÉS & INFUSIONS", [
        ("Thé ou infusion", [("", 2.90)]),
    ]),
]

X0, X1 = 352, 992                 # colonne carte
COLS = [926, 776]                 # centres des ovales (de droite à gauche)


def vagues():
    haut = ("M0 0H1024V236C880 286 760 226 600 250C430 276 250 300 0 262Z")
    lis = ("M0 274C250 312 430 288 600 262C760 238 880 298 1024 248")
    bas = ("M0 1370C200 1340 380 1392 600 1366C800 1342 900 1318 1024 1330V1448H0Z")
    lis_b = ("M0 1358C200 1328 380 1380 600 1354C800 1330 900 1306 1024 1318")
    return (f'<g id="VAGUES"><path fill="{CH}" d="{haut}"/>'
            f'<path fill="none" stroke="{CA}" stroke-width="7" d="{lis}"/>'
            f'<path fill="{CH}" d="{bas}"/><path fill="none" stroke="{CA}" stroke-width="7" d="{lis_b}"/></g>')


def titre():
    pill_x, pill_y, pw, ph = 664, 214, 320, 92
    return ('<g id="TITRE">'
            + text(642, 178, "BOISSONS", 158, CR, IMPACT, spacing=2)
            + f'<g transform="rotate(-3 {pill_x + pw / 2} {pill_y + ph / 2})">'
              f'<rect x="{pill_x}" y="{pill_y}" width="{pw}" height="{ph}" rx="30" fill="url(#Cuivre)" '
              f'stroke="{CF}" stroke-width="5"/>'
            + text(pill_x + pw / 2, pill_y + 66, "chaudes", 66, CF, HEROICA, italic=True, bold=True)
            + '</g></g>')


def photo():
    x, y, w, h = 36, 330, 286, 1020
    return ('<defs><clipPath id="ClipPhoto"><rect x="{0}" y="{1}" width="{2}" height="{3}" rx="26"/></clipPath></defs>'
            .format(x, y, w, h)
            + '<g id="PHOTO"><g clip-path="url(#ClipPhoto)">'
            + image(HERE / "images/photo-cafe.jpg", x, y, w, h, 1400, id="photo-cafe").replace("meet", "slice")
            + f'</g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="none" stroke="{CA}" '
              f'stroke-width="6"/></g>')


def carte():
    o, y = [], 372
    for famille, lignes in CARTE:
        o.append(f'<g id="famille-{famille.split()[0].lower()}">'
                 + text(X0, y + 40, famille, 46, CH, IMPACT, "start", spacing=1)
                 + f'<path d="M{X0} {y + 58}H{X1}" stroke="{CA}" stroke-width="4"/></g>')
        y += 82
        for nom, cases in lignes:
            yb = y + 70                                    # ligne de base du nom
            g = [text(X0, yb, nom, 44, CH, HEROICA, "start", bold=True)]
            for (lab, p), cx in zip(reversed(cases), COLS):
                if lab:
                    g.append(text(cx, yb - 50, lab, 22, CA, IMPACT, spacing=2))
                g.append(ovale_prix(cx, yb - 13, 66, 32, prix(p), size=36))
            g.append(f'<path d="M{X0} {yb + 30}H{X1}" stroke="{CA}" stroke-width="2.4" '
                     f'stroke-dasharray="0.1 9" stroke-linecap="round"/>')
            o.append(f'<g id="ligne-{nom.split()[0].lower()}">' + "".join(g) + '</g>')
            y += 118
        y += 40
    return '<g id="CARTE">' + "".join(o) + '</g>'


def menu():
    L = [f'<g id="FOND"><rect width="{GW}" height="{GH}" fill="{CR}"/></g>', vagues(), photo(),
         '<g id="LOGO">' + image(HERE / "images/galzin-logo.png", 30, 22, 214, 214, 900, id="galzin-logo") + '</g>',
         titre(), carte(),
         '<g id="MENTIONS">' + text(GW - 40, GH - 30, "Photos non contractuelles", 22, CR, HEROICA, "end",
                                    italic=True, bold=True)
         + '</g>']
    # coordonnées aplaties en points : textes à leur vraie taille dans Illustrator, groupes nommés de 1er niveau
    return svg_illustrator(210, 297, "\n".join(L), GW, "Galzin - Menu boissons chaudes")


if __name__ == "__main__":
    s = menu()
    (HERE / "galzin-menu-boissons-chaudes.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
