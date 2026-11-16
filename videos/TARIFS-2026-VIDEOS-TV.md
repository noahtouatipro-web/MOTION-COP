# Tarifs 2026 — mise à jour des vidéos TV

Source : `NOUVEAUX_TARIF_2026.xlsx` (tarifs boutiques 2026). Prix appliqués et re-rendus :

| Vidéo | Avant | Après |
|---|---|---|
| `galzin-3plus1` | Croissant 0€90 pièce par 4 (seul 1,20 €) · Chocolatine 1€05 pièce par 4 (seule 1,40 €) | Affichage **prix du lot** : croissants **3€65 les 4** (seul 1,25 €, « au lieu de 5,00 € ») · chocolatines **4€25 les 4** (seule 1,45 €, « au lieu de 5,80 € ») |
| `galzin-baguette` | 1€00 seule · 0€90 par 2 (1,80 € les 2) · 4 €/kg et 3,60 €/kg | **1€10** seule · **0€95** par 2 (**1,90 €** les 2) · **4,40 €/kg** et **3,80 €/kg** (baguette 250 g) |
| `galzin-americain` | Seul 8,90 € · Formule 10,50 € | Seul 8,90 € · Formule **11,50 €** |
| `galzin-sandwich-panini` | 7,20 € · 9,90 € | **7,50 €** · **10,20 €** (police du 2e prix réduite à 112 px pour tenir dans l'ovale) |
| `galzin-salade-wrap` | 8,20 € · 10,90 € | **8,50 €** · **11,90 €** |
| `galzin-tielles` | Lot 3+1 11,90 € | **12,90 €** |
| `galzin-pizza` (rouge + brun) | 25 € · « XL (32 cm) » | **29 €** · « XL (30 cm) » |
| `galzin-pizza-semaine` | 8,90 € | **9,90 €** |
| `galzin-menu`, `-menu-plateau`, `-menu-affiche` | 5€50 | **5€90** |
| `galzin-plus`, `galzin-plus-sandwich` | « Pour seulement 2,90 € » | « **À partir de** 2,90 € » (frites 2,90 € / salade 2,95 €) |
| `galzin-prix-garantis` | 6,20 € · 9,50 € · 9,90 € | **6,50 €** · **9,90 €** · **10,90 €** |
| `galzin-petit-dej` | Formule 3€80 · +1 € · +0,30 € | Formule **3€90** · +1 € · +0,30 € (inchangés) |
| `galzin-carte-pizzas` | voir tableau | Toutes +1 € ; **Tartiflette 9,90 €** (prix du tableau, remontée en 2e position) |
| `galzin-affiches` | Croissant 1,20 · Chocolatine 1,40 · Baguette 1,00 · Tielles 11,90 | **1,25** · **1,45** · **1,10** · **12,90** (Américain 8,90 inchangé) |

Version **brune** de `galzin-pizza` : la source ne contient que la version rouge. Pour la brune, remplacer
`--bg-center: #8a1f17` → `#49321f` et `--bg-edge: #3d0906` → `#1e140b` le temps du rendu.

## Hypothèses prises (à valider)

- Baguette « vendue seule » = prix de la **baguette tradition** (1,10 €) — pas de ligne « baguette » simple dans le tableau.
- Lots 3+1 : prix du tableau (**3,65 €** / **4,25 €**), même s'ils ne valent pas 3 × le prix unitaire.

## En attente

- `galzin-minions-tv` / `galzin-minions-tiktok` (galettes 4/6/8 parts) : prix 2027 non fixés dans le tableau.
- Pizza **Chorizo** (9,90 €) pas encore ajoutée à la carte : il manque sa composition.
