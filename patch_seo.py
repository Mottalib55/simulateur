#!/usr/bin/env python3
"""
patch_seo.py — SEO V6 improvements for salairebrutonet.com
Adds: og:image:alt, Twitter Card, font preload, Article schéma
Skips: prime-brut-en-net/
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pages that should NOT be touched
SKIP_DIRS = ['prime-brut-en-net']

# Pages that get Article schéma (educational/guide content only)
ARTICLE_PAGES = [
    'salaire-brut-net-cadre',
    'salaire-brut-net-non-cadre',
    'salaire-brut-net-fonction-publique',
    'salaire-brut-net-auto-entrepreneur',
    'salaire-brut-net-alternance-apprentissage',
    'salaire-brut-net-interim',
    'salaire-brut-net-stage',
    'salaire-brut-net-mensuel',
    'salaire-brut-net-annuel',
    'salaire-brut-net-horaire',
    'salaire-brut-net-journalier',
    'taux-horaire-brut-net',
    'différence-salaire-brut-net',
    'cotisations-sociales-salariales',
    'salaire-net-imposable',
    'salaire-net-avant-après-impôt',
    'lire-fiche-de-paie',
    'salaire-moyen-france',
    'négocier-salaire',
    'coût-employeur',
    'cadre-vs-non-cadre',
    'salaire-brut-net-alsace-moselle',
    'smic-brut-net-2026',
    'salaire-brut-net-2026',
    '13eme-mois-brut-net',
    'heures-supplémentaires-brut-net',
    'avantages-en-nature',
]

# All guide/tool pages to patch (excluding prime-brut-en-net, admin, scripts, etc.)
ALL_PAGES = ARTICLE_PAGES + [
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


def extract_meta(html, name_or_prop, attr='content'):
    """Extract meta tag content by name or property."""
    # Try property first
    pattern = rf'<meta\s+(?:property|name)="{re.escape(name_or_prop)}"\s+content="([^"]*)"'
    m = re.search(pattern, html)
    if m:
        return m.group(1)
    # Try reversed order
    pattern = rf'<meta\s+content="([^"]*)"\s+(?:property|name)="{re.escape(name_or_prop)}"'
    m = re.search(pattern, html)
    if m:
        return m.group(1)
    return ''


def extract_title(html):
    """Extract <title> content."""
    m = re.search(r'<title>([^<]+)</title>', html)
    return m.group(1) if m else ''


def extract_canonical(html):
    """Extract canonical URL."""
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    return m.group(1) if m else ''


def add_og_image_alt(html, description):
    """Add og:image:alt after og:image:height if not already present."""
    if 'og:image:alt' in html:
        return html

    # Try inserting after og:image:height
    pattern = r'(<meta\s+property="og:image:height"\s+content="[^"]*">)'
    replacement = r'\1\n    <meta property="og:image:alt" content="' + description.replace('\\', '\\\\') + '">'
    new_html = re.sub(pattern, replacement, html, count=1)

    if new_html != html:
        return new_html

    # Fallback: insert after og:image if no width/height
    pattern = r'(<meta\s+property="og:image"\s+content="[^"]*">)'
    replacement = r'\1\n    <meta property="og:image:alt" content="' + description.replace('\\', '\\\\') + '">'
    return re.sub(pattern, replacement, html, count=1)


def add_twitter_card(html, title, description):
    """Add Twitter Card tags if not already present."""
    if 'twitter:card' in html:
        return html

    twitter_tags = f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://salairebrutonet.com/img/og-image.png">'''

    # Insert after og:image:alt if present
    if 'og:image:alt' in html:
        pattern = r'(<meta\s+property="og:image:alt"\s+content="[^"]*">)'
        return re.sub(pattern, r'\1' + twitter_tags, html, count=1)

    # Insert after og:image:height
    if 'og:image:height' in html:
        pattern = r'(<meta\s+property="og:image:height"\s+content="[^"]*">)'
        return re.sub(pattern, r'\1' + twitter_tags, html, count=1)

    # Insert after og:image
    if 'og:image' in html:
        pattern = r'(<meta\s+property="og:image"\s+content="[^"]*">)'
        return re.sub(pattern, r'\1' + twitter_tags, html, count=1)

    return html


def add_font_preload(html):
    """Add font preload link before fonts.css if not already present."""
    if 'rel="preload"' in html and 'inter-latin.woff2' in html:
        return html

    pattern = r'(<link\s+rel="stylesheet"\s+href="/css/fonts\.css">)'
    replacement = '<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>\n    \\1'
    return re.sub(pattern, replacement, html, count=1)


def add_article_schema(html, title, description, canonical_url):
    """Add Article schéma JSON-LD after the last existing </script> JSON-LD block."""
    if '"@type": "Article"' in html or '"@type":"Article"' in html:
        return html

    schéma = {
        "@context": "https://schéma.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": canonical_url,
        "datePublished": "2026-01-15",
        "dateModified": "2026-06-20",
        "inLanguage": "fr",
        "author": {
            "@type": "Person",
            "name": "Mottalib Radif",
            "url": "https://salairebrutonet.com/a-propos/",
            "image": "https://salairebrutonet.com/team/mottalib-radif.jpg"
        },
        "publisher": {
            "@type": "Organization",
            "name": "SalaireBrutNet",
            "logo": {
                "@type": "ImageObject",
                "url": "https://salairebrutonet.com/img/logo.svg"
            }
        }
    }

    schema_json = json.dumps(schéma, indent=4, ensure_ascii=False)
    script_block = f'''    <script type="application/ld+json">
    {schema_json}
    </script>'''

    # Find the last </script> that closes a JSON-LD block (before </head> or before other content)
    # We look for the last occurrence of </script> followed by potential whitespace before </head> or <link or <script without ld+json
    # Strategy: find all JSON-LD script blocks and insert after the last one
    json_ld_pattern = r'(</script>\s*?)(?=\s*(?:<script type="text/javascript">|<!-- Microsoft Clarity|<link|</head>|\s*$))'

    # Find all positions of </script> that end JSON-LD blocks
    matches = list(re.finditer(r'</script>', html))
    if not matches:
        return html

    # Find JSON-LD blocks
    ld_blocks = list(re.finditer(r'<script type="application/ld\+json">[\s\S]*?</script>', html))
    if not ld_blocks:
        return html

    last_ld_end = ld_blocks[-1].end()
    # Insert the new schéma after the last JSON-LD block
    html = html[:last_ld_end] + '\n' + script_block + html[last_ld_end:]

    return html


def patch_file(filepath, page_slug):
    """Patch a single HTML file with SEO improvements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    title = extract_title(html)
    description = extract_meta(html, 'description')
    canonical_url = extract_canonical(html)

    # 1. Add og:image:alt
    html = add_og_image_alt(html, description)

    # 2. Add Twitter Card
    html = add_twitter_card(html, title, description)

    # 3. Add font preload
    html = add_font_preload(html)

    # 4. Add Article schéma (only for guide pages)
    if page_slug in ARTICLE_PAGES:
        html = add_article_schema(html, title, description, canonical_url)

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

    # Also patch 404.html
    filepath_404 = os.path.join(BASE_DIR, '404.html')
    if os.path.exists(filepath_404):
        with open(filepath_404, 'r', encoding='utf-8') as f:
            html = f.read()

        original = html
        description = extract_meta(html, 'description')

        # 404 has no og tags currently, so we need to add og:image block first
        if 'og:image' not in html:
            # Add OG tags after the description meta
            og_block = '''
    <meta property="og:type" content="website">
    <meta property="og:title" content="Page introuvable (404) | SalaireBrutNet">
    <meta property="og:description" content="''' + description + '''">
    <meta property="og:locale" content="fr_FR">
    <meta property="og:site_name" content="SalaireBrutNet">
    <meta property="og:image" content="https://salairebrutonet.com/img/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="''' + description + '''">'''
            # Insert after robots meta
            html = html.replace(
                '<meta name="robots" content="noindex, follow">',
                '<meta name="robots" content="noindex, follow">' + og_block
            )
        else:
            html = add_og_image_alt(html, description)

        if html != original:
            with open(filepath_404, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  PATCHED: 404.html")
            modified_count += 1
        else:
            print(f"  NO CHANGE: 404.html")

    print(f"\nDone! {modified_count} files modified, {skipped_count} skipped.")


if __name__ == '__main__':
    main()
