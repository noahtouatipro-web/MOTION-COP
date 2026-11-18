"""Ticket d'Or Galzin — Épiphanie 2027.

Format fini 160 x 75 mm (+ 3 mm de fond perdu). Recto et verso côte à côte dans un seul SVG.
Usage : python3 ticket_or.py            -> ticket-or.svg (N° 01, maquette)
        python3 ticket_or.py --serie    -> numeros/ticket-or-01.svg … ticket-or-15.svg
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo, ovale_prix, tirets  # noqa: E402

TW, TH = 1600, 750      # format fini (0,1 mm)
BLEED = 30              # 3 mm de fond perdu
M, GAP = 100, 200
W, H = M * 2 + TW * 2 + GAP, M * 2 + TH
TOTAL = 15

OR_DEFS = f"""<defs>
  <linearGradient id="Or" x1="0" y1="0" x2="1" y2="0.35">
    <stop offset="0" stop-color="{C['cuivre']}"/>
    <stop offset="0.22" stop-color="{C['cuivre_clair']}"/>
    <stop offset="0.42" stop-color="#FBE6B4"/>
    <stop offset="0.6" stop-color="{C['cuivre_clair']}"/>
    <stop offset="0.82" stop-color="{C['cuivre']}"/>
    <stop offset="1" stop-color="{C['cuivre_clair']}"/>
  </linearGradient>
</defs>"""


def couronne(cx, top, w, color):
    """Couronne des rois stylisée (5 pointes + perles)."""
    h = w * 0.55
    x0, x1, base = cx - w / 2, cx + w / 2, top + h
    pts = [(x0, top + h * 0.25), (x0 + w * 0.25, top + h * 0.55), (cx, top),
           (x1 - w * 0.25, top + h * 0.55), (x1, top + h * 0.25)]
    d = f"M{x0:.0f} {base:.0f}L{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for i in range(1, len(pts)):
        vx = (pts[i - 1][0] + pts[i][0]) / 2
        vy = top + h * 0.62
        d += f"L{vx:.0f} {vy:.0f}L{pts[i][0]:.0f} {pts[i][1]:.0f}"
    d += f"L{x1:.0f} {base:.0f}Z"
    perles = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{w * 0.045:.0f}" fill="{color}"/>' for x, y in pts)
    bande = (f'<rect x="{x0:.0f}" y="{base + w * 0.03:.0f}" width="{w:.0f}" height="{w * 0.1:.0f}" '
             f'rx="{w * 0.03:.0f}" fill="{color}"/>')
    return f'<g id="couronne"><path d="{d}" fill="{color}"/>{perles}{bande}</g>'


def etincelle(cx, cy, r, color):
    k = r * 0.22
    return (f'<path fill="{color}" d="M{cx} {cy - r}Q{cx + k} {cy - k} {cx + r} {cy}'
            f'Q{cx + k} {cy + k} {cx} {cy + r}Q{cx - k} {cy + k} {cx - r} {cy}Q{cx - k} {cy - k} {cx} {cy - r}Z"/>')


def vague_talon(x, w=400):
    """Bord droit ondulé du talon chocolat."""
    return (f"M{x - BLEED} {-BLEED}H{x + w}C{x + w - 45} 150 {x + w + 45} 250 {x + w} 375"
            f"C{x + w - 45} 500 {x + w + 45} 600 {x + w} {TH + BLEED}H{x - BLEED}Z")


def recto(num):
    n = f"{num:02d}"
    cx = 1010
    fond = (f'<g id="FOND"><rect x="{-BLEED}" y="{-BLEED}" width="{TW + 2 * BLEED}" height="{TH + 2 * BLEED}" '
            f'fill="url(#Or)"/></g>')
    deco = ('<g id="DORURE_DECO">'
            f'<rect x="465" y="35" width="1100" height="680" rx="26" fill="none" stroke="{C["chocolat"]}" stroke-width="7"/>'
            f'<rect x="485" y="55" width="1060" height="640" rx="16" fill="none" stroke="{C["chocolat"]}" stroke-width="2.5"/>'
            + etincelle(620, 140, 34, C["blanc"]) + etincelle(1400, 135, 30, C["blanc"])
            + etincelle(1475, 190, 14, C["blanc"]) + etincelle(555, 190, 14, C["blanc"])
            + etincelle(1480, 600, 18, C["blanc"]) + etincelle(545, 610, 18, C["blanc"])
            + '</g>')
    talon = ('<g id="VAGUES">'
             f'<path d="{vague_talon(0)}" fill="{C["chocolat"]}"/>'
             f'<path d="M415 {-BLEED}C370 150 460 250 415 375C370 500 460 600 415 {TH + BLEED}" fill="none" '
             f'stroke="{C["caramel"]}" stroke-width="9"/>'
             '</g>')
    numero = ('<g id="NUMERO">'
              + text(195, 390, "N°", 62, C["cuivre_clair"], spacing=4)
              + text(195, 590, n, 230, C["creme"])
              + text(195, 670, f"SUR {TOTAL}", 52, C["cuivre_clair"], spacing=6)
              + '</g>')
    textes = ('<g id="TEXTES">'
              + couronne(cx, 85, 170, C["chocolat"])
              + text(cx, 395, "TICKET D'OR", 200, C["chocolat"], spacing=4)
              + tirets(cx - 330, 487, "g", C["chocolat"], 0.55)
              + tirets(cx + 330, 487, "d", C["chocolat"], 0.55)
              + text(cx, 518, "Félicitations !", 92, C["chocolat"], font=HEROICA, bold=True)
              + text(cx, 592, "Tu as trouvé l'un des 15 tickets d'or", 50, C["chocolat_fonce"],
                     font=HEROICA, italic=True, bold=True)
              + f'<rect x="640" y="622" width="740" height="62" rx="31" fill="{C["chocolat"]}"/>'
              + text(cx, 666, "ÉPIPHANIE 2027 · À PRÉSENTER EN BOUTIQUE", 36, C["creme"], spacing=2)
              + '</g>')
    lg = f'<g id="LOGO_MENTIONS">{logo(80, 50, 230)}</g>'
    return f'<g id="RECTO" transform="translate({M} {M})">{fond}{deco}{talon}{numero}{textes}{lg}</g>'


def verso(num):
    n = f"{num:02d}"
    ox = M + TW + GAP
    fond = (f'<g id="FOND"><rect x="{-BLEED}" y="{-BLEED}" width="{TW + 2 * BLEED}" height="{TH + 2 * BLEED}" '
            f'fill="{C["creme"]}"/></g>')
    vagues = ('<g id="VAGUES">'
              f'<path fill="{C["chocolat"]}" d="M{-BLEED} {-BLEED}H{TW + BLEED}V150C1250 205 900 120 560 175'
              f'C330 212 140 200 {-BLEED} 170Z"/>'
              f'<path fill="none" stroke="{C["caramel"]}" stroke-width="8" d="M{-BLEED} 192C140 222 330 234 560 197'
              f'C900 142 1250 227 {TW + BLEED} 172"/>'
              f'<path fill="{C["chocolat"]}" d="M{-BLEED} 650C300 622 700 672 1050 637C1300 612 1480 622 {TW + BLEED} 632'
              f'V{TH + BLEED}H{-BLEED}Z"/>'
              '</g>')

    def etape(i, y, l1, l2=None):
        s = (f'<circle cx="120" cy="{y - 18}" r="48" fill="url(#Or)" stroke="{C["chocolat_fonce"]}" stroke-width="5"/>'
             + text(120, y + 8, str(i), 70, C["chocolat_fonce"])
             + text(200, y if not l2 else y - 22, l1, 48, C["chocolat"], font=HEROICA, bold=True, anchor="start"))
        if l2:
            s += text(200, y + 40, l2, 48, C["chocolat"], font=HEROICA, bold=True, anchor="start")
        return s

    textes = ('<g id="TEXTES">'
              + text(TW / 2, 112, "COMMENT RÉCUPÉRER TON LOT ?", 92, C["creme"], spacing=2)
              + etape(1, 300, "Garde ce ticket précieusement.")
              + etape(2, 440, "Apporte-le dans ta boutique Galzin", "avant le ____ / ____ / 2027.")
              + etape(3, 575, "Repars avec ton lot !")
              + text(1330, 262, "TON LOT", 50, C["chocolat"], spacing=4)
              + '</g>')
    lot = '<g id="PRIX">' + ovale_prix(1330, 352, 215, 72, "", "cuivre", rot=-3) + '</g>'
    equipe = ('<g id="EQUIPE">'
              f'<rect x="1100" y="440" width="460" height="160" rx="18" fill="none" stroke="{C["caramel"]}" '
              f'stroke-width="4" stroke-dasharray="14 10"/>'
              + text(1330, 478, "RÉSERVÉ À L'ÉQUIPE", 30, C["caramel"], spacing=3)
              + text(1125, 530, "Boutique : ______________", 30, C["chocolat"], font=HEROICA, anchor="start")
              + text(1125, 580, "Date : ___ / ___    Visa : ______", 30, C["chocolat"], font=HEROICA, anchor="start")
              + '</g>')
    mentions = ('<g id="LOGO_MENTIONS">'
                + text(TW / 2, 686, f"Ticket unique N° {n}/{TOTAL}. Toute copie ou ticket illisible n'est pas valable.",
                       25, C["creme"], font=HEROICA, italic=True, bold=True)
                + text(TW / 2, 716, "Lot non échangeable contre sa valeur en argent. Règlement complet en boutique et sur galzin.fr",
                       25, C["creme"], font=HEROICA, italic=True, bold=True)
                + '</g>')
    return (f'<g id="VERSO" transform="translate({ox} {M})">{fond}{vagues}{textes}{lot}{equipe}{mentions}</g>')


def guides():
    g = '<g id="GUIDES_NE_PAS_IMPRIMER" fill="none" stroke="#FF00FF" stroke-width="2">'
    for ox in (M, M + TW + GAP):
        g += f'<rect x="{ox}" y="{M}" width="{TW}" height="{TH}"/>'
    g += '</g>'
    g += text(M, 60, "RECTO — 160 × 75 mm (+3 mm fond perdu)", 34, "#999999", anchor="start")
    g += text(M + TW + GAP, 60, "VERSO", 34, "#999999", anchor="start")
    return g


def build(num):
    body = (f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>' + OR_DEFS + recto(num) + verso(num) + guides())
    return svg(W, H, body, f"Galzin - Ticket d'Or Epiphanie 2027 - N {num:02d}")


if __name__ == "__main__":
    if "--serie" in sys.argv:
        out = HERE / "numeros"
        out.mkdir(exist_ok=True)
        for i in range(1, TOTAL + 1):
            (out / f"ticket-or-{i:02d}.svg").write_text(build(i), encoding="utf-8")
        print(f"{TOTAL} tickets écrits dans {out}")
    else:
        (HERE / "ticket-or.svg").write_text(build(1), encoding="utf-8")
        print("ticket-or.svg écrit")
