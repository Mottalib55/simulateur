#!/usr/bin/env python3
"""
patch_eeat.py — E-E-A-T improvements for salairebrutonet.com
Adds: visible author byline + dates under h1, sources box before FAQ, inline source links
Skips: prime-brut-en-net/
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP_DIRS = ['prime-brut-en-net']

# Byline + dates HTML block (injected after </h1>)
BYLINE_HTML = '''
                <div class="flex flex-wrap items-center gap-3 text-sm text-slate-500 mt-3">
                    <div class="flex items-center gap-2">
                        <img src="/team/mottalib-radif.jpg" alt="Mottalib Radif" class="h-6 w-6 rounded-full object-cover" width="24" height="24" loading="lazy">
                        <span>Par <a href="/a-propos/" class="font-medium text-slate-700 hover:text-brand-600">Mottalib Radif</a></span>
                    </div>
                    <span class="text-slate-300">&middot;</span>
                    <time datetime="2026-01-15">Publi\u00e9 le 15 janv. 2026</time>
                    <span class="text-slate-300">&middot;</span>
                    <time datetime="2026-06-20">Mis \u00e0 jour le 20 juin 2026</time>
                </div>'''

# Source URLs
SRC_URSSAF_TAUX = ('URSSAF \u2013 Taux de cotisations sociales 2026', 'https://www.urssaf.fr/accueil/taux-baremes/taux-cotisations-sociales.html')
SRC_URSSAF_PLAFONDS = ('URSSAF \u2013 Plafonds de S\u00e9curit\u00e9 sociale', 'https://www.urssaf.fr/accueil/taux-baremes/plafonds.html')
SRC_AGIRC_ARRCO = ('AGIRC-ARRCO \u2013 Retraite compl\u00e9mentaire', 'https://www.agirc-arrco.fr/')
SRC_SERVICE_PUBLIC_SMIC = ('Service-Public.fr \u2013 SMIC 2026', 'https://www.service-public.fr/particuliers/vosdroits/F2300')
SRC_IMPOTS_PAS = ('Imp\u00f4ts.gouv.fr \u2013 Pr\u00e9l\u00e8vement \u00e0 la source', 'https://www.impots.gouv.fr/particulier/le-prélèvement-la-source')
SRC_INSEE = ('INSEE \u2013 Salaires dans le secteur priv\u00e9', 'https://www.insee.fr/fr/statistiques/serie/001567616')
SRC_LEGIFRANCE = ('L\u00e9gifrance \u2013 Code du travail', 'https://www.legifrance.gouv.fr/')
SRC_SERVICE_PUBLIC_FICHE = ('Service-Public.fr \u2013 Fiche de paie', 'https://www.service-public.fr/particuliers/vosdroits/F559')
SRC_SERVICE_PUBLIC_HEURES_SUP = ('Service-Public.fr \u2013 Heures suppl\u00e9mentaires', 'https://www.service-public.fr/particuliers/vosdroits/F2391')
SRC_URSSAF_AVN = ('URSSAF \u2013 Avantages en nature', 'https://www.urssaf.fr/accueil/taux-baremes/avantages-en-nature.html')
SRC_SERVICE_PUBLIC_FP = ('Service-Public.fr \u2013 R\u00e9mun\u00e9ration fonction publique', 'https://www.service-public.fr/particuliers/vosdroits/F461')
SRC_URSSAF_AE = ('URSSAF \u2013 Auto-entrepreneur', 'https://www.autoentrepreneur.urssaf.fr/')
SRC_SERVICE_PUBLIC_APPRENTI = ('Service-Public.fr \u2013 Apprentissage', 'https://www.service-public.fr/particuliers/vosdroits/F2918')
SRC_SERVICE_PUBLIC_INTERIM = ('Service-Public.fr \u2013 Travail int\u00e9rimaire', 'https://www.service-public.fr/particuliers/vosdroits/F11215')
SRC_SERVICE_PUBLIC_STAGE = ('Service-Public.fr \u2013 Gratification de stage', 'https://www.service-public.fr/particuliers/vosdroits/F32131')
SRC_IMPOTS_BAREME = ('Imp\u00f4ts.gouv.fr \u2013 Bar\u00e8me de l\'imp\u00f4t sur le revenu', 'https://www.impots.gouv.fr/particulier/questions/comment-est-calcule-limpot-sur-le-revenu')
SRC_URSSAF_ALSACE = ('URSSAF \u2013 Cotisations Alsace-Moselle', 'https://www.urssaf.fr/accueil/taux-baremes/taux-cotisations-sociales.html')

# Per-page source mapping: page_slug -> list of (label, url)
PAGE_SOURCES = {
    'salaire-brut-net-cadre': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS, SRC_AGIRC_ARRCO],
    'salaire-brut-net-non-cadre': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS],
    'salaire-brut-net-fonction-publique': [SRC_SERVICE_PUBLIC_FP, SRC_URSSAF_TAUX],
    'salaire-brut-net-auto-entrepreneur': [SRC_URSSAF_AE, SRC_URSSAF_TAUX],
    'salaire-brut-net-alternance-apprentissage': [SRC_SERVICE_PUBLIC_APPRENTI, SRC_LEGIFRANCE, SRC_URSSAF_TAUX],
    'salaire-brut-net-interim': [SRC_SERVICE_PUBLIC_INTERIM, SRC_URSSAF_TAUX],
    'salaire-brut-net-stage': [SRC_SERVICE_PUBLIC_STAGE, SRC_LEGIFRANCE],
    'salaire-brut-net-mensuel': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS],
    'salaire-brut-net-annuel': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS],
    'salaire-brut-net-horaire': [SRC_URSSAF_TAUX, SRC_SERVICE_PUBLIC_SMIC],
    'salaire-brut-net-journalier': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS],
    'taux-horaire-brut-net': [SRC_URSSAF_TAUX, SRC_SERVICE_PUBLIC_SMIC],
    'différence-salaire-brut-net': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS],
    'cotisations-sociales-salariales': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS, SRC_AGIRC_ARRCO],
    'salaire-net-imposable': [SRC_IMPOTS_PAS, SRC_URSSAF_TAUX],
    'salaire-net-avant-après-impôt': [SRC_IMPOTS_PAS, SRC_IMPOTS_BAREME],
    'lire-fiche-de-paie': [SRC_SERVICE_PUBLIC_FICHE, SRC_URSSAF_TAUX],
    'salaire-moyen-france': [SRC_INSEE, SRC_URSSAF_TAUX],
    'négocier-salaire': [SRC_INSEE, SRC_SERVICE_PUBLIC_SMIC],
    'coût-employeur': [SRC_URSSAF_TAUX, SRC_URSSAF_PLAFONDS],
    'cadre-vs-non-cadre': [SRC_URSSAF_TAUX, SRC_AGIRC_ARRCO],
    'salaire-brut-net-alsace-moselle': [SRC_URSSAF_ALSACE, SRC_URSSAF_PLAFONDS],
    'smic-brut-net-2026': [SRC_SERVICE_PUBLIC_SMIC, SRC_LEGIFRANCE, SRC_URSSAF_TAUX],
    'salaire-brut-net-2026': [SRC_URSSAF_TAUX, SRC_SERVICE_PUBLIC_SMIC, SRC_URSSAF_PLAFONDS],
    '13eme-mois-brut-net': [SRC_URSSAF_TAUX, SRC_LEGIFRANCE],
    'heures-supplémentaires-brut-net': [SRC_SERVICE_PUBLIC_HEURES_SUP, SRC_LEGIFRANCE, SRC_URSSAF_TAUX],
    'avantages-en-nature': [SRC_URSSAF_AVN, SRC_URSSAF_TAUX],
}

# All pages to patch with byline+dates (guides + tools, no sources for tools)
ALL_PAGES = list(PAGE_SOURCES.keys()) + [
    'calculateur-coût-employeur',
    'calculateur-heures-supplémentaires',
    'calculateur-temps-partiel',
    'comparateur-salaire-net-par-pays',
    'simulateur-augmentation',
    'simulateur-impôt-sur-le-revenu',
    'glossaire',
    'a-propos',
    'mentions-legales',
    'mission',
]


def build_sources_box(sources):
    """Build the Sources officielles HTML block."""
    items = '\n'.join(
        f'        <li><a href="{url}" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700 underline">{label}</a></li>'
        for label, url in sources
    )
    return f'''
                <div class="mt-10 rounded-xl border border-slate-200 bg-slate-50 p-5 not-prose">
                    <p class="text-sm font-semibold text-slate-700 mb-2">Sources officielles</p>
                    <ul class="space-y-1 text-sm text-slate-600">
{items}
                    </ul>
                </div>'''


def add_byline_under_h1(html):
    """Add byline+dates block right after the </h1> tag inside the pb-6 section."""
    # Check if byline already present near h1
    if 'datetime="2026-01-15"' in html:
        return html

    # Find the </h1> tag and inject byline after it
    # Pattern: </h1> possibly followed by whitespace, inside a section with pb-6
    pattern = r'(</h1>)\s*(\n\s*</div>\s*\n\s*</section>)'
    match = re.search(pattern, html)
    if match:
        replacement = match.group(1) + BYLINE_HTML + '\n' + match.group(2).lstrip('\n')
        html = html[:match.start()] + replacement + html[match.end():]
    return html


def add_sources_box(html, sources):
    """Add sources box before the FAQ section."""
    if 'Sources officielles' in html:
        return html
    if not sources:
        return html

    box = build_sources_box(sources)

    # Find the closing </div></section> right before the FAQ section
    # The FAQ section starts with: <section class="py-12 px-4"> containing "Questions fréquentes"
    faq_pattern = r'(\s*</div>\s*\n\s*</section>\s*\n)(\s*<section class="py-12 px-4">[\s\S]{0,200}Questions fr)'
    match = re.search(faq_pattern, html)
    if match:
        # Insert the sources box at the end of the prose div, before </div></section>
        # Find the </div> that closes the prose div
        pre_faq = match.group(1)
        faq_start = match.group(2)
        # Insert sources box before the closing </div></section>
        # We need to insert inside the prose section, before its closing tags
        insert_point = match.start()
        # Go back to find the right place - just before </div>\n</section> before FAQ
        html = html[:insert_point] + box + html[insert_point:]
        return html

    # Fallback: try inserting before any section containing "Questions fréquentes"
    faq_idx = html.find('Questions fréquentes')
    if faq_idx == -1:
        faq_idx = html.find('Questions fr')
    if faq_idx > 0:
        # Find the <section that contains this
        section_start = html.rfind('<section', 0, faq_idx)
        if section_start > 0:
            html = html[:section_start] + box + '\n' + html[section_start:]

    return html


def add_inline_source_links(html, page_slug):
    """Add inline links to official sources in the article content.
    Only adds a few key links per page to avoid over-linking."""

    # Only add inline links for pages with sources
    if page_slug not in PAGE_SOURCES:
        return html

    sources = PAGE_SOURCES[page_slug]
    source_urls = {url for _, url in sources}

    # Skip if inline links already present
    for _, url in sources:
        if url in html:
            return html

    # Define inline link patterns per source URL
    # Each entry: (text_pattern, replacement_with_link, source_url_to_check)
    inline_rules = []

    if any('taux-cotisations' in url for _, url in sources):
        # Add link on first mention of cotisations rates
        inline_rules.append((
            r'(<strong>Vieillesse plafonn\u00e9e</strong>)',
            r'<a href="https://www.urssaf.fr/accueil/taux-baremes/taux-cotisations-sociales.html" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'urssaf.fr/accueil/taux-baremes/taux-cotisations'
        ))

    if any('plafonds' in url for _, url in sources):
        # Add link on PSS mention
        inline_rules.append((
            r'(\b3\s*864\s*€(?:\s*/mois| par mois)?)',
            r'<a href="https://www.urssaf.fr/accueil/taux-baremes/plafonds.html" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'urssaf.fr/accueil/taux-baremes/plafonds'
        ))

    if any('F2300' in url for _, url in sources):
        # Add link on SMIC mention
        inline_rules.append((
            r'(<strong>11,88\s*€[^<]*</strong>)',
            r'<a href="https://www.service-public.fr/particuliers/vosdroits/F2300" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'service-public.fr/particuliers/vosdroits/F2300'
        ))
        # Also try: SMIC a été revalorisé à
        inline_rules.append((
            r'(1\s*801,80\s*€\s*brut)',
            r'<a href="https://www.service-public.fr/particuliers/vosdroits/F2300" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'service-public.fr/particuliers/vosdroits/F2300'
        ))

    if any('agirc-arrco.fr' in url for _, url in sources):
        # Add link on AGIRC-ARRCO mention
        inline_rules.append((
            r'(<strong>AGIRC-ARRCO Tranche 1</strong>)',
            r'<a href="https://www.agirc-arrco.fr/" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'agirc-arrco.fr'
        ))

    if any('prélèvement-la-source' in url for _, url in sources):
        inline_rules.append((
            r'(pr\u00e9l\u00e8vement \u00e0 la source)',
            r'<a href="https://www.impots.gouv.fr/particulier/le-prélèvement-la-source" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'impots.gouv.fr'
        ))

    if any('insee.fr' in url for _, url in sources):
        inline_rules.append((
            r'(donn\u00e9es INSEE|INSEE)',
            r'<a href="https://www.insee.fr/fr/statistiques/serie/001567616" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700">\1</a>',
            'insee.fr'
        ))

    # Apply rules (only first match per rule to avoid over-linking)
    for pattern, replacement, check_str in inline_rules:
        if check_str in html:
            continue  # Already has this link
        html = re.sub(pattern, replacement, html, count=1)

    return html


def patch_file(filepath, page_slug):
    """Patch a single HTML file with E-E-A-T improvements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Add byline + dates under h1
    html = add_byline_under_h1(html)

    # 2. Add inline source links (only for article pages)
    if page_slug in PAGE_SOURCES:
        html = add_inline_source_links(html, page_slug)

    # 3. Add sources box before FAQ
    sources = PAGE_SOURCES.get(page_slug, [])
    if sources:
        html = add_sources_box(html, sources)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    modified_count = 0
    skipped_count = 0

    for page_slug in ALL_PAGES:
        if page_slug in SKIP_DIRS:
            print(f"  SKIP: {page_slug}/")
            skipped_count += 1
            continue

        filepath = os.path.join(BASE_DIR, page_slug, 'index.html')
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filepath}")
            continue

        if patch_file(filepath, page_slug):
            print(f"  PATCHED: {page_slug}/index.html")
            modified_count += 1
        else:
            print(f"  NO CHANGE: {page_slug}/index.html")

    print(f"\nDone! {modified_count} files modified, {skipped_count} skipped.")


if __name__ == '__main__':
    main()
