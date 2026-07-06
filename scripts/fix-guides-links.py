#!/usr/bin/env python3
"""
Add 6 missing pages to the "Guides et outils" section across all site pages.
- Par statut: +Alsace-Moselle, +Brut net 2026
- Comprendre: +Cadre vs Non-cadre
- Outils: +Temps partiel, +Simulateur augmentation, +Widget intégrable
"""
import os
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = '<a href="{href}" class="block rounded-xl border border-slate-200 bg-white p-3 text-center hover:border-brand-300 hover:shadow-sm transition-all"><span class="block text-sm font-medium text-slate-900">{label}</span></a>'

# Strings to find → replace (add links before closing </div></div> of each category)
REPLACEMENTS = [
    # 1. Add to "Par statut": after Stage
    (
        LINK.format(href="/salaire-brut-net-stage/", label="Stage") + '</div></div>',
        LINK.format(href="/salaire-brut-net-stage/", label="Stage")
        + LINK.format(href="/salaire-brut-net-alsace-moselle/", label="Alsace-Moselle")
        + LINK.format(href="/salaire-brut-net-2026/", label="Brut net 2026")
        + '</div></div>',
    ),
    # 2. Add to "Comprendre": after Lire sa fiche de paie
    (
        LINK.format(href="/lire-fiche-de-paie/", label="Lire sa fiche de paie") + '</div></div>',
        LINK.format(href="/lire-fiche-de-paie/", label="Lire sa fiche de paie")
        + LINK.format(href="/cadre-vs-non-cadre/", label="Cadre vs Non-cadre")
        + '</div></div>',
    ),
    # 3. Add to "Outils": after Simulateur impôts
    (
        LINK.format(href="/simulateur-impot-sur-le-revenu/", label="Simulateur imp\u00f4ts") + '</div></div>',
        LINK.format(href="/simulateur-impot-sur-le-revenu/", label="Simulateur imp\u00f4ts")
        + LINK.format(href="/calculateur-temps-partiel/", label="Temps partiel")
        + LINK.format(href="/simulateur-augmentation/", label="Simulateur augmentation")
        + LINK.format(href="/widget/", label="Widget int\u00e9grable")
        + '</div></div>',
    ),
]

# Process all HTML files (excluding index.html which was already fixed)
html_files = glob.glob(os.path.join(BASE, "*/index.html"))
# Also check guide pages that might be at différent paths
html_files = [f for f in html_files if "/scripts/" not in f and "/node_modules/" not in f]

updated = 0
skipped = 0

for filepath in sorted(html_files):
    rel = os.path.relpath(filepath, BASE)

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Skip redirect pages (they don't have Guides et outils)
    if 'meta http-equiv="refresh"' in html:
        continue

    # Skip homepage (already fixed separately)
    if rel == "index.html":
        continue

    original = html
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)

    if html != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        updated += 1
    else:
        # Check if already has the links
        if "/cadre-vs-non-cadre/" in original and "/calculateur-temps-partiel/" in original:
            skipped += 1
        else:
            # Page doesn't have the Guides et outils section at all
            pass

print(f"Updated {updated} pages")
print(f"Already up-to-date: {skipped}")
