#!/usr/bin/env python3
"""
Génère les pages Phase 2 : statuts professionnels, périodes, contenu éducatif, outils.
Usage : python generate-pages.py
"""

import os
from datetime import date
from calcul import calculer_brut_vers_net, calculer_net_vers_brut, fmt, fmt2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://salairebrutonet.com"
TODAY = date.today().isoformat()

# ── Template HTML commun ──────────────────────────────────────────────────────

def page_head(title, description, canonical, keywords=""):
    return f'''<!DOCTYPE html>
<html lang="fr" class="scroll-smooth"><head>
    <meta name="msvalidate.01" content="15b1d26333aa4cd7a1cdba8e813bfc7f" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/img/logo.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
    <link rel="apple-touch-icon" sizes="192x192" href="/img/favicon-192.png">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:locale" content="fr_FR">
    <meta property="og:site_name" content="SalaireBrutNet">
    <meta property="og:image" content="https://salairebrutonet.com/img/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Mottalib Radif">
    <meta name="keywords" content="{keywords}">
    <link rel="manifest" href="/manifest.webmanifest">
    <link rel="stylesheet" href="/css/fonts.css">
    <link rel="stylesheet" href="/css/style.css">
    <script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","xanyylalio");</script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Calculateur Salaire Brut Net", "item": "{BASE_URL}/" }},
            {{ "@type": "ListItem", "position": 2, "name": "{title.split(' | ')[0].split(' - ')[0]}", "item": "{canonical}" }}
        ]
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "SalaireBrutNet",
        "url": "https://salairebrutonet.com",
        "logo": "https://salairebrutonet.com/img/logo.svg",
        "description": "Simulateur gratuit de conversion salaire brut en net pour la France. Taux 2026 à jour, cadre et non-cadre.",
        "founder": {{
            "@type": "Person",
            "name": "Mottalib Radif",
            "url": "https://salairebrutonet.com/a-propos/",
            "image": "https://salairebrutonet.com/team/mottalib-radif.jpg",
            "jobTitle": "Fondateur"
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Mottalib Radif",
        "url": "https://salairebrutonet.com/a-propos/",
        "image": "https://salairebrutonet.com/team/mottalib-radif.jpg",
        "jobTitle": "Fondateur de SalaireBrutNet",
        "worksFor": {{
            "@type": "Organization",
            "name": "SalaireBrutNet",
            "url": "https://salairebrutonet.com"
        }},
        "knowsAbout": ["salaire brut net", "cotisations sociales", "fiscalité française", "droit du travail"]
    }}
    </script>
</head>'''


HEADER = '''
<body class="bg-slate-50 text-slate-600 antialiased selection:bg-brand-100 selection:text-brand-900 flex flex-col min-h-screen">
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-brand-600 focus:text-white focus:rounded-lg focus:text-sm focus:font-semibold">Aller au contenu</a>
    <header class="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/90 backdrop-blur-md">
        <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
            <a href="/" class="flex items-center gap-2">
                <img src="/img/logo.svg" alt="SalaireBrutNet" class="h-8 w-8">
                <span class="text-base font-semibold tracking-tight text-slate-900">SalaireBrutNet</span>
            </a>
            <nav class="hidden md:flex gap-8 items-center">
                <a href="/" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Calcul Brut Net</a>
                <div class="relative nav-guides">
                    <button id="btn-guides-desktop" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors inline-flex items-center gap-1">Guides <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></button>
                    <div class="mega-menu"><div class="mega-menu-grid">
                        <div class="mega-menu-col"><h3>Par statut</h3><a href="/salaire-brut-net-cadre/">Cadre</a><a href="/salaire-brut-net-non-cadre/">Non-cadre</a><a href="/salaire-brut-net-fonction-publique/">Fonction publique</a><a href="/salaire-brut-net-auto-entrepreneur/">Auto-entrepreneur</a><a href="/salaire-brut-net-alternance-apprentissage/">Alternance</a><a href="/salaire-brut-net-interim/">Intérim</a><a href="/salaire-brut-net-stage/">Stage</a></div>
                        <div class="mega-menu-col"><h3>Par période</h3><a href="/salaire-brut-net-mensuel/">Mensuel</a><a href="/salaire-brut-net-annuel/">Annuel</a><a href="/salaire-brut-net-horaire/">Horaire</a><a href="/salaire-brut-net-journalier/">Journalier</a><a href="/taux-horaire-brut-net/">Taux horaire</a></div>
                        <div class="mega-menu-col"><h3>Comprendre</h3><a href="/difference-salaire-brut-net/">Différence brut/net</a><a href="/cotisations-sociales-salariales/">Cotisations sociales</a><a href="/salaire-net-imposable/">Net imposable</a><a href="/salaire-net-avant-apres-impot/">Net avant/après impôt</a><a href="/lire-fiche-de-paie/">Lire sa fiche de paie</a></div>
                        <div class="mega-menu-col"><h3>Outils</h3><a href="/cout-employeur/">Coût employeur</a><a href="/calculateur-cout-employeur/">Calculateur coût employeur</a><a href="/calculateur-heures-supplementaires/">Calculateur heures sup</a><a href="/comparateur-salaire-net-par-pays/">Comparateur pays</a><a href="/simulateur-impot-sur-le-revenu/">Simulateur impôts</a></div>
                        <div class="mega-menu-col"><h3>Composantes</h3><a href="/prime-brut-en-net/">Prime brut en net</a><a href="/13eme-mois-brut-net/">13ème mois</a><a href="/heures-supplementaires-brut-net/">Heures sup</a><a href="/avantages-en-nature/">Avantages en nature</a><a href="/smic-brut-net-2026/">SMIC 2026</a><a href="/salaire-moyen-france/">Salaire moyen France</a><a href="/negocier-salaire/">Négocier son salaire</a></div>
                    </div></div>
                </div>
                <a href="/simulateur-impot-sur-le-revenu/" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Simulateur Impôts</a>
                <a href="/mission/" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Notre Mission</a>
            </nav>
            <div class="flex items-center gap-3">
                <button id="btn-share" class="hidden sm:inline-flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-slate-800 transition-colors">
                    <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                    Partager
                </button>
                <button id="btn-hamburger" class="md:hidden inline-flex items-center justify-center w-10 h-10 rounded-lg hover:bg-slate-100 transition-colors" aria-label="Menu">
                    <svg id="hamburger-icon" class="h-6 w-6 text-slate-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
                    <svg id="close-icon" class="h-6 w-6 text-slate-700 hidden" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
            </div>
        </div>
        <div id="mobile-nav" class="mobile-nav">
            <div class="mobile-nav-main"><a href="/">Calcul Brut Net</a><a href="/simulateur-impot-sur-le-revenu/">Simulateur Impôts</a><a href="/mission/">Notre Mission</a></div>
            <div class="mobile-nav-section"><h3>Par statut</h3><div class="mobile-nav-links"><a href="/salaire-brut-net-cadre/">Cadre</a><a href="/salaire-brut-net-non-cadre/">Non-cadre</a><a href="/salaire-brut-net-fonction-publique/">Fonction publique</a><a href="/salaire-brut-net-auto-entrepreneur/">Auto-entrepreneur</a><a href="/salaire-brut-net-alternance-apprentissage/">Alternance</a><a href="/salaire-brut-net-interim/">Intérim</a><a href="/salaire-brut-net-stage/">Stage</a></div></div>
            <div class="mobile-nav-section"><h3>Par période</h3><div class="mobile-nav-links"><a href="/salaire-brut-net-mensuel/">Mensuel</a><a href="/salaire-brut-net-annuel/">Annuel</a><a href="/salaire-brut-net-horaire/">Horaire</a><a href="/salaire-brut-net-journalier/">Journalier</a><a href="/taux-horaire-brut-net/">Taux horaire</a></div></div>
            <div class="mobile-nav-section"><h3>Comprendre</h3><div class="mobile-nav-links"><a href="/difference-salaire-brut-net/">Différence brut/net</a><a href="/cotisations-sociales-salariales/">Cotisations sociales</a><a href="/salaire-net-imposable/">Net imposable</a><a href="/salaire-net-avant-apres-impot/">Net avant/après impôt</a><a href="/lire-fiche-de-paie/">Lire sa fiche de paie</a></div></div>
            <div class="mobile-nav-section"><h3>Outils</h3><div class="mobile-nav-links"><a href="/cout-employeur/">Coût employeur</a><a href="/calculateur-cout-employeur/">Calculateur coût employeur</a><a href="/calculateur-heures-supplementaires/">Calculateur heures sup</a><a href="/comparateur-salaire-net-par-pays/">Comparateur pays</a><a href="/simulateur-impot-sur-le-revenu/">Simulateur impôts</a></div></div>
            <div class="mobile-nav-section"><h3>Composantes</h3><div class="mobile-nav-links"><a href="/prime-brut-en-net/">Prime brut en net</a><a href="/13eme-mois-brut-net/">13ème mois</a><a href="/heures-supplementaires-brut-net/">Heures sup</a><a href="/avantages-en-nature/">Avantages en nature</a><a href="/smic-brut-net-2026/">SMIC 2026</a><a href="/salaire-moyen-france/">Salaire moyen France</a><a href="/negocier-salaire/">Négocier son salaire</a></div></div>
        </div>
    </header>
    <main id="main-content" class="flex-grow" role="main">
'''

FOOTER = '''
    </main>
    <footer class="bg-white border-t border-slate-200 py-10">
        <div class="mx-auto max-w-7xl px-4 flex flex-col md:flex-row justify-between items-center gap-6">
            <a href="/" class="flex items-center gap-2">
                <img src="/img/logo.svg" alt="SalaireBrutNet" class="h-6 w-6">
                <span class="text-sm font-semibold text-slate-900">SalaireBrutNet</span>
            </a>
            <p class="text-xs text-slate-500">© 2026 SalaireBrutNet · Estimation indicative</p>
            <div class="flex flex-wrap gap-4 justify-center">
                <a href="/" class="text-xs text-slate-500 hover:text-slate-900">Calcul Brut Net</a>
                <a href="/mentions-legales/" class="text-xs text-slate-500 hover:text-slate-900">Mentions légales</a>
                <a href="/a-propos/" class="text-xs text-slate-500 hover:text-slate-900">À propos</a>
                <a href="/mission/" class="text-xs text-slate-500 hover:text-slate-900">Notre Mission</a>
                <a href="/glossaire/" class="text-xs text-slate-500 hover:text-slate-900">Glossaire</a>
                <a href="/simulateur-impot-sur-le-revenu/" class="text-xs text-slate-500 hover:text-slate-900">Simulateur Impôts</a>
                <a href="/salaire-brut-net-cadre/" class="text-xs text-slate-500 hover:text-slate-900">Guides</a>
            </div>
        </div>
    </footer>
    <script>
    (function(){
        var hb=document.getElementById('btn-hamburger'),mn=document.getElementById('mobile-nav'),hi=document.getElementById('hamburger-icon'),ci=document.getElementById('close-icon');
        if(hb){hb.addEventListener('click',function(){var o=mn.classList.toggle('open');hi.classList.toggle('hidden',o);ci.classList.toggle('hidden',!o)});}
        if(mn){mn.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');hi.classList.remove('hidden');ci.classList.add('hidden')})});}
        var ng=document.querySelector('.nav-guides'),mm=document.querySelector('.mega-menu'),t;
        if(ng&&mm){function show(){clearTimeout(t);mm.classList.add('open')}function hide(){t=setTimeout(function(){mm.classList.remove('open')},250)}ng.addEventListener('mouseenter',show);ng.addEventListener('mouseleave',hide);mm.addEventListener('mouseenter',show);mm.addEventListener('mouseleave',hide);}
    })();
    </script>
'''


def breadcrumb(label):
    return f'''
        <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
            <ol class="flex items-center gap-2 text-sm text-slate-500">
                <li><a href="/" class="hover:text-brand-600 transition-colors">Accueil</a></li>
                <li><svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></li>
                <li class="text-slate-900 font-medium">{label}</li>
            </ol>
        </nav>'''


def calculator_widget(default_val=2500, statut_default="non-cadre", mode="brut"):
    """Inline calculator widget reusable across pages."""
    if mode == "brut":
        label_input = "Salaire brut mensuel"
        label_result = "Salaire net mensuel"
        result_id = "result-net-widget"
        calc_fn = "calculerBrutVersNet"
        result_field = "netAvantImpot"
    else:
        label_input = "Salaire net mensuel"
        label_result = "Salaire brut mensuel"
        result_id = "result-brut-widget"
        calc_fn = "calculerNetVersBrut"
        result_field = "brutMensuel"

    cadre_selected = 'selected' if statut_default == 'cadre' else ''
    nc_selected = 'selected' if statut_default == 'non-cadre' else ''

    return f'''
        <section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur rapide</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">{label_input}</label>
                            <input type="text" inputmode="decimal" id="widget-input" value="{default_val}"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" {nc_selected}>Non-cadre</option>
                                <option value="cadre" {cadre_selected}>Cadre</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Temps de travail</label>
                            <select id="widget-temps" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="100" selected>100%</option>
                                <option value="80">80%</option>
                                <option value="60">60%</option>
                                <option value="50">50%</option>
                            </select>
                        </div>
                    </div>
                    <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                        <p class="text-sm text-brand-600 font-medium">{label_result}</p>
                        <p class="text-3xl font-bold text-slate-900" id="{result_id}">–</p>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {{
        const inp = document.getElementById('widget-input');
        const sel = document.getElementById('widget-statut');
        const tmp = document.getElementById('widget-temps');
        const res = document.getElementById('{result_id}');
        function calc() {{
            const v = parseFloat(inp.value) || 0;
            const r = {calc_fn}(v, sel.value, parseInt(tmp.value)/100);
            res.textContent = formatMoney(r.{result_field});
        }}
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        tmp.addEventListener('change', calc);
        calc();
    }})();
    </script>'''


def links_grid(title, links):
    """Build a grid of internal links."""
    items = ""
    for url, label in links:
        items += f'''<a href="{url}" class="block rounded-xl border border-slate-200 bg-white p-3 text-center hover:border-brand-300 hover:shadow-sm transition-all">
            <span class="block text-sm font-medium text-slate-900">{label}</span>
        </a>\n'''
    return f'''
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl">
                <h2 class="text-lg font-bold text-slate-900 mb-4">{title}</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                    {items}
                </div>
            </div>
        </section>'''


RELATED_LINKS = [
    ("/salaire-brut-net-cadre/", "Cadre"),
    ("/salaire-brut-net-non-cadre/", "Non-cadre"),
    ("/salaire-brut-net-fonction-publique/", "Fonction publique"),
    ("/salaire-brut-net-auto-entrepreneur/", "Auto-entrepreneur"),
    ("/salaire-brut-net-alternance-apprentissage/", "Alternance"),
    ("/salaire-brut-net-interim/", "Intérim"),
    ("/salaire-brut-net-stage/", "Stage"),
    ("/salaire-brut-net-mensuel/", "Mensuel"),
    ("/salaire-brut-net-annuel/", "Annuel"),
    ("/salaire-brut-net-horaire/", "Horaire"),
    ("/salaire-brut-net-journalier/", "Journalier"),
    ("/taux-horaire-brut-net/", "Taux horaire"),
    ("/difference-salaire-brut-net/", "Différence brut/net"),
    ("/cotisations-sociales-salariales/", "Cotisations sociales"),
    ("/salaire-net-imposable/", "Net imposable"),
    ("/salaire-net-avant-apres-impot/", "Net avant/après impôt"),
    ("/lire-fiche-de-paie/", "Lire sa fiche de paie"),
    ("/cout-employeur/", "Coût employeur"),
    ("/calculateur-cout-employeur/", "Calculateur coût employeur"),
    ("/calculateur-heures-supplementaires/", "Calculateur heures sup"),
    ("/comparateur-salaire-net-par-pays/", "Comparateur pays"),
    ("/simulateur-impot-sur-le-revenu/", "Simulateur impôts"),
    ("/prime-brut-en-net/", "Prime brut en net"),
    ("/13eme-mois-brut-net/", "13ème mois"),
    ("/heures-supplementaires-brut-net/", "Heures sup"),
    ("/avantages-en-nature/", "Avantages en nature"),
    ("/smic-brut-net-2026/", "SMIC 2026"),
    ("/salaire-moyen-france/", "Salaire moyen France"),
    ("/negocier-salaire/", "Négocier son salaire"),
]


def write_page(slug, html_content):
    """Write page to slug/index.html"""
    folder = os.path.join(BASE_DIR, slug)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  ✓ {slug}/index.html")


def generate_conversion_table(amounts, statut="non-cadre"):
    """Generate an HTML conversion table for given brut amounts."""
    rows = ""
    for brut in amounts:
        r = calculer_brut_vers_net(brut, statut)
        rows += f'''<tr class="border-b border-slate-100">
            <td class="py-2 font-medium">{fmt(brut)} €</td>
            <td class="py-2 text-right">{fmt(r['net_avant_impot'])} €</td>
            <td class="py-2 text-right">{fmt(round(r['net_avant_impot'] * 12))} €</td>
            <td class="py-2 text-right">{fmt(r['cout_employeur'])} €</td>
        </tr>'''
    return f'''
    <div class="overflow-x-auto">
        <table class="w-full text-sm">
            <thead><tr class="border-b-2 border-slate-300">
                <th class="py-2 text-left font-semibold">Brut mensuel</th>
                <th class="py-2 text-right font-semibold">Net mensuel</th>
                <th class="py-2 text-right font-semibold">Net annuel</th>
                <th class="py-2 text-right font-semibold">Coût employeur</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>'''


def generate_faq_section(faqs):
    """Generate FAQ accordion with schema.org markup."""
    chevron_svg = '<svg class="h-5 w-5 text-slate-400 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>'
    items_html = ""
    schema_items = []
    for i, faq in enumerate(faqs):
        q_escaped = faq["q"].replace('"', '\\"')
        a_escaped = faq["a"].replace('"', '\\"')
        items_html += f'''
            <div class="rounded-xl border border-slate-200 bg-white">
                <button class="faq-toggle w-full flex items-center justify-between p-5 text-left" onclick="this.nextElementSibling.classList.toggle('hidden');this.querySelector('svg').style.transform=this.nextElementSibling.classList.contains('hidden')?'':'rotate(180deg)'">
                    <span class="font-medium text-slate-900">{faq["q"]}</span>
                    {chevron_svg}
                </button>
                <div class="faq-content hidden px-5 pb-5">
                    <p class="text-sm text-slate-600">{faq["a"]}</p>
                </div>
            </div>'''
        schema_items.append(f'{{"@type":"Question","name":"{q_escaped}","acceptedAnswer":{{"@type":"Answer","text":"{a_escaped}"}}}}')

    schema_json = ','.join(schema_items)
    return f'''
        <section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6">Questions fréquentes</h2>
                <div class="space-y-3">
                    {items_html}
                </div>
            </div>
        </section>
        <script type="application/ld+json">
        {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{schema_json}]}}
        </script>'''


def generate_examples(scenarios):
    """Generate concrète example cards."""
    cards = ""
    for s in scenarios:
        cards += f'''
            <div class="rounded-xl border border-slate-200 bg-white p-5">
                <p class="font-semibold text-slate-900 mb-2">{s["name"]}</p>
                <p class="text-sm text-slate-500 mb-3">{s["situation"]}</p>
                <div class="space-y-1 text-sm">
                    <div class="flex justify-between"><span class="text-slate-600">Brut mensuel</span><span class="font-medium">{s["brut"]}</span></div>
                    <div class="flex justify-between"><span class="text-slate-600">Net mensuel</span><span class="font-bold text-brand-600">{s["net"]}</span></div>
                    <div class="flex justify-between"><span class="text-slate-600">Net après impôt</span><span class="font-medium text-emerald-600">{s["net_apres_impot"]}</span></div>
                </div>
            </div>'''
    return f'''
        <h3 class="text-lg font-semibold text-slate-900 mt-8 mb-4">Exemples concrets</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            {cards}
        </div>'''



# ── 1. Pages par statut professionnel ──────────────────────────────────────────

def gen_status_pages():
    pages = [
        {
            "slug": "salaire-brut-net-cadre",
            "title": "Salaire Brut Net Cadre 2026 : Calcul et Cotisations",
            "desc": "Calculez votre salaire brut en net cadre. Cotisations spécifiques CET et AGIRC-ARRCO, taux détaillés avec simulateur gratuit. Résultat instantané 2026.",
            "kw": "salaire brut net cadre, brut en net cadre, cotisations cadre, calcul salaire cadre",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Cadre</span> 2026",
            "statut_default": "cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Spécificités du statut cadre</h2>
                <p>En tant que <strong>cadre</strong>, vos cotisations salariales sont légèrement plus élevées qu'un non-cadre. La principale différence réside dans la <strong>CET (Contribution d'Équilibre Technique)</strong> de 0,14% prélevée sur la totalité de votre salaire brut.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cotisations salariales cadre 2026</h3>
                <p>Voici le détail des cotisations prélevées sur votre salaire brut :</p>
                <ul class="space-y-1">
                    <li><strong>Vieillesse plafonnée</strong> : 6,90% (sur la tranche 1, jusqu'à 3 864 €/mois)</li>
                    <li><strong>Vieillesse déplafonnée</strong> : 0,40% (sur la totalité du brut)</li>
                    <li><strong>AGIRC-ARRCO Tranche 1</strong> : 3,15% (jusqu'au plafond SS)</li>
                    <li><strong>AGIRC-ARRCO Tranche 2</strong> : 8,64% (au-delà du plafond SS)</li>
                    <li><strong>CEG T1</strong> : 0,86% | <strong>CEG T2</strong> : 1,08%</li>
                    <li><strong>CET</strong> : 0,14% (spécifique cadre, sur la totalité)</li>
                    <li><strong>CSG déductible</strong> : 6,80% | <strong>CSG non déductible</strong> : 2,40% | <strong>CRDS</strong> : 0,50% (sur 98,25% du brut)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Différence cadre vs non-cadre</h3>
                <p>Pour un même salaire brut, un <strong>cadre touche environ 3% de moins en net</strong> qu'un non-cadre, principalement à cause de la CET. Par exemple, pour 3 000 € brut mensuel :</p>
                <ul>
                    <li>Non-cadre : environ 2 340 € net</li>
                    <li>Cadre : environ 2 336 € net</li>
                </ul>
                <p>La différence est faible sur les salaires inférieurs au plafond de la Sécurité sociale. Elle augmente pour les hauts salaires en raison des cotisations sur la tranche 2.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages du statut cadre</h3>
                <p>Malgré des cotisations légèrement plus élevées, le statut cadre offre des avantages :</p>
                <ul>
                    <li><strong>Retraite complémentaire plus élevée</strong> grâce aux cotisations AGIRC-ARRCO majorées</li>
                    <li><strong>Prévoyance obligatoire</strong> (couverture décès, invalidité)</li>
                    <li><strong>Période d'essai plus longue</strong> (jusqu'à 4 mois renouvelable)</li>
                    <li><strong>Préavis de démission/licenciement allongé</strong> (3 mois en général)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Convention collective et classification cadre</h2>
                <p>Le <strong>statut cadre</strong> n'est pas défini par la loi mais par les <a href="/difference-salaire-brut-net/" class="text-brand-600 hover:text-brand-700">conventions collectives</a>. Chaque branche professionnelle établit ses propres critères pour déterminer qui peut être considéré comme cadre. En général, le statut cadre est accordé aux salariés exerçant des fonctions d'encadrement, de conception ou de responsabilité.</p>
                <p>Les principaux critères incluent : le niveau de responsabilité, l'autonomie dans l'organisation du travail, la participation aux décisions stratégiques, et souvent un niveau de diplôme minimum (Bac+3 ou Bac+5). Certaines conventions collectives prévoient des positions intermédiaires comme "agent de maîtrise" ou "technicien supérieur" qui peuvent évoluer vers le statut cadre.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Historique : AGIRC et ARRCO avant la fusion de 2019</h3>
                <p>Jusqu'en 2019, le système de retraite complémentaire français distinguait clairement cadres et non-cadres avec deux organismes séparés :</p>
                <ul>
                    <li><strong>ARRCO</strong> (Association pour le Régime de Retraite Complémentaire des salariés) : couvrait tous les salariés du privé, cadres et non-cadres, pour la tranche 1 (jusqu'au plafond de la Sécurité sociale)</li>
                    <li><strong>AGIRC</strong> (Association Générale des Institutions de Retraite des Cadres) : couvrait exclusivement les cadres pour les tranches de salaire au-delà du plafond SS</li>
                </ul>
                <p>Depuis le <strong>1er janvier 2019</strong>, l'AGIRC et l'ARRCO ont fusionné en un régime unique : <strong>AGIRC-ARRCO</strong>. Cette fusion a simplifié le système tout en maintenant certaines spécificités pour les cadres, notamment la cotisation sur la tranche 2 (au-delà du plafond SS) et la contribution d'équilibre technique (CET).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact sur la retraite complémentaire : les points AGIRC-ARRCO</h2>
                <p>Les cotisations de retraite complémentaire des cadres permettent d'accumuler des <strong>points de retraite</strong> qui détermineront le montant de la pension à la retraite. Le système fonctionne ainsi :</p>
                <ul>
                    <li>Chaque euro cotisé permet d'acheter des points AGIRC-ARRCO</li>
                    <li>En 2026, le <strong>prix d'achat du point</strong> est de 18,7669 €</li>
                    <li>À la retraite, chaque point rapporte une <strong>valeur de service</strong> de 1,4159 € par an</li>
                </ul>
                <p>Pour un cadre, les cotisations sur la tranche 2 (au-delà de 3 864 €/mois) représentent un avantage important : le taux de cotisation de 8,64% (part salariale) permet d'accumuler davantage de points que sur la tranche 1. Par exemple, un cadre gagnant 5 000 € brut mensuel cotisé sur environ 1 136 € en tranche 2, ce qui génère environ 120 points par an supplémentaires par rapport à un non-cadre au plafond.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Prévoyance obligatoire cadre : la convention AGIRC</h3>
                <p>Les cadres bénéficient d'une <strong>prévoyance collective obligatoire</strong> financée par l'employeur (minimum 1,5% de la tranche A du salaire). Cette prévoyance couvre :</p>
                <ul>
                    <li><strong>Décès</strong> : versement d'un capital aux ayants droit (souvent 100% du salaire annuel brut)</li>
                    <li><strong>Invalidité</strong> : rente en cas d'incapacité permanente de travail</li>
                    <li><strong>Incapacité temporaire</strong> : maintien de salaire en complément des indemnités journalières de la Sécurité sociale</li>
                </ul>
                <p>Cette protection sociale renforcée est un avantage majeur du statut cadre, car elle offre une sécurité financière supérieure à celle des non-cadres. Certaines conventions collectives prévoient des garanties encore plus avantageuses, avec des taux de maintien de salaire pouvant atteindre 100% pendant plusieurs mois en cas d'arrêt maladie.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparaison détaillée cadre vs non-cadre pour différents niveaux de salaire</h2>
                <p>Voici une comparaison précise entre le salaire net d'un cadre et d'un non-cadre pour différents niveaux de rémunération en 2026 :</p>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Salaire Brut Mensuel</th>
                            <th class="border border-slate-300 px-4 py-2">Net Non-Cadre</th>
                            <th class="border border-slate-300 px-4 py-2">Net Cadre</th>
                            <th class="border border-slate-300 px-4 py-2">Différence</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2">2 000 €</td><td class="border border-slate-300 px-4 py-2">1 560 €</td><td class="border border-slate-300 px-4 py-2">1 557 €</td><td class="border border-slate-300 px-4 py-2">-3 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">3 000 €</td><td class="border border-slate-300 px-4 py-2">2 340 €</td><td class="border border-slate-300 px-4 py-2">2 336 €</td><td class="border border-slate-300 px-4 py-2">-4 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">4 000 €</td><td class="border border-slate-300 px-4 py-2">3 104 €</td><td class="border border-slate-300 px-4 py-2">3 074 €</td><td class="border border-slate-300 px-4 py-2">-30 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">5 000 €</td><td class="border border-slate-300 px-4 py-2">3 844 €</td><td class="border border-slate-300 px-4 py-2">3 828 €</td><td class="border border-slate-300 px-4 py-2">-16 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">7 000 €</td><td class="border border-slate-300 px-4 py-2">5 324 €</td><td class="border border-slate-300 px-4 py-2">5 306 €</td><td class="border border-slate-300 px-4 py-2">-18 €</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">On constate que la différence reste modérée même pour les hauts salaires. L'écart le plus important se situe autour de 4 000 € brut (juste au-dessus du plafond SS) où les cotisations tranche 2 pèsent davantage.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cas particulier : les cadres au forfait jours</h3>
                <p>De nombreux cadres sont soumis à une <strong>convention de forfait en jours</strong> plutôt qu'à un décompte horaire. Ce régime permet une grande autonomie dans l'organisation du travail mais implique certaines particularités :</p>
                <ul>
                    <li>Le nombre de jours travaillés est plafonné à <strong>218 jours par an</strong> (en l'absence d'accord plus favorable)</li>
                    <li>Pas d'heures supplémentaires : le salaire est fixe quelle que soit la durée réelle du travail</li>
                    <li>L'employeur doit assurer un suivi de la charge de travail et du respect des repos</li>
                    <li>Le cadre conserve le droit à 11 heures de repos consécutif et 35 heures de repos hebdomadaire</li>
                </ul>
                <p>Le forfait jours est réservé aux cadres qui disposent d'une autonomie dans l'organisation de leur emploi du temps et dont la nature des fonctions ne les conduit pas à suivre l'horaire collectif applicable au sein de l'entreprise. Attention : tous les cadres ne peuvent pas être au forfait jours. Les cadres dirigeants en sont exclus (ils n'ont aucune limite de durée du travail), tout comme les cadres intégrés (qui suivent l'horaire collectif).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pour optimiser votre rémunération en tant que cadre</h2>
                <p>En tant que cadre, plusieurs leviers permettent d'<strong>optimiser votre rémunération nette</strong> et de préparer votre avenir :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Plan d'Épargne Retraite (PER) d'entreprise</h3>
                <p>Le <strong>PER collectif</strong> permet de déduire les versements volontaires de votre revenu imposable, réduisant ainsi votre impôt sur le revenu. Les sommes versées (dans la limite de 10% du PASS) sont déductibles du revenu imposable. C'est particulièrement avantageux pour les cadres dans les tranches marginales d'imposition élevées (30%, 41% ou 45%).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Titres-restaurant et autres avantages en nature</h3>
                <p>Les <strong>titres-restaurant</strong> sont exonérés de cotisations sociales dans la limite de 7,18 € par titre (valeur 2026) et pour la part employeur comprise entre 50% et 60% de la valeur du titre. Pour un titre de 10 €, l'employeur peut contribuer à hauteur de 6 € en exonération de charges.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Intéressement et participation</h3>
                <p>Les primes d'<strong>intéressement</strong> et de <strong>participation</strong> sont exonérées de cotisations sociales (hors CSG/CRDS). Si elles sont placées sur un PEE (Plan d'Épargne Entreprise) ou un PER collectif, elles sont également exonérées d'impôt sur le revenu pendant 5 ans (ou jusqu'à la retraite pour le PER).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Négociation du package global</h3>
                <p>Lors d'une négociation salariale, pensez au <strong>package global</strong> : salaire de base, variable, primes, véhicule de fonction, stock-options ou BSPCE, mutuelle famille, prévoyance renforcée. Un véhicule de fonction, par exemple, représente un avantage en nature soumis à cotisations et impôt, mais peut être plus intéressant qu'une augmentation de salaire selon votre situation.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5. Statut de cadre dirigeant</h3>
                <p>Les <strong>cadres dirigeants</strong> (très minoritaires) ne sont pas soumis à la réglementation sur la durée du travail. Ils ne cotisent pas non plus à l'assurance chômage. Ce statut implique généralement une rémunération très élevée mais aussi une précarité accrue (pas d'indemnités Pôle emploi en cas de licenciement, sauf rupture conventionnelle ou accord spécifique).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Questions fréquentes sur le salaire brut net cadre</h2>
                <p><strong>Un cadre gagne-t-il forcément plus qu'un non-cadre ?</strong> Non, le statut cadre ne garantit pas un salaire minimum. Juridiquement, un cadre peut être payé au SMIC. En pratique, les cadres ont généralement des salaires supérieurs car leurs fonctions impliquent plus de responsabilités et de qualifications.</p>
                <p><strong>Peut-on perdre le statut cadre ?</strong> Oui, en cas de changement de fonctions (rétrogradation, mobilité interne), l'employeur peut proposer un passage au statut non-cadre. Cela nécessite l'accord du salarié car il s'agit d'une modification substantielle du contrat de travail.</p>
                <p><strong>Le statut cadre est-il compatible avec un temps partiel ?</strong> Oui, un cadre peut travailler à temps partiel. Le forfait jours peut également être aménagé en forfait jours réduit (par exemple 156 jours par an pour un 80%).</p>
                <p>Pour en savoir plus sur les différences entre <a href="/salaire-brut-net-non-cadre/" class="text-brand-600 hover:text-brand-700">salariés non-cadres</a> et cadres, ou pour mieux comprendre le détail des <a href="/cotisations-sociales-salariales/" class="text-brand-600 hover:text-brand-700">cotisations sociales</a>, consultez nos guides dédiés.</p>
            """
        },
        {
            "slug": "salaire-brut-net-non-cadre",
            "title": "Salaire Brut Net Non-Cadre 2026 : Calcul et Cotisations",
            "desc": "Calculez votre salaire brut en net non-cadre en 2026. Taux de cotisations salariales détaillés, charges sociales et simulateur gratuit avec résultat instantané.",
            "kw": "salaire brut net non cadre, brut en net non cadre, cotisations non cadre, employé",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Non-Cadre</span> 2026",
            "statut_default": "non-cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le statut non-cadre (employé / ouvrier)</h2>
                <p>Le statut <strong>non-cadre</strong> concerne la majorité des salariés en France. Les cotisations salariales représentent environ <strong>22% du salaire brut</strong>, ce qui signifie que pour 100 € brut, vous touchez environ 78 € net.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cotisations salariales non-cadre 2026</h3>
                <ul class="space-y-1">
                    <li><strong>Vieillesse plafonnée</strong> : 6,90% (tranche 1)</li>
                    <li><strong>Vieillesse déplafonnée</strong> : 0,40% (totalité)</li>
                    <li><strong>AGIRC-ARRCO T1</strong> : 3,15% | <strong>T2</strong> : 8,64%</li>
                    <li><strong>CEG T1</strong> : 0,86% | <strong>CEG T2</strong> : 1,08%</li>
                    <li><strong>CSG + CRDS</strong> : 9,70% (sur 98,25% du brut)</li>
                </ul>
                <p>Contrairement aux cadres, les non-cadres ne paient pas la cotisation CET (0,14%), ce qui leur laisse un net légèrement supérieur.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de conversion non-cadre</h3>
                <ul>
                    <li><a href="/1500-euros-brut-en-net/" class="text-brand-600 hover:text-brand-700">1 500 € brut</a> → environ 1 170 € net</li>
                    <li><a href="/2000-euros-brut-en-net/" class="text-brand-600 hover:text-brand-700">2 000 € brut</a> → environ 1 560 € net</li>
                    <li><a href="/2500-euros-brut-en-net/" class="text-brand-600 hover:text-brand-700">2 500 € brut</a> → environ 1 950 € net</li>
                    <li><a href="/3000-euros-brut-en-net/" class="text-brand-600 hover:text-brand-700">3 000 € brut</a> → environ 2 340 € net</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Qui est concerné par le statut non-cadre ?</h2>
                <p>Le statut <strong>non-cadre</strong> regroupe la majorité des salariés du secteur privé en France. Selon l'INSEE, environ 82% des salariés français ont un statut non-cadre. Cette catégorie englobe de nombreux profils professionnels très diversifiés.</p>
                <p>Sont considérés comme non-cadres tous les salariés qui n'ont pas de fonctions d'encadrement, de conception ou de direction. Cela inclut les employés administratifs, les ouvriers, les techniciens, les agents de maîtrise, les vendeurs, les assistants, etc. Le statut non-cadre n'est pas lié au niveau de salaire : un technicien hautement qualifié peut gagner plus qu'un jeune cadre débutant tout en restant non-cadre.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Les différentes catégories de non-cadres</h3>
                <p>Au sein du statut non-cadre, on distingue traditionnellement plusieurs catégories socioprofessionnelles :</p>
                <ul>
                    <li><strong>Employés</strong> : travail principalement administratif, commercial ou de service (secrétaires, assistants, vendeurs, hôtes d'accueil, agents de service)</li>
                    <li><strong>Ouvriers</strong> : travail manuel dans l'industrie, le bâtiment ou l'artisanat (opérateurs de production, mécaniciens, électriciens, maçons, chauffeurs)</li>
                    <li><strong>Techniciens</strong> : qualification technique spécialisée sans fonction d'encadrement (techniciens de maintenance, informaticiens, dessinateurs, laborantins)</li>
                    <li><strong>Agents de maîtrise</strong> : position intermédiaire entre employés/ouvriers et cadres, souvent avec une petite équipe à superviser (chefs d'équipe, contremaîtrès, responsables de secteur)</li>
                </ul>
                <p>Depuis la fusion AGIRC-ARRCO en 2019, ces distinctions n'ont plus d'impact sur les <a href="/cotisations-sociales-salariales/" class="text-brand-600 hover:text-brand-700">cotisations sociales</a>. Tous les non-cadres cotisent aux mêmes taux, quelle que soit leur catégorie.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Détail des cotisations non-cadre : calcul étape par étape</h2>
                <p>Comprendre le passage du brut au net nécessite de détailler chaque cotisation. Voici un <strong>exemple concret</strong> pour un salaire de <strong>2 500 € brut mensuel</strong> en 2026 :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 1 : Cotisations de Sécurité sociale</h3>
                <ul>
                    <li><strong>Assurance vieillesse plafonnée (6,90%)</strong> : 2 500 × 6,90% = 172,50 € (car sous le plafond de 3 864 €)</li>
                    <li><strong>Assurance vieillesse déplafonnée (0,40%)</strong> : 2 500 × 0,40% = 10,00 €</li>
                </ul>
                <p>Total Sécurité sociale : <strong>182,50 €</strong></p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 2 : Retraite complémentaire AGIRC-ARRCO</h3>
                <ul>
                    <li><strong>Tranche 1 (3,15%)</strong> : 2 500 × 3,15% = 78,75 €</li>
                    <li><strong>Tranche 2 (8,64%)</strong> : 0 € (salaire sous le plafond SS)</li>
                    <li><strong>CEG Tranche 1 (0,86%)</strong> : 2 500 × 0,86% = 21,50 €</li>
                </ul>
                <p>Total retraite complémentaire : <strong>100,25 €</strong></p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 3 : CSG et CRDS (sur 98,25% du brut)</h3>
                <p>Assiette CSG/CRDS : 2 500 × 98,25% = 2 456,25 €</p>
                <ul>
                    <li><strong>CSG déductible (6,80%)</strong> : 2 456,25 × 6,80% = 167,03 €</li>
                    <li><strong>CSG non déductible (2,40%)</strong> : 2 456,25 × 2,40% = 58,95 €</li>
                    <li><strong>CRDS (0,50%)</strong> : 2 456,25 × 0,50% = 12,28 €</li>
                </ul>
                <p>Total CSG/CRDS : <strong>238,26 €</strong></p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 4 : Assurance chômage</h3>
                <p>Depuis octobre 2018, l'assurance chômage n'est plus à la charge du salarié mais uniquement de l'employeur (4,05% du brut).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Total des cotisations et salaire net</h3>
                <p>Total cotisations salariales : 182,50 + 100,25 + 238,26 = <strong>521,01 €</strong><br>
                Salaire net avant impôt : 2 500 - 521,01 = <strong>1 978,99 € (environ 1 979 €)</strong><br>
                Taux de cotisations : 521,01 / 2 500 = <strong>20,84%</strong></p>
                <p>Ce taux de 21% environ est représentatif pour un salaire non-cadre inférieur au plafond de la Sécurité sociale. Notez que certains employeurs appliquent des cotisations complémentaires (mutuelle, prévoyance) qui peuvent augmenter légèrement le taux total.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact du dépassement du plafond de la Sécurité sociale</h2>
                <p>Le <strong>plafond de la Sécurité sociale</strong> (3 864 € mensuels en 2026) est un seuil important dans le calcul des cotisations. Au-delà de ce montant, certaines cotisations changent :</p>
                <ul>
                    <li>La cotisation <strong>vieillesse plafonnée (6,90%)</strong> ne s'appliqué plus sur la part dépassant 3 864 €</li>
                    <li>La cotisation <strong>AGIRC-ARRCO passé de 3,15% à 8,64%</strong> sur la tranche 2 (au-delà du plafond)</li>
                    <li>La <strong>CEG augmente</strong> de 0,86% à 1,08% sur la tranche 2</li>
                </ul>
                <p>Exemple concret : pour un non-cadre gagnant <strong>4 500 € brut</strong> :</p>
                <ul>
                    <li>Sur les 3 864 premiers euros : taux de ~22%</li>
                    <li>Sur les 636 € restants : vieillesse plafonnée supprimée (-6,90%) mais AGIRC-ARRCO augmenté (+5,49%)</li>
                    <li>Résultat : légère baisse du taux global de cotisations sur la tranche 2</li>
                    <li>Salaire net : environ 3 496 € (taux global ~22,3%)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Évolution possible vers le statut cadre</h3>
                <p>De nombreux non-cadres évoluent vers le <a href="/salaire-brut-net-cadre/" class="text-brand-600 hover:text-brand-700">statut cadre</a> au cours de leur carrière. Cette évolution dépend de plusieurs facteurs :</p>
                <ul>
                    <li><strong>La convention collective</strong> de votre entreprise, qui définit les critères d'accès au statut cadre (niveau de responsabilité, diplômes, ancienneté)</li>
                    <li><strong>Une promotion interne</strong> vers un poste d'encadrement ou de conception</li>
                    <li><strong>Une mobilité professionnelle</strong> vers un poste à plus hautes responsabilités</li>
                    <li><strong>L'obtention d'un diplôme</strong> (Bac+5, MBA) qui peut justifier le passage au statut cadre</li>
                </ul>
                <p>Le passage au statut cadre s'accompagne généralement d'une augmentation de salaire qui compense largement la légère hausse des cotisations (CET à 0,14%). Il ouvre également droit à la prévoyance cadre obligatoire et améliore les perspectives de retraite complémentaire.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Avantages et protections spécifiques des non-cadres</h2>
                <p>Bien que le statut non-cadre soit parfois perçu comme moins prestigieux que le statut cadre, il offre plusieurs avantages et protections :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Décompte horaire et heures supplémentaires</h3>
                <p>Contrairement aux cadres au forfait jours, les non-cadres bénéficient d'un <strong>décompte horaire</strong> de leur temps de travail. Cela signifie :</p>
                <ul>
                    <li>Toute heure travaillée au-delà de 35h par semaine (ou de la durée conventionnelle) donne droit à une <strong>majoration de salaire</strong> (25% pour les 8 premières heures sup, 50% au-delà)</li>
                    <li>Les heures supplémentaires sont exonérées d'impôt sur le revenu dans la limite de 7 500 € par an</li>
                    <li>La durée du travail est strictement encadrée par la loi (amplitude maximale, repos obligatoires)</li>
                </ul>
                <p>Pour un non-cadre au <a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC</a> (1 801,80 € brut), 10 heures supplémentaires par mois à 25% représentent environ 135 € brut supplémentaires, soit 105 € net non imposables.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Mutuelle et prévoyance d'entreprise</h3>
                <p>Depuis 2016, tous les salariés du privé (cadres et non-cadres) doivent bénéficier d'une <strong>mutuelle santé collective</strong> financée au minimum à 50% par l'employeur. La part employeur est exonérée de cotisations sociales dans certaines limites.</p>
                <p>De nombreuses entreprises proposent également une <strong>prévoyance collective</strong> pour les non-cadres (bien que non obligatoire contrairement aux cadres), couvrant l'incapacité de travail, l'invalidité et le décès.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Comité Social et Économique (CSE)</h3>
                <p>Le <strong>CSE</strong> (anciennement CE, comité d'entreprise) distribue des avantages sociaux et culturels financés par une contribution patronale (généralement 0,2 à 2% de la masse salariale). Ces avantages peuvent inclure :</p>
                <ul>
                    <li>Chèques vacances, chèques cadeaux</li>
                    <li>Billetterie à tarif réduit (cinéma, parcs d'attraction)</li>
                    <li>Participations aux frais de garde d'enfants</li>
                    <li>Aide au logement, prêts à taux zéro</li>
                </ul>
                <p>Ces avantages sont exonérés de cotisations sociales et d'impôt sur le revenu dans certaines limites (en général pour les événements familiaux et les activités sociales et culturelles).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Période d'essai et préavis</h3>
                <p>Pour les non-cadres, la <strong>période d'essai</strong> est généralement plus courte que pour les cadres :</p>
                <ul>
                    <li>Employés/ouvriers : 2 mois renouvelable 1 fois (soit 4 mois maximum)</li>
                    <li>Agents de maîtrise/techniciens : 3 mois renouvelable 1 fois (soit 6 mois maximum)</li>
                </ul>
                <p>Le <strong>préavis de démission</strong> est également plus court (1 à 2 mois selon les conventions collectives), ce qui facilite la mobilité professionnelle.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques pour les salariés non-cadres</h2>
                <p>Voici quelques conseils pour optimiser votre situation en tant que non-cadre :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Vérifiez votre fiche de paie tous les mois</h3>
                <p>Les erreurs sur les <a href="/lire-fiche-de-paie/" class="text-brand-600 hover:text-brand-700">fiches de paie</a> sont fréquentes. Vérifiez notamment :</p>
                <ul>
                    <li>Le nombre d'heures travaillées et d'heures supplémentaires</li>
                    <li>Les primes et indemnités (prime d'ancienneté, prime de 13ème mois, prime de panier)</li>
                    <li>Le bon calcul des cotisations (environ 22% du brut pour un non-cadre)</li>
                    <li>La cohérence entre le net à payer avant impôt et le net à payer (après prélèvement à la source)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Négociez votre salaire régulièrement</h3>
                <p>Même en tant que non-cadre, vous pouvez <a href="/negocier-salaire/" class="text-brand-600 hover:text-brand-700">négocier votre salaire</a>. Les meilleurs moments sont :</p>
                <ul>
                    <li>Lors de l'embauche</li>
                    <li>Après une formation qualifiante</li>
                    <li>Lors de l'entretien annuel d'évaluation</li>
                    <li>Après un changement de fonctions ou de responsabilités</li>
                </ul>
                <p>Préparez votre argumentaire en vous basant sur le <a href="/salaire-moyen-france/" class="text-brand-600 hover:text-brand-700">salaire moyen</a> de votre secteur d'activité et de votre région.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Profitez des dispositifs d'épargne salariale</h3>
                <p>Si votre entreprise propose de l'<strong>intéressement</strong>, de la <strong>participation</strong> ou un <strong>PEE/PERCO</strong>, profitez-en. Ces dispositifs sont très avantageux fiscalement et permettent de se constituer une épargne sans effort.</p>
            """
        },
        {
            "slug": "salaire-brut-net-fonction-publique",
            "title": "Brut Net Fonction Publique 2026 : Calcul Fonctionnaire",
            "desc": "Calculez votre salaire brut en net fonction publique en 2026. Cotisations spécifiques fonctionnaire, taux réduits et simulateur gratuit. Résultat instantané.",
            "kw": "salaire brut net fonction publique, brut net fonctionnaire, cotisations fonctionnaire, traitement brut net",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Fonction Publique</span> 2026",
            "statut_default": "non-cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Particularités de la fonction publique</h2>
                <p>Les <strong>fonctionnaires</strong> bénéficient de cotisations sociales plus faibles que les salariés du privé. Le taux de cotisations salariales est d'environ <strong>16 à 17%</strong> du traitement brut, contre 22-25% dans le privé.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cotisations spécifiques fonctionnaire</h3>
                <ul class="space-y-1">
                    <li><strong>Pension civile (retraite)</strong> : 11,10% du traitement indiciaire</li>
                    <li><strong>CSG déductible</strong> : 6,80% (sur 98,25% du brut)</li>
                    <li><strong>CSG non déductible</strong> : 2,40%</li>
                    <li><strong>CRDS</strong> : 0,50%</li>
                    <li><strong>RAFP</strong> : 5% (sur primes, plafonné à 20% du traitement)</li>
                </ul>
                <p>Les fonctionnaires ne cotisent <strong>pas au chômage</strong> ni à la retraite complémentaire AGIRC-ARRCO (ils ont le régime de la CNRACL ou la pension civile).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Règle de conversion rapide</h3>
                <p>Pour un fonctionnaire, le salaire net représente environ <strong>83% du traitement brut</strong> (hors primes), soit un taux de cotisation d'environ 17%. C'est plus avantageux que le privé.</p>
                <p class="text-sm text-slate-500 mt-4">Note : notre calculateur ci-dessous utilise les taux du secteur privé. Pour un calcul précis fonction publique, appliquez un coefficient d'environ 0,83 à votre traitement brut.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Les trois fonctions publiques en France</h2>
                <p>Le secteur public français se divise en <strong>trois fonctions publiques</strong> distinctes, chacune ayant ses propres règles de rémunération et de cotisations :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Fonction Publique d'État (FPE)</h3>
                <p>La FPE regroupe les ministères et services déconcentrés de l'État (Éducation nationale, Police, Finances publiques, etc.). Elle emploie environ <strong>2,5 millions d'agents</strong>. Les fonctionnaires d'État cotisent au régime de retraite de la <strong>pension civile de l'État</strong> ou au régime spécial pour certaines catégories (militaires, magistrats).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Fonction Publique Territoriale (FPT)</h3>
                <p>La FPT concerne les collectivités locales : régions, départements, communes et leurs établissements publics. Elle compte environ <strong>2 millions d'agents</strong>. Les fonctionnaires territoriaux cotisent à la <strong>CNRACL</strong> (Caisse Nationale de Retraites des Agents des Collectivités Locales), sauf s'ils travaillent à temps non complet (moins de 28h par semaine), auquel cas ils relèvent du régime général.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Fonction Publique Hospitalière (FPH)</h3>
                <p>La FPH emploie le personnel des hôpitaux publics, maisons de retraite publiques et établissements médico-sociaux publics. Elle représente environ <strong>1,2 million d'agents</strong>. Les fonctionnaires hospitaliers cotisent également à la <strong>CNRACL</strong>, avec les mêmes règles que la FPT.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">La grille indiciaire et le système de points d'indice</h2>
                <p>Dans la fonction publique, la rémunération de base (le <strong>traitement indiciaire</strong>) est calculée selon une grille standardisée basée sur des points d'indice. Chaque fonctionnaire se voit attribuer un <strong>indice majoré</strong> qui dépend de son grade, son échelon et son ancienneté.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Comment calculer son traitement brut ?</h3>
                <p>La formule est simple :<br>
                <strong>Traitement brut mensuel = (Indice majoré × Valeur du point) / 12</strong></p>
                <p>En 2026, la <strong>valeur annuelle du point d'indice</strong> est de 60,4942 € (inchangée depuis juillet 2023). Un fonctionnaire à l'indice majoré 500 gagne donc :</p>
                <p>(500 × 60,4942) / 12 = <strong>2 520,59 € brut mensuel</strong></p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de grilles indiciaires 2026</h3>
                <ul>
                    <li><strong>Adjoint administratif 1ère classe (début)</strong> : IM 352 → 1 781 € brut</li>
                    <li><strong>Attaché territorial (début)</strong> : IM 390 → 1 973 € brut</li>
                    <li><strong>Professeur certifié (début)</strong> : IM 450 → 2 277 € brut</li>
                    <li><strong>Ingénieur territorial (fin de carrière)</strong> : IM 821 → 4 153 € brut</li>
                    <li><strong>Professeur agrégé (fin de carrière)</strong> : IM 1 067 → 5 395 € brut</li>
                </ul>
                <p>Ces montants sont des traitements indiciaires bruts, auxquels s'ajoutent éventuellement des primes et indemnités.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Primes et indemnités dans la fonction publique</h2>
                <p>En plus du traitement indiciaire, les fonctionnaires peuvent percevoir diverses <strong>primes et indemnités</strong> qui varient fortement selon les corps et les fonctions :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Nouvelle Bonification Indiciaire (NBI)</h3>
                <p>La NBI est attribuée aux agents exerçant des fonctions comportant une responsabilité ou une technicité particulière. Elle s'ajoute à l'indice majoré (généralement entre 10 et 50 points supplémentaires) et ouvre des droits à retraite.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">IFSE (Indemnité de Fonctions, de Sujétions et d'Expertise)</h3>
                <p>L'IFSE a remplacé plusieurs anciennes primes dans la fonction publique territoriale. Elle est modulable et peut représenter de quelques dizaines à plusieurs centaines d'euros mensuels selon les responsabilités exercées.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">CIA (Complément Indemnitaire Annuel)</h3>
                <p>Le CIA est une prime annuelle versée en une ou plusieurs fois. Son montant varie fortement selon les filières (de 300 € à plus de 1 500 € par an).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Autres primes courantes</h3>
                <ul>
                    <li><strong>Supplément Familial de Traitement (SFT)</strong> : versé aux agents ayant des enfants à charge (de 2,29 € à 120 € par mois selon le nombre d'enfants)</li>
                    <li><strong>Indemnité de résidence</strong> : varie selon la zone géographique (0%, 1% ou 3% du traitement brut)</li>
                    <li><strong>GIPA</strong> (Garantie Individuelle du Pouvoir d'Achat) : versée aux agents dont le traitement n'a pas suffisamment augmenté sur 4 ans</li>
                </ul>
                <p>Important : les primes sont soumises aux cotisations sociales (CSG, CRDS, RAFP) mais ne comptent que partiellement pour la retraite (seulement via le RAFP, plafonné à 20% du traitement indiciaire).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparaison fonction publique vs secteur privé</h2>
                <p>Le choix entre fonction publique et privé ne se résume pas au salaire brut. Voici une analyse comparative détaillée :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages de la fonction publique</h3>
                <ul>
                    <li><strong>Sécurité de l'emploi</strong> : les fonctionnaires titulaires ne peuvent être licenciés (sauf faute grave ou insuffisance professionnelle avec procédure stricte)</li>
                    <li><strong>Cotisations sociales plus faibles</strong> : environ 17% contre 22-25% dans le privé, ce qui améliore le pouvoir d'achat</li>
                    <li><strong>Déroulement de carrière prévisible</strong> : avancement automatique à l'ancienneté via les échelons</li>
                    <li><strong>Retraite calculée sur les 6 derniers mois</strong> (pour la FPE et la FPT) contre les 25 meilleures années dans le privé</li>
                    <li><strong>Mobilité géographique facilitée</strong> : détachement et mutation possibles dans toute la France</li>
                    <li><strong>Congés généreux</strong> : 25 jours de CA minimum + jours de RTT selon les cas + congés spéciaux (mariage, naissance, etc.)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Inconvénients de la fonction publique</h3>
                <ul>
                    <li><strong>Salaires inférieurs au privé</strong> pour les profils qualifiés, notamment en début de carrière (ingénieurs, informaticiens, cadres commerciaux)</li>
                    <li><strong>Primes limitées</strong> : le régime indemnitaire représente souvent moins de 20% de la rémunération totale</li>
                    <li><strong>Progression salariale lente</strong> : le point d'indice est gelé la plupart du temps (seulement 3 revalorisations entre 2010 et 2024)</li>
                    <li><strong>Pas d'assurance chômage</strong> : en cas de démission ou rupture conventionnelle, pas d'indemnisation Pôle emploi</li>
                    <li><strong>Rigidité</strong> : difficultés pour changer de métier ou de filière sans repasser un concours</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Comparaison salariale concrète</h3>
                <p>Voici quelques comparaisons entre postes équivalents public/privé (salaires bruts mensuels moyens 2026) :</p>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Poste</th>
                            <th class="border border-slate-300 px-4 py-2">Fonction Publique</th>
                            <th class="border border-slate-300 px-4 py-2">Secteur Privé</th>
                            <th class="border border-slate-300 px-4 py-2">Écart</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2">Assistant administratif débutant</td><td class="border border-slate-300 px-4 py-2">1 800 €</td><td class="border border-slate-300 px-4 py-2">1 900 €</td><td class="border border-slate-300 px-4 py-2">-5%</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Infirmier 5 ans d'expérience</td><td class="border border-slate-300 px-4 py-2">2 400 €</td><td class="border border-slate-300 px-4 py-2">2 600 €</td><td class="border border-slate-300 px-4 py-2">-8%</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Ingénieur informatique débutant</td><td class="border border-slate-300 px-4 py-2">2 500 €</td><td class="border border-slate-300 px-4 py-2">3 200 €</td><td class="border border-slate-300 px-4 py-2">-22%</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Cadre confirmé (10 ans exp.)</td><td class="border border-slate-300 px-4 py-2">3 500 €</td><td class="border border-slate-300 px-4 py-2">4 500 €</td><td class="border border-slate-300 px-4 py-2">-22%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">L'écart se creuse pour les profils très qualifiés et les postes à responsabilités. En revanche, pour les postes d'exécution, la fonction publique reste compétitive grâce à la sécurité de l'emploi et aux cotisations réduites.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">La retraite dans la fonction publique</h2>
                <p>Le <strong>système de retraite des fonctionnaires</strong> diffère sensiblement de celui du secteur privé :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul de la pension de base</h3>
                <p>La pension de retraite d'un fonctionnaire est calculée selon la formule :<br>
                <strong>Pension = Traitement indiciaire des 6 derniers mois × Taux de liquidation × Pourcentage de bonification</strong></p>
                <ul>
                    <li><strong>Traitement de référence</strong> : moyenne des 6 derniers mois (hors primes), contre 25 meilleures années dans le privé</li>
                    <li><strong>Taux de liquidation</strong> : 75% maximum pour 43 ans de service (contre 50% dans le privé pour 172 trimestres)</li>
                    <li><strong>Âge de départ</strong> : 62 ans (comme dans le privé) sauf pour les catégories actives (policiers, infirmiers) qui peuvent partir dès 52 ou 57 ans</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">RAFP : la retraite complémentaire des fonctionnaires</h3>
                <p>Depuis 2005, les fonctionnaires cotisent au <strong>RAFP</strong> (Retraite Additionnelle de la Fonction Publique) sur leurs primes et indemnités, dans la limite de 20% du traitement indiciaire. Le taux de cotisation est de 10% (5% salarié + 5% employeur).</p>
                <p>Le RAFP fonctionne par points, comme l'AGIRC-ARRCO. Cependant, les montants sont généralement modestes car les primes représentent une faible part de la rémunération totale dans la fonction publique (15 à 25% en moyenne).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple de calcul de pension</h3>
                <p>Un fonctionnaire partant à 62 ans avec 42 ans de service et un traitement indiciaire de 3 000 € :</p>
                <ul>
                    <li>Taux de liquidation : (42/43) × 75% = 73,26%</li>
                    <li>Pension de base : 3 000 × 73,26% = <strong>2 198 € brut/mois</strong></li>
                    <li>Pension nette (après CSG/CRDS ~9%) : environ <strong>2 000 € net/mois</strong></li>
                </ul>
                <p>À cela s'ajoute la pension RAFP (variable selon les primes accumulées) qui représente généralement 50 à 150 € supplémentaires par mois.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Contractuels de la fonction publique</h2>
                <p>Tous les agents publics ne sont pas fonctionnaires titulaires. Les <strong>contractuels</strong> (ou agents non titulaires) représentent environ 20% des effectifs de la fonction publique. Ils sont recrutés en CDD ou CDI et relèvent du régime général de la Sécurité sociale (comme les salariés du privé).</p>
                <p>Les contractuels cotisent donc aux taux du privé (environ 22% de cotisations salariales) et bénéficient du régime de retraite de base et complémentaire du privé (AGIRC-ARRCO). Leur <a href="/difference-salaire-brut-net/" class="text-brand-600 hover:text-brand-700">salaire net</a> est donc inférieur à celui d'un titulaire pour un même brut.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">CDIsation des contractuels</h3>
                <p>Depuis la loi de transformation de la fonction publique de 2019, les contractuels en CDD depuis au moins 6 ans peuvent demander un <strong>CDI de droit public</strong>. Ce CDI offre plus de stabilité mais ne confère pas le statut de fonctionnaire titulaire (pas de garantie d'emploi à vie, pas de pension civile).</p>
            """
        },
        {
            "slug": "salaire-brut-net-auto-entrepreneur",
            "title": "Salaire Brut Net Auto-Entrepreneur 2026 : Calcul Revenus",
            "desc": "Calculez vos revenus nets en auto-entrepreneur et micro-entreprise en 2026. Cotisations sociales, abattement fiscal et simulateur gratuit. Résultat instantané.",
            "kw": "auto entrepreneur brut net, revenu net auto entrepreneur, charges micro entreprise, cotisations auto entrepreneur",
            "h1": "Revenus <span class=\"text-brand-600\">Auto-Entrepreneur</span> 2026",
            "statut_default": "non-cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le régime auto-entrepreneur (micro-entreprise)</h2>
                <p>Le calcul brut/net pour un <strong>auto-entrepreneur</strong> est très différent du salariat. Il n'y a pas de "salaire brut" à proprement parler, mais un <strong>chiffre d'affaires</strong> sur lequel sont appliquées des cotisations forfaitaires.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Taux de cotisations micro-entreprise 2026</h3>
                <ul class="space-y-1">
                    <li><strong>Prestations de services (BIC)</strong> : 21,2% du CA</li>
                    <li><strong>Prestations de services (BNC)</strong> : 21,1% du CA</li>
                    <li><strong>Activités commerciales (vente)</strong> : 12,3% du CA</li>
                    <li><strong>Professions libérales (CIPAV)</strong> : 21,2% du CA</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Versement libératoire de l'impôt</h3>
                <p>Si vous optez pour le <strong>versement libératoire</strong>, un taux supplémentaire s'ajoute :</p>
                <ul>
                    <li>Vente de marchandises : +1%</li>
                    <li>Prestations de services BIC : +1,7%</li>
                    <li>Prestations de services BNC : +2,2%</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple concret</h3>
                <p>Pour un consultant en micro-BNC facturant <strong>5 000 € par mois</strong> :</p>
                <ul>
                    <li>Cotisations sociales : 5 000 × 21,1% = 1 055 €</li>
                    <li>Revenu net avant impôt : environ <strong>3 945 €</strong></li>
                </ul>
                <p class="text-sm text-slate-500 mt-4">Note : le calculateur ci-dessous est conçu pour les salariés du privé. Les auto-entrepreneurs doivent appliquer les taux forfaitaires ci-dessus.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Plafonds de chiffre d'affaires 2026</h2>
                <p>Pour bénéficier du régime de la <strong>micro-entreprise</strong>, votre chiffre d'affaires annuel ne doit pas dépasser certains seuils. En 2026, les plafonds sont :</p>
                <ul>
                    <li><strong>Activités de vente de marchandises</strong> (BIC) : 188 700 € de CA annuel</li>
                    <li><strong>Prestations de services commerciales ou artisanales</strong> (BIC) : 77 700 € de CA annuel</li>
                    <li><strong>Prestations de services libérales</strong> (BNC) : 77 700 € de CA annuel</li>
                    <li><strong>Activités mixtes</strong> : 188 700 € au total, dont maximum 77 700 € pour les prestations de services</li>
                </ul>
                <p>Si vous dépassez ces plafonds <strong>deux années consécutives</strong>, vous basculez automatiquement au régime réel d'imposition (entreprise individuelle classique ou société). En cas de dépassement ponctuel, vous bénéficiez d'une année de tolérance.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Franchise de TVA</h3>
                <p>Les auto-entrepreneurs bénéficient d'une <strong>franchise en base de TVA</strong>, ce qui signifie qu'ils ne facturent pas la TVA à leurs clients et ne la récupèrent pas sur leurs achats. Les seuils de franchise sont :</p>
                <ul>
                    <li>Vente de marchandises : 91 900 € (seuil majoré : 101 000 €)</li>
                    <li>Prestations de services : 36 800 € (seuil majoré : 39 100 €)</li>
                </ul>
                <p>Au-delà de ces seuils, vous devez facturer la TVA dès le 1er jour du mois de dépassement.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">ACRE : exonération de cotisations en début d'activité</h2>
                <p>L'<strong>ACRE</strong> (Aide à la Création ou à la Reprise d'Entreprise) permet aux nouveaux auto-entrepreneurs de bénéficier d'une <strong>exonération partielle de cotisations sociales</strong> pendant la première année d'activité.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Taux réduits avec l'ACRE (première année)</h3>
                <ul>
                    <li>Vente de marchandises : <strong>6,2%</strong> au lieu de 12,3%</li>
                    <li>Prestations de services BIC : <strong>10,6%</strong> au lieu de 21,2%</li>
                    <li>Prestations de services BNC : <strong>10,6%</strong> au lieu de 21,1%</li>
                    <li>Professions libérales CIPAV : <strong>10,6%</strong> au lieu de 21,2%</li>
                </ul>
                <p>L'ACRE s'appliqué automatiquement à tous les créateurs d'auto-entreprise depuis 2020. L'exonération est dégressive : taux réduit la 1ère année, puis retour au taux normal dès la 2ème année.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple chiffré de l'ACRE</h3>
                <p>Un consultant en micro-BNC réalisant 40 000 € de CA la première année :</p>
                <ul>
                    <li><strong>Avec ACRE</strong> : 40 000 × 10,6% = 4 240 € de cotisations → Revenu net : 35 760 €</li>
                    <li><strong>Sans ACRE</strong> : 40 000 × 21,1% = 8 440 € de cotisations → Revenu net : 31 560 €</li>
                    <li><strong>Économie</strong> : 4 200 € sur la première année</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparaison micro-entreprise vs SASU vs EURL</h2>
                <p>Choisir entre auto-entreprise, SASU ou EURL dépend de votre activité, de votre CA prévisionnel et de vos objectifs. Voici un comparatif détaillé :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Auto-entreprise (micro-entreprise)</h3>
                <p><strong>Avantages :</strong></p>
                <ul>
                    <li>Formalités de création simplissimes (gratuit, en ligne en 10 minutes)</li>
                    <li>Comptabilité ultra-légère (simple livre de recettes)</li>
                    <li>Cotisations proportionnelles au CA (si pas de CA, pas de cotisations)</li>
                    <li>Pas de TVA à gérer (franchise en base)</li>
                </ul>
                <p><strong>Inconvénients :</strong></p>
                <ul>
                    <li>Plafonds de CA limitants (77 700 € ou 188 700 €)</li>
                    <li>Impossibilité de déduire les charges réelles (seulement abattement forfaitaire)</li>
                    <li>Protection sociale moins bonne que les salariés (pas de chômage, retraite calculée sur le CA)</li>
                    <li>Responsabilité illimitée (patrimoine personnel engagé, sauf résidence principale protégée)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">SASU (Société par Actions Simplifiée Unipersonnelle)</h3>
                <p><strong>Avantages :</strong></p>
                <ul>
                    <li>Régime général de la Sécurité sociale (assimilé salarié) → meilleure protection sociale</li>
                    <li>Optimisation possible en arbitrant salaire/dividendes</li>
                    <li>Responsabilité limitée au capital social</li>
                    <li>Image plus professionnelle auprès des clients</li>
                    <li>Possibilité de déduire toutes les charges réelles</li>
                </ul>
                <p><strong>Inconvénients :</strong></p>
                <ul>
                    <li>Coût de création (500 à 1 500 €) et de gestion annuelle (expert-comptable obligatoire)</li>
                    <li>Cotisations sociales élevées sur les salaires (environ 80% du salaire net)</li>
                    <li>Formalisme administratif lourd (AG annuelle, dépôt des comptes, etc.)</li>
                    <li>Pas d'assurance chômage (sauf si option coûteuse)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">EURL (Entreprise Unipersonnelle à Responsabilité Limitée)</h3>
                <p><strong>Avantages :</strong></p>
                <ul>
                    <li>Cotisations sociales calculées sur le bénéfice (environ 45% pour les TNS)</li>
                    <li>Déduction de toutes les charges réelles</li>
                    <li>Responsabilité limitée au capital social</li>
                    <li>Régime fiscal avantageux (IR ou IS au choix)</li>
                </ul>
                <p><strong>Inconvénients :</strong></p>
                <ul>
                    <li>Protection sociale des TNS (Travailleurs Non Salariés) moins bonne que le régime général</li>
                    <li>Cotisations minimales même en cas de déficit</li>
                    <li>Formalisme administratif (comptabilité, déclarations)</li>
                    <li>Coût de création et de gestion</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Quel statut choisir selon votre CA ?</h3>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">CA annuel prévisionnel</th>
                            <th class="border border-slate-300 px-4 py-2">Statut recommandé</th>
                            <th class="border border-slate-300 px-4 py-2">Raison</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2">0 - 30 000 €</td><td class="border border-slate-300 px-4 py-2">Auto-entreprise</td><td class="border border-slate-300 px-4 py-2">Simplicité maximale, pas de charges fixes</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">30 000 - 70 000 €</td><td class="border border-slate-300 px-4 py-2">Auto-entreprise ou EURL</td><td class="border border-slate-300 px-4 py-2">Selon le niveau de charges réelles</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">70 000 - 150 000 €</td><td class="border border-slate-300 px-4 py-2">EURL ou SASU</td><td class="border border-slate-300 px-4 py-2">Optimisation fiscale et sociale</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">&gt; 150 000 €</td><td class="border border-slate-300 px-4 py-2">SASU ou SAS</td><td class="border border-slate-300 px-4 py-2">Protection sociale et développement</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">CFE et impôts locaux de l'auto-entrepreneur</h2>
                <p>En tant qu'auto-entrepreneur, vous êtes redevable de la <strong>Cotisation Foncière des Entreprises (CFE)</strong>, un impôt local dû par toutes les entreprises exerçant une activité professionnelle au 1er janvier de l'année.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exonération de CFE la première année</h3>
                <p>Bonne nouvelle : vous êtes automatiquement <strong>exonéré de CFE</strong> l'année de création de votre auto-entreprise. La CFE devient due à partir de la 2ème année d'activité.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Montant de la CFE</h3>
                <p>Le montant de la CFE varie selon votre commune et votre CA :</p>
                <ul>
                    <li>CA &lt; 10 000 € : entre <strong>220 € et 550 €</strong> selon la commune</li>
                    <li>CA entre 10 000 € et 32 600 € : entre <strong>220 € et 1 100 €</strong></li>
                    <li>CA entre 32 600 € et 100 000 € : entre <strong>220 € et 2 400 €</strong></li>
                </ul>
                <p>La CFE est payable en novembre (ou en deux fois en juin et novembre si le montant dépassé 3 000 €). Elle est déductible du bénéfice imposable si vous êtes à l'IR.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exonérations possibles de CFE</h3>
                <p>Certains auto-entrepreneurs peuvent bénéficier d'exonérations permanentes ou temporaires :</p>
                <ul>
                    <li><strong>Auto-entrepreneurs domiciliés à domicile</strong> sans espace dédié à l'activité professionnelle peuvent être exonérés (selon les communes)</li>
                    <li><strong>Artisans</strong> sont exonérés si leur CA est inférieur à 5 000 €</li>
                    <li><strong>Zones prioritaires</strong> (QPV, ZRR, ZFU) : exonération possible pendant 5 ans</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cumul salariat + auto-entreprise</h2>
                <p>Il est tout à fait possible de <strong>cumuler un emploi salarié</strong> et une auto-entreprise. C'est même très courant : environ 30% des auto-entrepreneurs ont également une activité salariée.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Conditions du cumul</h3>
                <ul>
                    <li><strong>Vérifiez votre contrat de travail</strong> : certains contrats comportent une clause d'exclusivité ou de non-concurrence qui peut limiter ou interdire une activité parallèle</li>
                    <li><strong>Informez votre employeur</strong> si votre contrat l'exige (clause de loyauté)</li>
                    <li><strong>Ne concurrencez pas votre employeur</strong> : vous ne pouvez pas démarcher ses clients ou exercer une activité concurrente</li>
                    <li><strong>Respectez la durée maximale du travail</strong> : la somme des deux activités ne doit pas dépasser 48h par semaine en moyenne (ou 60h ponctuellement)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cotisations sociales en cumul</h3>
                <p>Attention : vous cotisez <strong>deux fois aux régimes sociaux</strong> (salarié + auto-entrepreneur), mais vous ne cumulez pas forcément tous les droits. Par exemple :</p>
                <ul>
                    <li><strong>Retraite</strong> : vous cotisez aux deux régimes (général + SSI), vous accumulerez des trimestres dans les deux régimes (maximum 4 par an) et deux pensions à la retraite</li>
                    <li><strong>Maladie</strong> : une seule couverture, rattachée à votre activité principale (généralement le salariat si CA auto-entrepreneur &lt; revenu salarié)</li>
                    <li><strong>Chômage</strong> : vos cotisations d'auto-entrepreneur ne donnent pas droit au chômage. Seule votre activité salariée ouvre des droits à Pôle emploi</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Optimisation fiscale du cumul</h3>
                <p>Le cumul salariat + auto-entreprise peut être fiscalement intéressant :</p>
                <ul>
                    <li>Votre revenu auto-entrepreneur bénéficie d'un <strong>abattement forfaitaire</strong> (34% pour les BNC, 50% pour les BIC services, 71% pour la vente)</li>
                    <li>Vous pouvez déduire vos <strong>frais professionnels réels</strong> liés à l'auto-entreprise (déplacements, matériel, formations) du revenu imposable si vous optez pour la déclaration contrôlée</li>
                    <li>Les revenus de l'auto-entreprise s'ajoutent à votre salaire pour calculer votre <strong>taux de prélèvement à la source</strong>, pensez à le mettre à jour pour éviter une régularisation importante</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cessation d'activité et radiation</h2>
                <p>Fermer son auto-entreprise est aussi simple que de la créer. Il suffit de déclarer la <strong>cessation d'activité</strong> en ligne sur le guichet unique (formalites.entreprises.gouv.fr). La radiation est gratuite et immédiate.</p>
                <p>Attention : en cas de cessation, vous devez effectuer une <strong>déclaration de CA finale</strong> dans les 60 jours et payer les cotisations sociales correspondantes. Vous recevrez également une CFE au prorata du temps d'activité dans l'année.</p>
                <p>Pour comparer avec le salariat classique, consultez nos guides sur le <a href="/salaire-brut-net-cadre/" class="text-brand-600 hover:text-brand-700">statut cadre</a> et <a href="/salaire-brut-net-non-cadre/" class="text-brand-600 hover:text-brand-700">non-cadre</a>.</p>
            """
        },
        {
            "slug": "salaire-brut-net-alternance-apprentissage",
            "title": "Brut Net Alternance et Apprentissage 2026 : Simulateur",
            "desc": "Calculez votre salaire brut en net en alternance ou apprentissage en 2026. Exonérations spécifiques, grille de rémunération par âge et simulateur gratuit.",
            "kw": "salaire alternance brut net, apprentissage brut net, rémunération alternant, salaire apprenti net",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Alternance</span> 2026",
            "statut_default": "non-cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Rémunération en alternance et apprentissage</h2>
                <p>Les apprentis et alternants bénéficient d'un régime spécial : leur rémunération est calculée en <strong>pourcentage du SMIC</strong> et ils sont largement exonérés de cotisations sociales salariales.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Grille de rémunération apprentissage 2026</h3>
                <p>La rémunération minimum dépend de l'âge et de l'année d'apprentissage (base SMIC 2026 : 1 801,80 € brut) :</p>
                <ul class="space-y-1">
                    <li><strong>16-17 ans</strong> : 27% (1ère année) → 39% (2e) → 55% (3e) du SMIC</li>
                    <li><strong>18-20 ans</strong> : 43% → 51% → 67% du SMIC</li>
                    <li><strong>21-25 ans</strong> : 53% → 61% → 78% du SMIC</li>
                    <li><strong>26 ans et +</strong> : 100% du SMIC ou du minimum conventionnel</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Brut = Net pour les apprentis ?</h3>
                <p>Bonne nouvelle : pour les apprentis dont la rémunération ne dépassé pas <strong>79% du SMIC</strong>, le salaire brut est égal au salaire net. Les cotisations salariales sont entièrement exonérées.</p>
                <p>Au-delà de 79% du SMIC, seule la part excédentaire est soumise aux cotisations normales.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Contrat de professionnalisation</h3>
                <p>Les alternants en contrat de professionnalisation sont soumis aux cotisations classiques (comme un salarié standard). Leur rémunération minimum est :</p>
                <ul>
                    <li><strong>Moins de 21 ans</strong> : 55% du SMIC (65% si bac pro)</li>
                    <li><strong>21-25 ans</strong> : 70% du SMIC (80% si bac pro)</li>
                    <li><strong>26 ans et +</strong> : 100% du SMIC ou 85% du minimum conventionnel</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différences entre contrat d'apprentissage et contrat de professionnalisation</h2>
                <p>Les deux types de contrats d'alternance poursuivent le même objectif (formation en alternance), mais présentent des différences importantes :</p>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Critère</th>
                            <th class="border border-slate-300 px-4 py-2">Contrat d'apprentissage</th>
                            <th class="border border-slate-300 px-4 py-2">Contrat de professionnalisation</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Âge</strong></td><td class="border border-slate-300 px-4 py-2">16 à 29 ans (30 ans révolus)</td><td class="border border-slate-300 px-4 py-2">16 à 25 ans ou demandeurs d'emploi 26+</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Diplôme visé</strong></td><td class="border border-slate-300 px-4 py-2">CAP à diplôme d'ingénieur</td><td class="border border-slate-300 px-4 py-2">Qualification professionnelle</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Durée</strong></td><td class="border border-slate-300 px-4 py-2">6 mois à 3 ans</td><td class="border border-slate-300 px-4 py-2">6 à 12 mois (24 mois max)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Rémunération</strong></td><td class="border border-slate-300 px-4 py-2">27% à 100% du SMIC selon âge/année</td><td class="border border-slate-300 px-4 py-2">55% à 100% du SMIC selon âge/diplôme</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Cotisations</strong></td><td class="border border-slate-300 px-4 py-2">Exonération jusqu'à 79% du SMIC</td><td class="border border-slate-300 px-4 py-2">Cotisations normales</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Organisme de formation</strong></td><td class="border border-slate-300 px-4 py-2">CFA (Centre de Formation d'Apprentis)</td><td class="border border-slate-300 px-4 py-2">Organisme de formation agréé</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Avantages pour l'apprenti</h2>
                <p>Le statut d'apprenti offre de nombreux avantages au-delà de la simple formation :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Exonération d'impôt sur le revenu</h3>
                <p>Les salaires des apprentis sont <strong>exonérés d'impôt sur le revenu</strong> dans la limite du montant annuel du <a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC</a> (21 621,60 € en 2026). Concrètement, un apprenti gagnant jusqu'à 1 801,80 € brut par mois ne paie aucun impôt sur ce revenu.</p>
                <p>Si la rémunération dépasse le SMIC annuel, seule la part excédentaire est imposable. Par exemple, un apprenti de 24 ans en 3ème année gagnant 78% du SMIC (1 405 € brut) est totalement exonéré.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Aides au logement et à la mobilité</h3>
                <p>Les apprentis peuvent bénéficier de plusieurs aides financières :</p>
                <ul>
                    <li><strong>Aide Mobili-Jeune</strong> : jusqu'à 100 € par mois pour les apprentis de moins de 30 ans payant un loyer</li>
                    <li><strong>APL</strong> (Aide Personnalisée au Logement) : accessible aux apprentis sous conditions de ressources</li>
                    <li><strong>Aide au permis de conduire</strong> : 500 € pour les apprentis majeurs en contrat d'apprentissage</li>
                    <li><strong>Aide à la mobilité Erasmus+</strong> : pour les apprentis effectuant une partie de leur formation à l'étranger</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Carte d'étudiant des métiers</h3>
                <p>Les apprentis en CFA reçoivent une <strong>carte d'étudiant des métiers</strong> qui donne accès aux mêmes réductions que les étudiants : cinéma, musées, transports, restauration, abonnements divers.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Protection sociale complète</h3>
                <p>Contrairement aux stagiaires, les apprentis sont de véritables salariés avec une couverture sociale complète :</p>
                <ul>
                    <li><strong>Assurance maladie</strong> : remboursement des soins comme tout salarié</li>
                    <li><strong>Congés payés</strong> : 2,5 jours par mois travaillé (30 jours ouvrables par an)</li>
                    <li><strong>Congés pour révisions</strong> : 5 jours supplémentaires dans le mois précédant les examens</li>
                    <li><strong>Retraite</strong> : les trimestres d'apprentissage comptent pour la retraite</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Avantages pour l'employeur</h2>
                <p>Recruter un apprenti présente également de nombreux avantages pour l'entreprise :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Aides financières à l'embauche</h3>
                <p>L'État accorde une <strong>aide exceptionnelle</strong> aux entreprises qui recrutent des apprentis :</p>
                <ul>
                    <li><strong>6 000 €</strong> pour un apprenti de moins de 18 ans</li>
                    <li><strong>6 000 €</strong> pour un apprenti de 18 ans et plus (toutes entreprises)</li>
                </ul>
                <p>Cette aide est versée la première année du contrat. Les entreprises de moins de 250 salariés peuvent également bénéficier d'une aide de 1 000 € à 2 000 € pour le recrutement d'un apprenti en situation de handicap.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exonérations de charges patronales</h3>
                <p>L'employeur bénéficie d'importantes <strong>exonérations de cotisations patronales</strong> sur le salaire de l'apprenti :</p>
                <ul>
                    <li>Exonération totale des cotisations patronales pour les entreprises de moins de 11 salariés</li>
                    <li>Exonération partielle pour les entreprises de 11 salariés et plus</li>
                </ul>
                <p>Le <a href="/cout-employeur/" class="text-brand-600 hover:text-brand-700">coût employeur</a> d'un apprenti est donc très inférieur à celui d'un salarié classique.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Durée du travail et temps de formation</h2>
                <p>Le temps de travail d'un apprenti est réparti entre l'<strong>entreprise</strong> et le <strong>centre de formation</strong>. La durée légale est de 35 heures par semaine, réparties comme suit :</p>
                <ul>
                    <li>En moyenne, <strong>60 à 75%</strong> du temps en entreprise</li>
                    <li><strong>25 à 40%</strong> du temps en CFA (généralement 1 semaine sur 3, ou 2 jours par semaine)</li>
                </ul>
                <p>Le temps passé en formation est considéré comme du <strong>temps de travail effectif</strong> et rémunéré comme tel. L'apprenti ne doit donc pas effectuer d'heures supplémentaires pour compenser les jours de formation.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Heures supplémentaires des apprentis</h3>
                <p>Les apprentis de <strong>18 ans et plus</strong> peuvent effectuer des heures supplémentaires dans les mêmes conditions qu'un salarié classique (majoration de 25% ou 50%). Les apprentis mineurs peuvent également faire des heures supplémentaires, dans la limite de 5 heures par semaine, après autorisation de l'inspection du travail.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Rupture du contrat d'apprentissage</h2>
                <p>Le contrat d'apprentissage peut être rompu dans plusieurs cas :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Période d'essai (45 jours)</h3>
                <p>Durant les <strong>45 premiers jours</strong> en entreprise (hors période en CFA), le contrat peut être rompu librement par l'une ou l'autre des parties, sans motif ni indemnité.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Accord mutuel</h3>
                <p>L'employeur et l'apprenti peuvent convenir d'un commun accord de mettre fin au contrat. Cet accord doit être formalisé par écrit.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Obtention du diplôme</h3>
                <p>Si l'apprenti obtient son diplôme avant la fin du contrat, il peut mettre fin au contrat en respectant un <strong>préavis de 1 mois</strong> (notification écrite à l'employeur).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Rupture unilatérale après 45 jours</h3>
                <p>Après la période d'essai, la rupture est plus encadrée :</p>
                <ul>
                    <li><strong>Par l'apprenti</strong> : démission possible après saisine du médiateur consulaire, avec préavis minimum de 7 jours</li>
                    <li><strong>Par l'employeur</strong> : licenciement possible uniquement pour faute grave, inaptitude ou force majeure</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Après l'apprentissage : l'embauche en CDI</h2>
                <p>À l'issue du contrat d'apprentissage, l'employeur peut proposer un <strong>CDI</strong> à l'apprenti. Dans ce cas :</p>
                <ul>
                    <li><strong>Pas de période d'essai</strong> : l'apprentissage tient lieu de période d'essai</li>
                    <li><strong>Reprise de l'ancienneté</strong> : la durée du contrat d'apprentissage est prise en compte dans l'ancienneté du salarié</li>
                    <li><strong>Salaire</strong> : passage au salaire <a href="/salaire-brut-net-non-cadre/" class="text-brand-600 hover:text-brand-700">non-cadre</a> ou <a href="/salaire-brut-net-cadre/" class="text-brand-600 hover:text-brand-700">cadre</a> selon le poste, avec cotisations normales</li>
                </ul>
                <p>Environ <strong>70% des apprentis</strong> trouvent un emploi dans les 7 mois suivant leur formation, ce qui fait de l'apprentissage l'une des voies les plus efficaces pour l'insertion professionnelle.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Aide à l'embauche d'un alternant 2026</h2>
                <p>Pour encourager le recrutement d'alternants, l'État a reconduit en 2026 une <strong>aide exceptionnelle à l'embauche</strong> qui représente un avantage financier majeur pour les employeurs.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Montant de l'aide 2026</h3>
                <p>L'aide s'élève à <strong>6 000 €</strong> pour tout contrat d'apprentissage conclu entre le 1er janvier 2026 et le 31 décembre 2026, quelle que soit la taille de l'entreprise. Cette aide s'appliqué pour :</p>
                <ul>
                    <li>Les apprentis préparant un diplôme ou titre à finalité professionnelle inférieur ou égal au <strong>niveau 7 du RNCP</strong> (Bac +5, master, diplôme d'ingénieur)</li>
                    <li>Les contrats conclus dans les <strong>entreprises de moins de 250 salariés</strong> sans condition</li>
                    <li>Les entreprises de <strong>250 salariés et plus</strong> sous conditions (engagement de seuil d'alternants)</li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Modalités de versement</h3>
                <p>L'aide de 6 000 € est versée automatiquement par l'Agence de Services et de Paiement (ASP) :</p>
                <ul>
                    <li>Versement mensuel anticipé de <strong>500 €/mois pendant 12 mois</strong> (soit 6 000 € sur la première année)</li>
                    <li>Aucune démarché à effectuer : l'aide est attribuée automatiquement après transmission du contrat à l'OPCO</li>
                    <li>L'aide couvre en grande partie le coût du salaire de l'apprenti en 1ère année</li>
                </ul>
                <p>Combinée aux exonérations de charges patronales, cette aide rend le <a href="/cout-employeur/" class="text-brand-600 hover:text-brand-700">coût d'un apprenti</a> très avantageux, voire quasi nul pour les petites entreprises et les apprentis mineurs.</p>
            """
        },
        {
            "slug": "salaire-brut-net-stage",
            "title": "Salaire Brut Net Stage 2026 : Gratification Stagiaire",
            "desc": "Calculez la gratification de stage brut en net 2026. Seuil d'exonération à 4,35€/h, cotisations détaillées et montant minimum légal. Simulateur gratuit.",
            "kw": "gratification stage brut net, salaire stagiaire net, stage rémunération, indemnité stage cotisations",
            "h1": "Gratification de <span class=\"text-brand-600\">Stage</span> Brut Net 2026",
            "statut_default": "non-cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">La gratification de stage en 2026</h2>
                <p>Les stages de plus de 2 mois consécutifs doivent obligatoirement être rémunérés. On parle de <strong>gratification</strong> et non de salaire, car le stagiaire n'est pas un salarié.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Montant minimum 2026</h3>
                <p>La gratification minimum est de <strong>4,35 € par heure</strong>, soit environ <strong>669 € par mois</strong> pour un temps plein (154 heures). Ce montant correspond à 15% du plafond horaire de la Sécurité sociale.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Brut = Net pour les stagiaires</h3>
                <p>Tant que la gratification ne dépassé pas le seuil de <strong>4,35 €/heure</strong> (environ 669 €/mois), elle est <strong>totalement exonérée</strong> de cotisations sociales et d'impôt sur le revenu. Le brut est donc égal au net.</p>
                <p>Si l'employeur verse plus que le minimum, seule la <strong>fraction excédentaire</strong> est soumise aux cotisations sociales classiques.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple</h3>
                <ul>
                    <li><strong>Gratification de 669 €</strong> : 669 € net (pas de cotisations)</li>
                    <li><strong>Gratification de 1 000 €</strong> : les cotisations s'appliquent sur 331 € (1 000 - 669), net ≈ 927 €</li>
                    <li><strong>Gratification de 1 500 €</strong> : cotisations sur 831 €, net ≈ 1 317 €</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conditions légales du stage en France</h2>
                <p>Les stages en France sont strictement encadrés par la loi pour éviter les abus et garantir que le stage reste un <strong>dispositif pédagogique</strong> et non un contrat de travail déguisé.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Durée maximale du stage</h3>
                <p>Un stage ne peut pas dépasser <strong>6 mois par année d'enseignement</strong> (soit 924 heures). Cette limite s'appliqué quel que soit le nombre de stages effectués dans l'année. Au-delà, l'entreprise doit embaucher l'étudiant en <a href="/salaire-brut-net-alternance-apprentissage/" class="text-brand-600 hover:text-brand-700">contrat d'apprentissage</a> ou en contrat de professionnalisation.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Convention de stage obligatoire</h3>
                <p>Tout stage doit faire l'objet d'une <strong>convention tripartite</strong> signée entre :</p>
                <ul>
                    <li>L'établissement d'enseignement (université, école, lycée)</li>
                    <li>L'entreprise d'accueil</li>
                    <li>Le stagiaire</li>
                </ul>
                <p>La convention définit les missions, la durée, les horaires, la gratification et les conditions d'encadrement. Sans convention de stage, la relation peut être requalifiée en <strong>contrat de travail</strong>, avec obligation pour l'employeur de payer des cotisations rétroactives et d'éventuelles indemnités.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Délai de carence entre deux stages</h3>
                <p>Pour éviter que les entreprises n'enchaînent les stagiaires sur un même poste, la loi imposé un <strong>délai de carence</strong> entre deux stages sur le même poste :</p>
                <ul>
                    <li>Délai de carence = <strong>1/3 de la durée du stage précédent</strong></li>
                    <li>Exemple : après un stage de 6 mois, l'entreprise doit attendre 2 mois avant d'accueillir un nouveau stagiaire sur le même poste</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Gratification de stage : calcul détaillé</h2>
                <p>Le calcul de la gratification de stage repose sur le <strong>nombre d'heures effectuées</strong>. Le taux horaire minimum est fixé à <strong>15% du plafond horaire de la Sécurité sociale</strong>, soit 4,35 € en 2026.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Méthode de calcul</h3>
                <p>Pour calculer la gratification mensuelle :<br>
                <strong>Gratification = Nombre d'heures de présence × 4,35 €</strong></p>
                <p>Exemples concrets :</p>
                <ul>
                    <li><strong>Temps plein (35h/semaine)</strong> : 151,67 heures par mois × 4,35 € = 659,76 € (arrondi à 669 € souvent)</li>
                    <li><strong>Temps partiel (28h/semaine)</strong> : 121,33 heures par mois × 4,35 € = 527,79 €</li>
                    <li><strong>Stage de 3 semaines</strong> : 105 heures × 4,35 € = 456,75 €</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Gratification supérieure au minimum légal</h3>
                <p>L'employeur peut choisir de verser une gratification <strong>supérieure</strong> au minimum légal. Dans ce cas :</p>
                <ul>
                    <li>La fraction jusqu'à 4,35 €/h reste <strong>exonérée</strong> de cotisations sociales et d'impôt</li>
                    <li>La fraction <strong>au-delà</strong> est soumise aux cotisations sociales classiques (environ 22%) et à l'impôt sur le revenu</li>
                </ul>
                <p>Exemple : un stagiaire gratifié à 1 200 € par mois (35h/semaine) :</p>
                <ul>
                    <li>Part exonérée : 151,67 h × 4,35 € = 659,76 €</li>
                    <li>Part soumise à cotisations : 1 200 - 659,76 = 540,24 €</li>
                    <li>Cotisations salariales (~22%) : 540,24 × 22% = 118,85 €</li>
                    <li>Gratification nette : 1 200 - 118,85 = <strong>1 081,15 €</strong></li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Droits et avantages des stagiaires</h2>
                <p>Bien que les stagiaires ne soient pas des salariés, ils bénéficient de plusieurs droits et avantages :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Congés et absences</h3>
                <p>Les stagiaires ont droit à des <strong>autorisations d'absence</strong> dans les mêmes conditions que les salariés :</p>
                <ul>
                    <li><strong>Grossesse</strong> : autorisation d'absence pour les examens médicaux obligatoires</li>
                    <li><strong>Congé paternité</strong> : 25 jours (comme les salariés)</li>
                    <li><strong>Mariage, PACS, décès</strong> : jours d'absence autorisés</li>
                </ul>
                <p>Important : les stagiaires n'ont <strong>pas droit aux congés payés</strong>. En cas d'absence (maladie, congés), la gratification peut être réduite au prorata du temps effectivement présent.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Tickets restaurant et accès à la cantine</h3>
                <p>Les stagiaires doivent bénéficier des mêmes avantages que les salariés en matière de <strong>restauration</strong> :</p>
                <ul>
                    <li>Accès au restaurant d'entreprise ou aux titres-restaurant si l'entreprise en fournit aux salariés</li>
                    <li>Si l'entreprise verse des titres-restaurant, le stagiaire peut participer à hauteur de 50% de la valeur (comme un salarié)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Remboursement des frais de transport</h3>
                <p>Les employeurs doivent rembourser <strong>50% du prix des titres d'abonnement</strong> aux transports publics, exactement comme pour les salariés. Ce remboursement n'est pas considéré comme une gratification et reste exonéré de cotisations.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Protection sociale</h3>
                <p>Les stagiaires bénéficient d'une <strong>couverture sociale</strong> spécifique :</p>
                <ul>
                    <li><strong>Accident du travail</strong> : le stagiaire est couvert par l'assurance de l'établissement d'enseignement (pas par l'entreprise)</li>
                    <li><strong>Responsabilité civile</strong> : généralement couverte par l'assurance de l'école</li>
                    <li><strong>Maladie</strong> : le stagiaire reste rattaché à la Sécurité sociale étudiante ou parentale</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5. Jours de congés pour révisions et examens</h3>
                <p>Si le stage se déroule durant la période de révisions ou d'examens, le stagiaire peut demander des <strong>jours d'absence autorisée</strong> pour se préparer et passer ses examens. Ces jours ne sont généralement pas rémunérés (sauf accord de l'entreprise).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différences entre stage et emploi</h2>
                <p>Il est essentiel de comprendre qu'un <strong>stage n'est pas un emploi</strong>. Voici les principales différences :</p>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Critère</th>
                            <th class="border border-slate-300 px-4 py-2">Stage</th>
                            <th class="border border-slate-300 px-4 py-2">Emploi (CDD/CDI)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Objectif</strong></td><td class="border border-slate-300 px-4 py-2">Formation pédagogique</td><td class="border border-slate-300 px-4 py-2">Production / Travail</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Durée maximale</strong></td><td class="border border-slate-300 px-4 py-2">6 mois</td><td class="border border-slate-300 px-4 py-2">Illimitée (CDD max 18 mois)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Rémunération</strong></td><td class="border border-slate-300 px-4 py-2">Gratification (min. 669 €)</td><td class="border border-slate-300 px-4 py-2">Salaire (min. SMIC 1 802 €)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Congés payés</strong></td><td class="border border-slate-300 px-4 py-2">Non</td><td class="border border-slate-300 px-4 py-2">Oui (2,5 jours/mois)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Assurance chômage</strong></td><td class="border border-slate-300 px-4 py-2">Non</td><td class="border border-slate-300 px-4 py-2">Oui</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Cotisations retraite</strong></td><td class="border border-slate-300 px-4 py-2">Non (sauf si &gt; 669 €)</td><td class="border border-slate-300 px-4 py-2">Oui</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Protection licenciement</strong></td><td class="border border-slate-300 px-4 py-2">Aucune</td><td class="border border-slate-300 px-4 py-2">Oui (procédure encadrée)</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Risques de requalification en contrat de travail</h2>
                <p>Si le stage ne respecte pas les conditions légales, il peut être <strong>requalifié en contrat de travail</strong> par le conseil de prud'hommes. Les principaux motifs de requalification sont :</p>
                <ul>
                    <li><strong>Absence de convention de stage</strong> ou convention non conforme</li>
                    <li><strong>Missions ne correspondant pas à la formation</strong> : le stagiaire effectué des tâches purement productives sans lien avec son cursus</li>
                    <li><strong>Autonomie excessive</strong> : le stagiaire travaille sans encadrement ni suivi pédagogique</li>
                    <li><strong>Remplacement d'un salarié absent</strong> ou récemment licencié</li>
                    <li><strong>Dépassement de la durée légale</strong> de 6 mois</li>
                </ul>
                <p>En cas de requalification, l'employeur doit verser :</p>
                <ul>
                    <li>Un <strong>rappel de salaire</strong> (différence entre la gratification et le SMIC)</li>
                    <li>Les <strong>cotisations sociales</strong> rétroactives (part patronale et salariale)</li>
                    <li>D'éventuelles <strong>indemnités de licenciement</strong> si la relation est rompue sans motif valable</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Embauche après un stage</h2>
                <p>Si l'employeur souhaite <strong>embaucher le stagiaire</strong> à l'issue du stage, plusieurs options s'offrent à lui :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Embauche en CDI ou CDD classique</h3>
                <p>L'entreprise peut proposer un <a href="/salaire-brut-net-non-cadre/" class="text-brand-600 hover:text-brand-700">contrat de travail classique</a> (CDD ou CDI). Dans ce cas :</p>
                <ul>
                    <li>La <strong>période d'essai</strong> s'appliqué normalement (2 à 4 mois selon le statut)</li>
                    <li>La <strong>durée du stage</strong> peut être déduite de la période d'essai si cela est prévu dans le contrat de travail (maximum 50% de la durée du stage)</li>
                    <li>Le salaire passé au minimum au <a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC</a> (1 801,80 € brut) ou plus selon le poste</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Contrat d'apprentissage ou de professionnalisation</h3>
                <p>Si le stagiaire est encore en formation, l'entreprise peut proposer un <a href="/salaire-brut-net-alternance-apprentissage/" class="text-brand-600 hover:text-brand-700">contrat d'alternance</a>. Cette solution permet de continuer à former le jeune tout en bénéficiant d'aides financières et d'exonérations de charges.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pour les stagiaires</h2>
                <p>Voici quelques conseils pratiques pour tirer le meilleur parti de votre stage :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Négociez votre gratification</h3>
                <p>Le minimum légal est de 4,35 €/h (669 € par mois), mais de nombreuses entreprises versent davantage, surtout dans les grandes entreprises et les secteurs en tension (tech, finance, conseil). N'hésitez pas à <a href="/negocier-salaire/" class="text-brand-600 hover:text-brand-700">négocier</a> votre gratification, en particulier si vous avez déjà une expérience ou des compétences spécifiques.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Demandez une attestation de stage</h3>
                <p>À la fin du stage, demandez une <strong>attestation de stage</strong> mentionnant vos missions, vos compétences développées et la durée du stage. Ce document sera précieux pour vos futures candidatures.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Gardez le contact</h3>
                <p>Même si vous n'êtes pas embauché immédiatement, restez en contact avec votre maître de stage et les collègues que vous avez côtoyés. Ils pourront vous recommander ou vous informer d'opportunités futures.</p>
            """
        },
        {
            "slug": "salaire-brut-net-interim",
            "title": "Salaire Brut Net Intérim 2026 : Calcul Intérimaire",
            "desc": "Calculez votre salaire brut en net en intérim en 2026. IFM (10%), ICCP (10%), cotisations spécifiques intérimaire et simulateur gratuit. Résultat instantané.",
            "kw": "salaire intérim brut net, brut net intérimaire, IFM, indemnité fin de mission, ICCP",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Intérim</span> 2026",
            "statut_default": "non-cadre",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Rémunération en intérim</h2>
                <p>Les <strong>intérimaires</strong> sont soumis aux mêmes cotisations que les salariés du secteur privé. Le calcul brut/net est donc identique. Cependant, la rémunération totale inclut des primes spécifiques.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnité de Fin de Mission (IFM)</h3>
                <p>À la fin de chaque mission, l'intérimaire perçoit une <strong>IFM de 10%</strong> de la rémunération brute totale. Cette prime compense la précarité de l'emploi.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnité Compensatrice de Congés Payés (ICCP)</h3>
                <p>L'intérimaire reçoit aussi une <strong>ICCP de 10%</strong> calculée sur le brut total + IFM.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple de calcul intérim</h3>
                <p>Pour une mission d'un mois à <strong>2 000 € brut</strong> :</p>
                <ul>
                    <li>Salaire brut de base : 2 000 €</li>
                    <li>IFM (10%) : + 200 €</li>
                    <li>ICCP (10% sur 2 200 €) : + 220 €</li>
                    <li>Brut total : <strong>2 420 €</strong></li>
                    <li>Net (après ~22% de cotisations) : environ <strong>1 888 €</strong></li>
                </ul>
                <p>L'IFM et l'ICCP sont soumises aux cotisations sociales et à l'impôt sur le revenu.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le fonctionnement du travail intérimaire</h2>
                <p>Le <strong>travail intérimaire</strong> (ou travail temporaire) est une relation tripartite impliquant trois acteurs :</p>
                <ul>
                    <li><strong>L'entreprise de travail temporaire (ETT)</strong> : l'agence d'intérim qui emploie juridiquement l'intérimaire et le rémunère</li>
                    <li><strong>L'entreprise utilisatrice</strong> : l'entreprise qui accueille l'intérimaire pour réaliser une mission temporaire</li>
                    <li><strong>L'intérimaire</strong> : le salarié en mission</li>
                </ul>
                <p>L'intérimaire signe un <strong>contrat de mission</strong> avec l'ETT (et non avec l'entreprise utilisatrice). Ce contrat précise la durée, les missions, la rémunération et les conditions de travail.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cas de recours autorisés</h3>
                <p>Le recours à l'intérim n'est autorisé que dans des situations précises :</p>
                <ul>
                    <li><strong>Remplacement d'un salarié absent</strong> (congés, maladie, congé maternité)</li>
                    <li><strong>Accroissement temporaire d'activité</strong> (surcroît ponctuel de travail, commande exceptionnelle)</li>
                    <li><strong>Emploi saisonnier</strong> (vendanges, activités touristiques)</li>
                    <li><strong>Emploi d'usage</strong> dans certains secteurs (audiovisuel, spectacle, hôtellerie)</li>
                    <li><strong>Contrat de mission-formation</strong> (CDI intérimaire avec périodes de formation)</li>
                </ul>
                <p>Il est <strong>interdit</strong> de recourir à l'intérim pour :</p>
                <ul>
                    <li>Remplacer un salarié gréviste</li>
                    <li>Pourvoir un poste suite à un licenciement économique (dans les 6 mois)</li>
                    <li>Effectuer des travaux particulièrement dangereux (sauf dérogation)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Durée des contrats de mission</h2>
                <p>La durée maximale d'un <strong>contrat de mission</strong> (renouvellements inclus) dépend du motif de recours :</p>
                <ul>
                    <li><strong>Remplacement d'un salarié absent</strong> : durée de l'absence (+ éventuellement quelques jours pour le délai de préavis)</li>
                    <li><strong>Accroissement temporaire d'activité</strong> : 18 mois maximum (renouvellements inclus)</li>
                    <li><strong>Emploi saisonnier</strong> : durée de la saison</li>
                    <li><strong>Travaux urgents de sécurité</strong> : 9 mois maximum</li>
                </ul>
                <p>En cas de dépassement de la durée maximale, le contrat peut être <strong>requalifié en CDI</strong> avec l'entreprise utilisatrice.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Délai de carence entre deux missions</h3>
                <p>Pour éviter que l'intérim ne devienne un emploi permanent déguisé, la loi imposé un <strong>délai de carence</strong> entre deux missions sur le même poste :</p>
                <ul>
                    <li>Délai de carence = <strong>1/3 de la durée de la mission précédente</strong></li>
                    <li>Exemple : après une mission de 6 mois, l'entreprise doit attendre 2 mois avant de faire appel à un nouvel intérimaire sur ce poste</li>
                </ul>
                <p>Le même intérimaire peut être réembauché sans délai de carence si la mission est différente ou si des circonstances exceptionnelles le justifient.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Rémunération de l'intérimaire : principe d'égalité</h2>
                <p>Le principe fondamental est celui de <strong>l'égalité de traitement</strong> : l'intérimaire doit percevoir la même rémunération qu'un salarié permanent de l'entreprise utilisatrice occupant le même poste, à qualification et ancienneté équivalentes.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul du salaire de base</h3>
                <p>Le salaire de base de l'intérimaire ne peut pas être inférieur :</p>
                <ul>
                    <li>Au <a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC</a> (1 801,80 € brut mensuel pour 35h)</li>
                    <li>Au <strong>minimum conventionnel</strong> applicable dans l'entreprise utilisatrice pour le poste occupé</li>
                    <li>À la rémunération d'un salarié de l'entreprise utilisatrice de <strong>même qualification</strong></li>
                </ul>
                <p>Si l'entreprise utilisatrice verse des primes (13ème mois, prime d'ancienneté, prime de performance), l'intérimaire doit en bénéficier au prorata de son temps de présence.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnité de Fin de Mission (IFM) : 10%</h3>
                <p>L'<strong>IFM</strong> est une prime de précarité versée à la fin de chaque mission pour compenser l'instabilité de l'emploi intérimaire. Son montant est de <strong>10% de la rémunération totale brute</strong> (salaire + primes + heures supplémentaires).</p>
                <p>Exceptions : l'IFM n'est pas due si :</p>
                <ul>
                    <li>Le contrat de mission est suivi d'un <strong>CDI dans l'entreprise utilisatrice</strong></li>
                    <li>L'intérimaire <strong>refuse un CDI</strong> proposé par l'entreprise utilisatrice</li>
                    <li>La mission est rompue à l'initiative de l'intérimaire (démission)</li>
                    <li>Il s'agit d'un <strong>contrat saisonnier</strong> ou d'un <strong>CDI intérimaire</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnité Compensatrice de Congés Payés (ICCP) : 10%</h3>
                <p>Comme l'intérimaire ne prend généralement pas de congés pendant sa mission, il perçoit une <strong>ICCP de 10%</strong> calculée sur la rémunération brute totale <strong>augmentée de l'IFM</strong>.</p>
                <p>Formule exacte :<br>
                ICCP = (Salaire brut + IFM) × 10%</p>
                <p>Cette indemnité compense les congés payés non pris. Elle est soumise aux <a href="/cotisations-sociales-salariales/" class="text-brand-600 hover:text-brand-700">cotisations sociales</a> et à l'impôt sur le revenu.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exemple complet de calcul de rémunération intérim</h2>
                <p>Prenons l'exemple d'un intérimaire en mission pendant <strong>3 mois</strong> à raison de <strong>35h par semaine</strong>, avec un taux horaire de <strong>13 € brut</strong> :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Mois 1 : 151,67 heures travaillées</h3>
                <ul>
                    <li>Salaire brut : 151,67 h × 13 € = <strong>1 971,71 €</strong></li>
                    <li>IFM (10%) : 1 971,71 × 10% = <strong>197,17 €</strong></li>
                    <li>ICCP (10% sur 2 168,88 €) : <strong>216,89 €</strong></li>
                    <li><strong>Brut total : 2 385,77 €</strong></li>
                    <li>Cotisations salariales (~22%) : 524,87 €</li>
                    <li><strong>Net mensuel : 1 860,90 €</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Fin de mission (après 3 mois)</h3>
                <p>Si la mission dure 3 mois, l'intérimaire aura perçu :</p>
                <ul>
                    <li>3 mois de salaire : 3 × 1 971,71 = 5 915,13 €</li>
                    <li>IFM totale : 591,51 €</li>
                    <li>ICCP totale : 650,66 €</li>
                    <li><strong>Total brut sur 3 mois : 7 157,30 €</strong></li>
                    <li><strong>Total net sur 3 mois : environ 5 583 €</strong></li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Droits et avantages des intérimaires</h2>
                <p>Les intérimaires bénéficient des mêmes droits que les salariés permanents de l'entreprise utilisatrice :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Accès aux équipements collectifs</h3>
                <p>L'intérimaire a accès aux <strong>mêmes installations</strong> que les salariés permanents :</p>
                <ul>
                    <li>Restaurant d'entreprise ou tickets restaurant</li>
                    <li>Vestiaires, douches, sanitaires</li>
                    <li>Locaux de repos</li>
                    <li>Activités sociales et culturelles du CSE (si la mission dépassé 3 mois)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Transport et indemnités kilométriques</h3>
                <p>L'intérimaire bénéficie du remboursement à <strong>50% des frais de transport</strong> en commun (comme tout salarié). Si la mission nécessite des déplacements, l'entreprise utilisatrice ou l'ETT doit rembourser les frais selon le barème légal.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Formation professionnelle et DIF intérimaire</h3>
                <p>Les intérimaires cumulent des <strong>droits à la formation</strong> via le <strong>FAFTT</strong> (Fonds d'Assurance Formation du Travail Temporaire). Après 1 607 heures de travail intérimaire (équivalent d'un an à temps plein), l'intérimaire peut demander une formation financée.</p>
                <p>Le <strong>CPF</strong> (Compte Personnel de Formation) fonctionne normalement pour les intérimaires : ils accumulent 500 € par an (800 € pour les non-qualifiés).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Ancienneté et retraite</h3>
                <p>Les périodes d'intérim comptent pour :</p>
                <ul>
                    <li>Les <strong>trimestres de retraite</strong> (cotisations versées à l'assurance vieillesse)</li>
                    <li>L'<strong>ancienneté</strong> en cas d'embauche en CDI dans l'entreprise utilisatrice (si la mission a duré plus de 6 mois)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">CDI intérimaire (CDII)</h2>
                <p>Depuis 2013, les agences d'intérim peuvent proposer des <strong>CDI intérimaires</strong> (CDII). Ce type de contrat offre plus de stabilité que les missions ponctuelles :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Fonctionnement du CDII</h3>
                <ul>
                    <li>L'intérimaire est embauché en <strong>CDI par l'agence</strong> (et non en contrat de mission)</li>
                    <li>Il alterne entre <strong>périodes de mission</strong> (chez des entreprises utilisatrices) et <strong>périodes d'intermission</strong> (sans mission)</li>
                    <li>Pendant les périodes d'intermission, il perçoit une <strong>rémunération minimale</strong> garantie (généralement équivalente au SMIC)</li>
                    <li>L'agence doit proposer régulièrement des missions adaptées au profil de l'intérimaire</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages du CDII</h3>
                <ul>
                    <li><strong>Sécurité de l'emploi</strong> : revenu garanti même sans mission</li>
                    <li><strong>Continuité des droits</strong> : couverture sociale, retraite, chômage (en cas de rupture du CDII)</li>
                    <li><strong>Accès au crédit facilité</strong> : les banques considèrent le CDII comme un CDI classique</li>
                    <li><strong>Formation continue</strong> : l'agence doit proposer des formations pendant les périodes d'intermission</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Inconvénients du CDII</h3>
                <ul>
                    <li><strong>Pas d'IFM ni d'ICCP</strong> : le salarié en CDII ne perçoit pas les primes de précarité (10% + 10%)</li>
                    <li><strong>Obligation d'accepter les missions</strong> : refuser systématiquement les missions proposées peut constituer un motif de licenciement</li>
                    <li><strong>Salaire d'intermission parfois faible</strong> : si l'intérimaire enchaîne peu de missions, son revenu peut stagner au niveau du SMIC</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Rupture du contrat de mission</h2>
                <p>Le contrat de mission peut être rompu avant son terme dans plusieurs cas :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Période d'essai</h3>
                <p>Tout contrat de mission comporte une <strong>période d'essai</strong> calculée en fonction de la durée de la mission :</p>
                <ul>
                    <li>Mission ≤ 1 mois : 2 jours ouvrés</li>
                    <li>Mission de 1 à 2 mois : 3 jours ouvrés</li>
                    <li>Mission &gt; 2 mois : 5 jours ouvrés</li>
                </ul>
                <p>Pendant cette période, l'ETT ou l'intérimaire peuvent rompre le contrat librement, sans motif ni indemnité.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Embauche en CDI</h3>
                <p>L'intérimaire peut rompre le contrat de mission avant son terme s'il obtient un <strong>CDI</strong> (dans l'entreprise utilisatrice ou ailleurs). Il doit respecter un préavis (généralement 1 jour par semaine restante, plafonné à 2 semaines).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Faute grave ou force majeure</h3>
                <p>L'ETT peut rompre le contrat en cas de <strong>faute grave</strong> de l'intérimaire (vol, insubordination, non-respect des règles de sécurité). L'intérimaire peut également rompre en cas de manquement grave de l'entreprise utilisatrice (harcèlement, non-paiement du salaire).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Embauche après une mission d'intérim</h2>
                <p>Si l'entreprise utilisatrice souhaite <strong>embaucher l'intérimaire</strong> en CDI ou CDD à l'issue de la mission :</p>
                <ul>
                    <li><strong>Pas de période d'essai</strong> : la mission d'intérim tient lieu de période d'essai (si elle a duré au moins 2 mois)</li>
                    <li><strong>Reprise d'ancienneté</strong> : la durée de la mission est prise en compte dans l'ancienneté du salarié</li>
                    <li><strong>Pas d'IFM</strong> : l'intérimaire ne perçoit pas l'indemnité de fin de mission si l'embauche est immédiate</li>
                </ul>
                <p>Environ <strong>30% des intérimaires</strong> sont embauchés en CDI par l'entreprise utilisatrice après une ou plusieurs missions, ce qui fait de l'intérim un excellent tremplin vers l'emploi stable.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparaison intérim vs CDD vs CDI</h2>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Critère</th>
                            <th class="border border-slate-300 px-4 py-2">Intérim</th>
                            <th class="border border-slate-300 px-4 py-2">CDD</th>
                            <th class="border border-slate-300 px-4 py-2">CDI</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Employeur</strong></td><td class="border border-slate-300 px-4 py-2">Agence d'intérim (ETT)</td><td class="border border-slate-300 px-4 py-2">Entreprise utilisatrice</td><td class="border border-slate-300 px-4 py-2">Entreprise utilisatrice</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Durée</strong></td><td class="border border-slate-300 px-4 py-2">Variable (généralement courte)</td><td class="border border-slate-300 px-4 py-2">Maximum 18 mois</td><td class="border border-slate-300 px-4 py-2">Indéterminée</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Prime de précarité</strong></td><td class="border border-slate-300 px-4 py-2">IFM 10% + ICCP 10%</td><td class="border border-slate-300 px-4 py-2">10% en fin de contrat</td><td class="border border-slate-300 px-4 py-2">Aucune</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Congés payés</strong></td><td class="border border-slate-300 px-4 py-2">ICCP (10%)</td><td class="border border-slate-300 px-4 py-2">Oui (2,5 j/mois)</td><td class="border border-slate-300 px-4 py-2">Oui (2,5 j/mois)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Assurance chômage</strong></td><td class="border border-slate-300 px-4 py-2">Oui (fin de mission)</td><td class="border border-slate-300 px-4 py-2">Oui (fin de contrat)</td><td class="border border-slate-300 px-4 py-2">Oui (licenciement)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Flexibilité</strong></td><td class="border border-slate-300 px-4 py-2">Très élevée</td><td class="border border-slate-300 px-4 py-2">Moyenne</td><td class="border border-slate-300 px-4 py-2">Faible</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Pour en savoir plus sur les <a href="/difference-salaire-brut-net/" class="text-brand-600 hover:text-brand-700">différences entre brut et net</a> ou sur le calcul des <a href="/cout-employeur/" class="text-brand-600 hover:text-brand-700">charges patronales</a>, consultez nos guides dédiés.</p>
            """
        },
    ]

    # Add enrichment data
    for p in pages:
        slug = p["slug"]
        if slug == "salaire-brut-net-cadre":
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 3500, 4000, 5000], "cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Quelle est la différence de cotisations entre cadre et non-cadre ?", "a": "Un cadre paie la cotisation CET (0,14%) en plus. Pour un salaire sous le plafond de la Sécurité sociale, la différence est minime (quelques euros). Elle augmente pour les hauts salaires."},
                {"q": "Le statut cadre est-il avantageux ?", "a": "Oui : meilleure retraite complémentaire, prévoyance obligatoire, couverture décès/invalidité. Les cotisations légèrement supérieures financent ces avantages."},
                {"q": "À partir de quel salaire est-on cadre ?", "a": "Le statut cadre ne dépend pas du salaire mais de la convention collective et du poste. Un cadre peut gagner le SMIC, même si c'est rare en pratique."},
                {"q": "Comment passer du statut non-cadre à cadre ?", "a": "Le passage au statut cadre dépend de votre convention collective et d'un accord avec votre employeur, souvent lors d'une promotion ou d'un changement de poste."},
                {"q": "Les cadres paient-ils plus d'impôt ?", "a": "Pas directement. L'impôt dépend du net imposable, pas du statut. Mais les cadres ont généralement des salaires plus élevés, donc un impôt plus important."},
            ])
            p["examples"] = generate_examples([
                {"name": "Sophie, 32 ans", "situation": "Ingénieure logiciel – cadre", "brut": "3 500 €", "net": "2 693 €", "net_apres_impot": "2 438 €"},
                {"name": "Marc, 45 ans", "situation": "Directeur commercial – cadre", "brut": "5 000 €", "net": "3 828 €", "net_apres_impot": "3 344 €"},
                {"name": "Léa, 28 ans", "situation": "Chef de projet marketing – cadre", "brut": "2 800 €", "net": "2 157 €", "net_apres_impot": "1 995 €"},
            ])
        elif slug == "salaire-brut-net-non-cadre":
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 3500, 4000, 5000], "non-cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Quel est le taux de cotisations pour un non-cadre ?", "a": "Environ 22% du salaire brut pour un non-cadre dont le salaire est inférieur au plafond de la Sécurité sociale (3 864 €/mois en 2026)."},
                {"q": "Un non-cadre peut-il cotiser à une retraite complémentaire ?", "a": "Oui, tous les salariés du privé cotisent à l'AGIRC-ARRCO. Les non-cadres cotisent principalement sur la tranche 1 (jusqu'au plafond SS)."},
                {"q": "Quelle est la différence entre employé et ouvrier ?", "a": "Ces catégories sont des distinctions historiques. Depuis la fusion AGIRC-ARRCO en 2019, les cotisations sont identiques pour tous les non-cadres."},
                {"q": "Le salaire net non-cadre est-il toujours supérieur au net cadre ?", "a": "Pour un même brut, oui : un non-cadre touche quelques euros de plus en net car il ne paie pas la CET (0,14%). La différence est faible sous le plafond SS."},
                {"q": "Comment vérifier mes cotisations sur ma fiche de paie ?", "a": "Additionnez toutes les cotisations salariales listées. Le total devrait représenter environ 22% de votre brut si vous êtes non-cadre."},
            ])
            p["examples"] = generate_examples([
                {"name": "Julie, 28 ans", "situation": "Assistante administrative", "brut": "2 200 €", "net": "1 716 €", "net_apres_impot": "1 612 €"},
                {"name": "Thomas, 35 ans", "situation": "Technicien maintenance", "brut": "2 800 €", "net": "2 184 €", "net_apres_impot": "2 023 €"},
                {"name": "Emma, 42 ans", "situation": "Agent logistique", "brut": "2 000 €", "net": "1 560 €", "net_apres_impot": "1 488 €"},
            ])
        else:
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 3500], "non-cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Comment calculer mon salaire net ?", "a": "Utilisez notre calculateur ci-dessus ou appliquez un coefficient de 0,78 à votre brut mensuel pour une estimation rapide."},
                {"q": "Les cotisations sont-elles les mêmes partout en France ?", "a": "Oui, les cotisations de Sécurité sociale sont nationales. Seules certaines mutuelles d'entreprise peuvent varier."},
                {"q": "Puis-je négocier mon salaire brut ?", "a": "Oui, le salaire brut est négociable lors de l'embauche ou lors des entretiens annuels. Préparez vos arguments et renseignez-vous sur les salaires du marché."},
                {"q": "Que signifie le plafond de la Sécurité sociale ?", "a": "C'est un seuil (3 864 € par mois en 2026) au-delà duquel certaines cotisations changent de taux ou ne s'appliquent plus."},
                {"q": "Le salaire net est-il le montant versé sur mon compte ?", "a": "Le net avant impôt est affiché sur votre fiche de paie. Le montant réel versé est le net après prélèvement à la source."},
            ])
            p["examples"] = ""
    
    for p in pages:
        html = page_head(p["title"], p["desc"], f'{BASE_URL}/{p["slug"]}/', p["kw"])
        html += HEADER
        html += breadcrumb(p["h1"].replace('<span class="text-brand-600">', '').replace('</span>', ''))
        html += f'''
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 mb-6">{p["h1"]}</h1>
            </div>
        </section>'''
        html += calculator_widget(2500, p["statut_default"], "brut")
        html += f'''
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>'''
        if "table" in p and p["table"]:
            html += f'''
        <section class="py-12 px-4 bg-slate-50">
            <div class="mx-auto max-w-4xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6">Tableau de conversion brut → net</h2>
                {p["table"]}
            </div>
        </section>'''
        if "examples" in p and p["examples"]:
            html += f'''
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl">
                {p["examples"]}
            </div>
        </section>'''
        if "faqs" in p and p["faqs"]:
            html += p["faqs"]
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\n</body></html>"
        write_page(p["slug"], html)


# ── 2. Pages par période ──────────────────────────────────────────────────────

def gen_period_pages():
    pages = [
        {
            "slug": "salaire-brut-net-mensuel",
            "title": "Salaire Brut Net Mensuel 2026 : Calcul Mois par Mois",
            "desc": "Convertissez votre salaire brut mensuel en net en 2026. Cotisations salariales détaillées mois par mois, cadre et non-cadre. Calculateur gratuit instantané.",
            "kw": "salaire brut net mensuel, brut en net par mois, calcul salaire mensuel",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Mensuel</span> 2026",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul mensuel du salaire brut en net</h2>
                <p>Le <strong>salaire brut mensuel</strong> est le montant le plus couramment utilisé dans les contrats de travail et les fiches de paie en France. C'est la base de référence pour calculer vos cotisations et votre salaire net.</p>
                <p>Pour convertir votre brut mensuel en net, il faut déduire environ <strong>22% de cotisations salariales</strong> (non-cadre) ou <strong>25%</strong> (cadre). Le montant exact dépend de votre niveau de salaire par rapport au <strong>plafond de la Sécurité sociale</strong> (3 864 €/mois en 2026).</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Tableau rapide brut → net mensuel</h3>
                <ul>
                    <li><a href="/1500-euros-brut-en-net/" class="text-brand-600">1 500 € brut/mois</a> → ~1 170 € net</li>
                    <li><a href="/2000-euros-brut-en-net/" class="text-brand-600">2 000 € brut/mois</a> → ~1 560 € net</li>
                    <li><a href="/2500-euros-brut-en-net/" class="text-brand-600">2 500 € brut/mois</a> → ~1 950 € net</li>
                    <li><a href="/3000-euros-brut-en-net/" class="text-brand-600">3 000 € brut/mois</a> → ~2 340 € net</li>
                    <li><a href="/4000-euros-brut-en-net/" class="text-brand-600">4 000 € brut/mois</a> → ~3 120 € net</li>
                    <li><a href="/5000-euros-brut-en-net/" class="text-brand-600">5 000 € brut/mois</a> → ~3 900 € net</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Formules de conversion détaillées</h2>
                <p>Pour convertir précisément votre <strong>salaire brut mensuel en net</strong>, vous devez appliquer les taux de cotisations sociales en vigueur. Ces taux varient selon votre statut professionnel et votre niveau de rémunération.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Formule pour un non-cadre</h3>
                <p>Pour un salarié <a href="/salaire-brut-net-non-cadre/" class="text-brand-600 hover:text-brand-700">non-cadre</a> gagnant moins de 3 864 € brut mensuel (plafond de la Sécurité sociale) :</p>
                <ul>
                    <li><strong>Salaire net avant impôt</strong> = Salaire brut × 0,78</li>
                    <li>Taux de cotisations salariales : environ <strong>22%</strong></li>
                </ul>
                <p>Exemple : 2 500 € brut × 0,78 = <strong>1 950 € net avant impôt</strong></p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Formule pour un cadre</h3>
                <p>Pour un salarié <a href="/salaire-brut-net-cadre/" class="text-brand-600 hover:text-brand-700">cadre</a>, le taux de cotisations est légèrement plus élevé en raison de la CET (Contribution d'Équilibre Technique) :</p>
                <ul>
                    <li><strong>Salaire net avant impôt</strong> = Salaire brut × 0,76 (pour les salaires sous le plafond SS)</li>
                    <li>Taux de cotisations salariales : environ <strong>24%</strong></li>
                </ul>
                <p>Pour les salaires au-delà du plafond SS (3 864 € par mois), le coefficient se rapproche de 0,78 car certaines cotisations ne s'appliquent plus sur la part excédentaire.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cas pratiques avec exemples chiffrés</h2>
                <p>Voici des cas concrets de conversion brut/net mensuel pour différents profils professionnels :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cas 1 : Employé au SMIC</h3>
                <p>Un salarié au <a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC</a> en 2026 :</p>
                <ul>
                    <li>Salaire brut mensuel : <strong>1 801,80 €</strong></li>
                    <li>Cotisations salariales (environ 21,5%) : -387,39 €</li>
                    <li>Salaire net avant impôt : <strong>1 414,41 €</strong></li>
                    <li>Après prélèvement à la source (taux 0% sous conditions) : <strong>1 414,41 €</strong></li>
                </ul>
                <p>Note : les salariés au SMIC bénéficient d'une légère réduction du taux de cotisations (environ 21,5% au lieu de 22%).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cas 2 : Technicien non-cadre à 2 800 € brut</h3>
                <ul>
                    <li>Salaire brut mensuel : <strong>2 800 €</strong></li>
                    <li>Cotisations salariales (22%) : -616 €</li>
                    <li>Salaire net avant impôt : <strong>2 184 €</strong></li>
                    <li>Prélèvement à la source (taux estimé 3,5%) : -76,44 €</li>
                    <li>Salaire net après impôt : <strong>2 107,56 €</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cas 3 : Cadre à 4 500 € brut (au-dessus du plafond SS)</h3>
                <ul>
                    <li>Salaire brut mensuel : <strong>4 500 €</strong></li>
                    <li>Cotisations sur tranche 1 (jusqu'à 3 864 €) : -926,40 €</li>
                    <li>Cotisations sur tranche 2 (au-delà de 3 864 €) : -125,88 €</li>
                    <li>Salaire net avant impôt : <strong>3 447,72 €</strong></li>
                    <li>Prélèvement à la source (taux estimé 7,5%) : -258,58 €</li>
                    <li>Salaire net après impôt : <strong>3 189,14 €</strong></li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Pièges à éviter dans le calcul mensuel</h2>
                <p>Attention à ces erreurs courantes lors de la conversion brut/net mensuel :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Le 13ème mois n'est pas inclus dans le mensuel</h3>
                <p>Beaucoup de contrats prévoient un <strong>13ème mois</strong> (prime annuelle équivalant à un mois de salaire). Cette prime s'ajoute aux 12 mois de salaire habituel et n'est pas incluse dans le brut mensuel affiché sur votre <a href="/lire-fiche-de-paie/" class="text-brand-600 hover:text-brand-700">fiche de paie</a>.</p>
                <p>Si vous avez un 13ème mois, votre rémunération annuelle réelle est :<br>
                <strong>Revenu annuel total = (Brut mensuel × 12) + 13ème mois</strong></p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Les primes variables ne sont pas toujours incluses</h3>
                <p>Certaines primes sont versées mensuellement (prime de panier, prime d'ancienneté) et s'ajoutent au brut mensuel. D'autres sont versées ponctuellement (prime de performance, participation, intéressement) et ne figurent pas dans le salaire mensuel régulier.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Les heures supplémentaires modifient le brut mensuel</h3>
                <p>Les <strong>heures supplémentaires</strong> augmentent votre brut mensuel (majoration de 25% ou 50%) et sont exonérées d'impôt sur le revenu dans la limite de 7 500 € par an. Elles sont cependant soumises aux cotisations sociales normales.</p>
                <p>Exemple : un salarié à 2 000 € brut effectuant 10 heures supplémentaires (majoration 25%) :</p>
                <ul>
                    <li>Taux horaire : 2 000 / 151,67 = 13,18 €/h</li>
                    <li>Heures sup : 10 h × 13,18 × 1,25 = 164,75 €</li>
                    <li>Brut total du mois : 2 000 + 164,75 = <strong>2 164,75 €</strong></li>
                    <li>Net : environ 1 688 € (au lieu de 1 560 €)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Confusion entre net avant impôt et net à payer</h3>
                <p>Sur votre fiche de paie, vous verrez deux montants nets :</p>
                <ul>
                    <li><strong>Net avant prélèvement à la source</strong> : salaire net après cotisations sociales mais avant impôt</li>
                    <li><strong>Net à payer</strong> : montant réellement versé sur votre compte après déduction du prélèvement à la source</li>
                </ul>
                <p>Pour mieux comprendre ces différences, consultez notre guide sur <a href="/difference-salaire-brut-net/" class="text-brand-600 hover:text-brand-700">la différence entre salaire brut et net</a>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Évolution du salaire mensuel au cours de la carrière</h2>
                <p>Le salaire brut mensuel évolue tout au long de votre carrière professionnelle. Selon l'INSEE, un salarié français voit son salaire augmenter en moyenne de :</p>
                <ul>
                    <li><strong>+3 à 5% par an</strong> en début de carrière (0-5 ans d'expérience)</li>
                    <li><strong>+2 à 3% par an</strong> en milieu de carrière (5-20 ans)</li>
                    <li><strong>+1 à 2% par an</strong> en fin de carrière (au-delà de 20 ans)</li>
                </ul>
                <p>Ces augmentations proviennent de plusieurs sources : l'ancienneté, les promotions, le changement d'entreprise, l'acquisition de nouvelles compétences et la revalorisation annuelle des salaires dans la convention collective.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Négocier son salaire mensuel</h3>
                <p>Les meilleurs moments pour <a href="/negocier-salaire/" class="text-brand-600 hover:text-brand-700">négocier votre salaire mensuel</a> sont :</p>
                <ul>
                    <li><strong>Lors de l'embauche</strong> : c'est le moment où vous avez le plus de levier de négociation</li>
                    <li><strong>Entretien annuel d'évaluation</strong> : préparez des arguments chiffrés (résultats, responsabilités accrues)</li>
                    <li><strong>Après une formation qualifiante</strong> ou l'obtention d'une certification</li>
                    <li><strong>Lors d'un changement de poste</strong> en interne (promotion, mobilité)</li>
                    <li><strong>Après une offre externe</strong> : si un concurrent vous fait une proposition, vous pouvez en informer votre employeur pour renégocier</li>
                </ul>
                <p>Conseil : raisonnez toujours en <strong>salaire brut</strong> lors des négociations, car c'est la référence légale. Le passage au net se fait automatiquement selon les <a href="/cotisations-sociales-salariales/" class="text-brand-600 hover:text-brand-700">cotisations en vigueur</a>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le salaire mensuel et les mois courts ou longs</h2>
                <p>Une question fréquente : le salaire mensuel varie-t-il selon le nombre de jours dans le mois ? La réponse est <strong>non</strong>. Le salaire brut mensuel reste identique, que le mois comporte 28, 30 ou 31 jours.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Principe du lissage mensuel</h3>
                <p>Le salaire mensuel est calculé sur une base annuelle lissée sur 12 mois. Ainsi, vous percevez le même montant en février (28 ou 29 jours) qu'en mars (31 jours), même si le nombre de jours ouvrés diffère.</p>
                <p>Ce lissage est avantageux pour le salarié car il garantit une <strong>rémunération stable et prévisible</strong> chaque mois, indépendamment du calendrier.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exception : entrée ou sortie en cours de mois</h3>
                <p>Si vous arrivez ou quittez l'entreprise en cours de mois, votre salaire est alors calculé <strong>au prorata</strong> des jours travaillés :</p>
                <ul>
                    <li><strong>Salaire au prorata = (Salaire mensuel / Nombre de jours dans le mois) × Jours travaillés</strong></li>
                </ul>
                <p>Exemple : vous commencez le 15 mars (mois de 31 jours) avec un salaire de 2 500 € brut :</p>
                <ul>
                    <li>Nombre de jours travaillés : 17 jours (du 15 au 31 mars)</li>
                    <li>Salaire prorata : (2 500 / 31) × 17 = <strong>1 370 € brut</strong></li>
                </ul>
                <p>Cette règle s'appliqué aussi en cas d'absence non rémunérée (congé sans solde, grève) : le salaire est réduit au prorata des jours d'absence.</p>
            """
        },
        {
            "slug": "salaire-brut-net-annuel",
            "title": "Salaire Brut Net Annuel 2026 : Conversion Année Complète",
            "desc": "Convertissez votre salaire brut annuel en net annuel en 2026. Calculateur gratuit avec détail des cotisations salariales sur 12 mois, cadre et non-cadre.",
            "kw": "salaire brut net annuel, brut en net par an, salaire annuel net, conversion annuelle",
            "h1": "Salaire Brut Net <span class=\"text-brand-600\">Annuel</span> 2026",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Du brut annuel au net annuel</h2>
                <p>Le <strong>salaire brut annuel</strong> est souvent mentionné dans les offres d'emploi et les contrats de travail. Pour obtenir votre net annuel, divisez par 12 pour obtenir le brut mensuel, puis appliquez les cotisations.</p>
                <p>La formule rapide : <strong>net annuel ≈ brut annuel × 0,78</strong> (non-cadre) ou <strong>× 0,75</strong> (cadre).</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de conversion annuelle</h3>
                <ul>
                    <li><strong>20 000 € brut/an</strong> → ~15 600 € net/an (~1 300 €/mois)</li>
                    <li><strong>25 000 € brut/an</strong> → ~19 500 € net/an (~1 625 €/mois)</li>
                    <li><strong>30 000 € brut/an</strong> → ~23 400 € net/an (~1 950 €/mois)</li>
                    <li><strong>35 000 € brut/an</strong> → ~27 300 € net/an (~2 275 €/mois)</li>
                    <li><strong>40 000 € brut/an</strong> → ~31 200 € net/an (~2 600 €/mois)</li>
                    <li><strong>50 000 € brut/an</strong> → ~39 000 € net/an (~3 250 €/mois)</li>
                </ul>
                <p>Attention : ces montants sont des estimations. Le calcul exact dépend de votre statut et du plafond de la Sécurité sociale.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Pourquoi raisonner en salaire annuel ?</h2>
                <p>De plus en plus d'offres d'emploi affichent le salaire en <strong>brut annuel</strong> plutôt qu'en mensuel. Cette pratique, importée des pays anglo-saxons, présente plusieurs avantages :</p>
                <ul>
                    <li><strong>Comparaison facilitée</strong> : le brut annuel permet de comparer directement des offres sans se préoccuper du nombre de mois de salaire (12, 13 ou 14 mois)</li>
                    <li><strong>Vision globale</strong> : il intègre les primes annuelles et permet d'avoir une vue d'ensemble de votre rémunération</li>
                    <li><strong>Norme internationale</strong> : pour les entreprises multinationales, le brut annuel facilite les comparaisons entre pays</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Passer du brut annuel au mensuel</h3>
                <p>Pour obtenir votre <strong>salaire brut mensuel</strong> à partir du brut annuel, divisez simplement par 12 :</p>
                <p><strong>Brut mensuel = Brut annuel / 12</strong></p>
                <p>Exemples concrets :</p>
                <ul>
                    <li>30 000 € brut/an ÷ 12 = <strong>2 500 € brut/mois</strong></li>
                    <li>45 000 € brut/an ÷ 12 = <strong>3 750 € brut/mois</strong></li>
                    <li>60 000 € brut/an ÷ 12 = <strong>5 000 € brut/mois</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Attention au 13ème mois dans le calcul annuel</h3>
                <p>Si votre contrat prévoit un <strong>13ème mois</strong>, il faut distinguer deux cas :</p>
                <p><strong>Cas 1 : Le 13ème mois est inclus dans le brut annuel</strong><br>
                Le brut mensuel réel = Brut annuel / 13</p>
                <p>Exemple : 39 000 € brut/an (incluant 13ème mois) ÷ 13 = <strong>3 000 € brut/mois</strong></p>
                <p><strong>Cas 2 : Le 13ème mois s'ajoute au brut annuel</strong><br>
                Brut annuel total = (Brut annuel affiché × 13) / 12</p>
                <p>Exemple : 36 000 € brut/an sur 12 mois + 13ème mois de 3 000 € = <strong>39 000 € brut annuel total</strong></p>
                <p>Conseil : clarifiez toujours ce point lors de l'entretien d'embauche pour éviter les mauvaises surprises.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du net annuel imposable</h2>
                <p>Le <strong>salaire net imposable</strong> (ou net fiscal) diffère du net à payer qui figure sur votre bulletin de paie. Il sert de base au calcul de votre impôt sur le revenu et du prélèvement à la source.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Formule du net imposable</h3>
                <p>Net imposable = Brut annuel - Cotisations déductibles (Sécurité sociale, retraite, chômage) - CSG déductible (6,80%)</p>
                <p>La CSG non déductible (2,40%) et la CRDS (0,50%) sont <strong>réintégrées</strong> dans le net imposable.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple de calcul pour 30 000 € brut annuel</h3>
                <ul>
                    <li>Brut annuel : 30 000 €</li>
                    <li>Cotisations déductibles (environ 14%) : -4 200 €</li>
                    <li>CSG déductible (6,80% sur 98,25% du brut) : -2 000 €</li>
                    <li>Net avant impôt : 23 400 €</li>
                    <li>Réintégration CSG non déductible + CRDS (2,90% sur 98,25%) : +859 €</li>
                    <li><strong>Net imposable annuel : 24 259 €</strong></li>
                </ul>
                <p>C'est sur ce montant de 24 259 € que sera calculé votre impôt sur le revenu (après application d'un abattement forfaitaire de 10% pour frais professionnels).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaires annuels par secteur d'activité en 2026</h2>
                <p>Selon les statistiques de l'INSEE et les études de rémunération, voici les <a href="/salaire-moyen-france/" class="text-brand-600 hover:text-brand-700">salaires moyens annuels bruts</a> par secteur en France :</p>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Secteur</th>
                            <th class="border border-slate-300 px-4 py-2">Brut annuel moyen</th>
                            <th class="border border-slate-300 px-4 py-2">Net annuel moyen</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2">Informatique / Tech</td><td class="border border-slate-300 px-4 py-2">45 000 €</td><td class="border border-slate-300 px-4 py-2">35 100 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Banque / Finance</td><td class="border border-slate-300 px-4 py-2">52 000 €</td><td class="border border-slate-300 px-4 py-2">40 560 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Ingénierie</td><td class="border border-slate-300 px-4 py-2">48 000 €</td><td class="border border-slate-300 px-4 py-2">37 440 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Commerce / Vente</td><td class="border border-slate-300 px-4 py-2">32 000 €</td><td class="border border-slate-300 px-4 py-2">24 960 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Santé (hors médecins)</td><td class="border border-slate-300 px-4 py-2">35 000 €</td><td class="border border-slate-300 px-4 py-2">27 300 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Enseignement</td><td class="border border-slate-300 px-4 py-2">33 000 €</td><td class="border border-slate-300 px-4 py-2">25 740 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">Hôtellerie / Restauration</td><td class="border border-slate-300 px-4 py-2">26 000 €</td><td class="border border-slate-300 px-4 py-2">20 280 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">BTP</td><td class="border border-slate-300 px-4 py-2">30 000 €</td><td class="border border-slate-300 px-4 py-2">23 400 €</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Ces chiffres sont des moyennes nationales. Les salaires peuvent varier considérablement selon la région (Paris vs province), la taille de l'entreprise et le niveau d'expérience.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Évolution du salaire annuel selon l'expérience</h2>
                <p>Le salaire annuel augmente généralement de façon significative avec l'expérience. Voici une projection typique pour un profil cadre dans le secteur tertiaire :</p>
                <ul>
                    <li><strong>0-2 ans d'expérience</strong> : 28 000 - 35 000 € brut/an</li>
                    <li><strong>3-5 ans</strong> : 35 000 - 45 000 € brut/an</li>
                    <li><strong>6-10 ans</strong> : 45 000 - 60 000 € brut/an</li>
                    <li><strong>11-15 ans</strong> : 60 000 - 80 000 € brut/an</li>
                    <li><strong>15+ ans (manager senior)</strong> : 80 000 - 120 000 € brut/an</li>
                </ul>
                <p>Les sauts salariaux les plus importants se produisent lors des <strong>changements d'entreprise</strong> : en moyenne, changer d'employeur permet d'augmenter son salaire de 10 à 20%, contre 3 à 5% en restant dans la même entreprise.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Impact du statut sur le salaire annuel</h3>
                <p>Le statut professionnel influence le salaire annuel moyen :</p>
                <ul>
                    <li><strong>Cadres</strong> : salaire moyen de 55 000 € brut/an (médiane : 48 000 €)</li>
                    <li><strong>Professions intermédiaires</strong> : 33 000 € brut/an (techniciens, agents de maîtrise)</li>
                    <li><strong>Employés</strong> : 26 000 € brut/an</li>
                    <li><strong>Ouvriers</strong> : 27 000 € brut/an</li>
                </ul>
                <p>Pour mieux comprendre ces différences, consultez nos pages sur le <a href="/salaire-brut-net-cadre/" class="text-brand-600 hover:text-brand-700">salaire brut net cadre</a> et <a href="/salaire-brut-net-non-cadre/" class="text-brand-600 hover:text-brand-700">non-cadre</a>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Optimiser son salaire annuel</h2>
                <p>Pour maximiser votre salaire annuel net, plusieurs leviers existent :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Avantages en nature et frais professionnels</h3>
                <p>Certains avantages sont plus intéressants qu'une augmentation de salaire brut :</p>
                <ul>
                    <li><strong>Véhicule de fonction</strong> : économie de 3 000 à 8 000 € par an (selon usage privé toléré)</li>
                    <li><strong>Téléphone professionnel</strong> : économie de 500 à 1 000 € par an</li>
                    <li><strong>Tickets restaurant</strong> : gain net de 600 à 1 200 € par an (part employeur exonérée)</li>
                    <li><strong>Remboursement des frais de transport</strong> : 50% du pass Navigo = 420 € par an</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Épargne salariale</h3>
                <p>L'intéressement et la participation sont <strong>exonérés de cotisations sociales</strong> et d'impôt sur le revenu s'ils sont placés sur un PEE ou PER. Un salarié peut ainsi recevoir 2 000 à 5 000 € par an en plus de son salaire, sans payer de charges.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Heures supplémentaires défiscalisées</h3>
                <p>Les heures supplémentaires sont <strong>exonérées d'impôt sur le revenu</strong> dans la limite de 7 500 € par an. Pour un salarié dans la tranche d'imposition à 30%, cela représente une économie de 2 250 € d'impôt.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Négociation lors du changement d'emploi</h3>
                <p>Le moment le plus propice pour augmenter significativement son salaire annuel est lors d'un <strong>changement d'employeur</strong>. N'hésitez pas à demander 10 à 20% de plus que votre salaire actuel, en vous appuyant sur les grilles salariales du marché.</p>
                <p>Pour préparer votre négociation, consultez notre guide pour <a href="/negocier-salaire/" class="text-brand-600 hover:text-brand-700">négocier efficacement son salaire</a>.</p>
            """
        },
        {
            "slug": "salaire-brut-net-horaire",
            "title": "Salaire Brut Net Horaire 2026 : Taux Horaire Brut en Net",
            "desc": "Convertissez votre taux horaire brut en net en 2026. Calcul sur base 35h/semaine, SMIC horaire à 11,88€ et simulateur gratuit avec résultat instantané.",
            "kw": "taux horaire brut net, salaire horaire brut en net, smic horaire net, brut en net heure",
            "h1": "Taux Horaire <span class=\"text-brand-600\">Brut Net</span> 2026",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Convertir un taux horaire brut en net</h2>
                <p>Pour convertir un <strong>taux horaire brut en net</strong>, la méthode est simple : appliquez le même coefficient que pour le salaire mensuel, soit environ <strong>×0,78</strong> (non-cadre) ou <strong>×0,75</strong> (cadre).</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Base de calcul</h3>
                <p>En France, la durée légale du travail est de <strong>35 heures par semaine</strong>, soit <strong>151,67 heures par mois</strong> (35h × 52 semaines / 12 mois). Pour passer du taux horaire au salaire mensuel : taux horaire × 151,67.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">SMIC horaire 2026</h3>
                <ul>
                    <li><strong>SMIC brut horaire</strong> : 11,88 €</li>
                    <li><strong>SMIC net horaire</strong> : ~9,27 € (non-cadre)</li>
                    <li><strong>SMIC mensuel brut</strong> : 1 801,80 €</li>
                    <li><strong>SMIC mensuel net</strong> : ~1 426 €</li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de taux horaires</h3>
                <ul>
                    <li><strong>12 € brut/h</strong> → ~9,36 € net/h → ~1 420 €/mois net</li>
                    <li><strong>15 € brut/h</strong> → ~11,70 € net/h → ~1 775 €/mois net</li>
                    <li><strong>20 € brut/h</strong> → ~15,60 € net/h → ~2 366 €/mois net</li>
                    <li><strong>25 € brut/h</strong> → ~19,50 € net/h → ~2 958 €/mois net</li>
                    <li><strong>30 € brut/h</strong> → ~23,40 € net/h → ~3 550 €/mois net</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Heures supplémentaires et majoration du taux horaire</h2>
                <p>Au-delà de la durée légale de 35h par semaine, les heures travaillées sont considérées comme des <strong>heures supplémentaires</strong> et donnent droit à une majoration du taux horaire :</p>
                <ul>
                    <li><strong>Les 8 premières heures sup (de la 36ème à la 43ème heure)</strong> : majoration de 25%</li>
                    <li><strong>Au-delà de 43h par semaine</strong> : majoration de 50%</li>
                </ul>
                <p>Exemple pour un taux horaire de 15 € brut :</p>
                <ul>
                    <li>Heures normales : 15 € brut/h → 11,70 € net/h</li>
                    <li>Heures sup à 25% : 15 × 1,25 = 18,75 € brut/h → 14,63 € net/h</li>
                    <li>Heures sup à 50% : 15 × 1,50 = 22,50 € brut/h → 17,55 € net/h</li>
                </ul>
                <p>Bonus fiscal : les heures supplémentaires sont <strong>exonérées d'impôt sur le revenu</strong> dans la limite de 7 500 € par an, ce qui rend leur taux horaire net encore plus avantageux.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du taux horaire à partir du mensuel</h2>
                <p>Si vous connaissez votre <a href="/salaire-brut-net-mensuel/" class="text-brand-600 hover:text-brand-700">salaire brut mensuel</a>, vous pouvez facilement calculer votre taux horaire brut :</p>
                <p><strong>Taux horaire brut = Salaire brut mensuel / 151,67</strong></p>
                <p>Le nombre 151,67 correspond au nombre d'heures travaillées par mois pour un temps plein (35h × 52 semaines / 12 mois).</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de conversion mensuel → horaire</h3>
                <ul>
                    <li><a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC</a> 1 801,80 € / 151,67 = <strong>11,88 € brut/h</strong></li>
                    <li>2 500 € brut/mois / 151,67 = <strong>16,48 € brut/h</strong></li>
                    <li>3 000 € brut/mois / 151,67 = <strong>19,78 € brut/h</strong></li>
                    <li>4 000 € brut/mois / 151,67 = <strong>26,37 € brut/h</strong></li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux horaire net et pouvoir d'achat</h2>
                <p>Connaître son taux horaire net permet de mieux évaluer le <strong>coût horaire de votre temps</strong> et de prendre des décisions éclairées (accepter ou refuser des heures supplémentaires, arbitrer entre temps libre et revenus).</p>
                <p>Pour un salarié au SMIC net (9,27 €/h), une heure de travail permet d'acheter :</p>
                <ul>
                    <li>2 baguettes de pain (environ 1 € chacune)</li>
                    <li>1 ticket de cinéma (environ 10 €)</li>
                    <li>1,5 litres d'essence (environ 1,80 €/L)</li>
                </ul>
                <p>Pour un cadre à 25 €/h net, une heure permet d'acheter environ 2,7 fois plus.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux horaire par secteur d'activité en 2026</h2>
                <p>Le taux horaire brut varie considérablement selon le secteur d'activité et le niveau de qualification. Voici un aperçu des <strong>taux horaires moyens</strong> pratiqués dans différents secteurs :</p>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Secteur</th>
                            <th class="border border-slate-300 px-4 py-2">Taux horaire brut moyen</th>
                            <th class="border border-slate-300 px-4 py-2">Taux horaire net moyen</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Restauration / Hôtellerie</strong></td><td class="border border-slate-300 px-4 py-2">11,88 - 15 €</td><td class="border border-slate-300 px-4 py-2">9,27 - 11,70 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>BTP / Artisanat</strong></td><td class="border border-slate-300 px-4 py-2">14 - 18 €</td><td class="border border-slate-300 px-4 py-2">10,92 - 14,04 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Commerce / Vente</strong></td><td class="border border-slate-300 px-4 py-2">12 - 16 €</td><td class="border border-slate-300 px-4 py-2">9,36 - 12,48 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Santé / Social</strong></td><td class="border border-slate-300 px-4 py-2">15 - 22 €</td><td class="border border-slate-300 px-4 py-2">11,70 - 17,16 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Informatique / Tech</strong></td><td class="border border-slate-300 px-4 py-2">20 - 35 €</td><td class="border border-slate-300 px-4 py-2">15,60 - 27,30 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Finance / Assurance</strong></td><td class="border border-slate-300 px-4 py-2">25 - 40 €</td><td class="border border-slate-300 px-4 py-2">19,50 - 31,20 €</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Ces fourchettes sont indicatives et peuvent varier selon l'expérience, la région et la taille de l'entreprise. Les métiers spécialisés ou en tension (développeurs, ingénieurs, professions médicales) bénéficient généralement de taux horaires plus élevés.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux horaire et temps partiel</h2>
                <p>Le <strong>taux horaire reste identique</strong> que vous travailliez à temps plein ou à temps partiel. Seul le nombre d'heures travaillées change, ce qui modifié votre salaire mensuel total.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul du salaire mensuel à temps partiel</h3>
                <p>Pour calculer votre salaire mensuel à temps partiel, multipliez votre taux horaire par le nombre d'heures mensuelles correspondant à votre quotité de travail :</p>
                <ul>
                    <li><strong>80% (28h/semaine)</strong> : 121,33 heures/mois (28 × 52 / 12)</li>
                    <li><strong>60% (21h/semaine)</strong> : 91 heures/mois (21 × 52 / 12)</li>
                    <li><strong>50% (17,5h/semaine)</strong> : 75,83 heures/mois (17,5 × 52 / 12)</li>
                </ul>
                <p>Exemple pour un taux horaire de 16 € brut :</p>
                <ul>
                    <li>Temps plein (35h) : 16 × 151,67 = <strong>2 427 € brut/mois</strong></li>
                    <li>80% : 16 × 121,33 = <strong>1 941 € brut/mois</strong></li>
                    <li>60% : 16 × 91 = <strong>1 456 € brut/mois</strong></li>
                    <li>50% : 16 × 75,83 = <strong>1 213 € brut/mois</strong></li>
                </ul>
                <p>Avantage du temps partiel : vous conservez tous vos droits sociaux (congés payés, mutuelle, retraite) au prorata de votre temps de travail.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Évolution du taux horaire au fil de la carrière</h2>
                <p>Le taux horaire brut augmente naturellement avec l'expérience et l'ancienneté. Voici une projection type de l'évolution du taux horaire selon l'âge et l'expérience professionnelle :</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Évolution type pour un profil non-cadre</h3>
                <ul>
                    <li><strong>18-22 ans (débutant)</strong> : 11,88 - 13 €/h (SMIC à légèrement au-dessus)</li>
                    <li><strong>23-30 ans (junior, 1-5 ans d'expérience)</strong> : 13 - 17 €/h</li>
                    <li><strong>31-40 ans (confirmé, 5-15 ans d'expérience)</strong> : 17 - 22 €/h</li>
                    <li><strong>41-55 ans (senior, 15+ ans d'expérience)</strong> : 20 - 25 €/h</li>
                    <li><strong>55+ ans (expert)</strong> : 23 - 28 €/h</li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Évolution type pour un profil cadre</h3>
                <ul>
                    <li><strong>23-27 ans (jeune diplômé)</strong> : 18 - 22 €/h</li>
                    <li><strong>28-35 ans (junior/confirmé)</strong> : 22 - 30 €/h</li>
                    <li><strong>36-45 ans (senior)</strong> : 30 - 40 €/h</li>
                    <li><strong>46-60 ans (expert/manager)</strong> : 40 - 60 €/h</li>
                </ul>
                <p>Ces progressions peuvent être accélérées par des changements d'entreprise, des promotions, l'acquisition de compétences rares ou une <a href="/negocier-salaire/" class="text-brand-600 hover:text-brand-700">négociation salariale</a> bien menée.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Convertir entre taux horaire net et annuel</h2>
                <p>Pour passer facilement d'un <strong>taux horaire net</strong> à un <strong>salaire annuel net</strong> et inversement, voici les formules de conversion :</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Du taux horaire net au salaire annuel net</h3>
                <p><strong>Salaire annuel net = Taux horaire net × 1 820</strong></p>
                <p>Le nombre 1 820 correspond aux heures travaillées par an pour un temps plein (151,67 heures/mois × 12 mois ≈ 1 820 heures/an).</p>
                <p>Exemples :</p>
                <ul>
                    <li>10 €/h net → 10 × 1 820 = <strong>18 200 € net/an</strong></li>
                    <li>15 €/h net → 15 × 1 820 = <strong>27 300 € net/an</strong></li>
                    <li>20 €/h net → 20 × 1 820 = <strong>36 400 € net/an</strong></li>
                    <li>25 €/h net → 25 × 1 820 = <strong>45 500 € net/an</strong></li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Du salaire annuel net au taux horaire net</h3>
                <p><strong>Taux horaire net = Salaire annuel net / 1 820</strong></p>
                <p>Exemples :</p>
                <ul>
                    <li>20 000 € net/an / 1 820 = <strong>10,99 €/h net</strong></li>
                    <li>30 000 € net/an / 1 820 = <strong>16,48 €/h net</strong></li>
                    <li>40 000 € net/an / 1 820 = <strong>21,98 €/h net</strong></li>
                    <li>50 000 € net/an / 1 820 = <strong>27,47 €/h net</strong></li>
                </ul>
                <p>Cette conversion est particulièrement utile pour comparer des offres d'emploi exprimées en annuel avec votre taux horaire actuel, ou pour évaluer l'impact d'une <a href="/salaire-brut-net-annuel/" class="text-brand-600 hover:text-brand-700">augmentation annuelle</a> sur votre taux horaire effectif.</p>
            """
        },
        {
            "slug": "salaire-brut-net-journalier",
            "title": "Salaire Brut Net Journalier 2026 : Calcul par Jour",
            "desc": "Convertissez votre salaire brut journalier en net en 2026. Calcul sur base 7h/jour ou 151,67h/mois, TJM freelance et simulateur gratuit. Résultat instantané.",
            "kw": "salaire journalier brut net, TJM brut net, taux journalier net, salaire par jour",
            "h1": "Salaire <span class=\"text-brand-600\">Journalier</span> Brut Net 2026",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du salaire journalier brut en net</h2>
                <p>Le <strong>salaire journalier</strong> se calcule sur une base de <strong>7 heures par jour</strong> (35h / 5 jours). Il y a en moyenne <strong>21,67 jours ouvrés par mois</strong> (260 jours / 12 mois).</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Formule de conversion</h3>
                <ul>
                    <li>Salaire mensuel = Taux journalier × 21,67</li>
                    <li>Taux journalier = Salaire mensuel / 21,67</li>
                    <li>Net journalier ≈ Brut journalier × 0,78 (non-cadre)</li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples</h3>
                <ul>
                    <li><strong>100 € brut/jour</strong> → ~78 € net/jour → ~2 167 € brut/mois</li>
                    <li><strong>150 € brut/jour</strong> → ~117 € net/jour → ~3 250 € brut/mois</li>
                    <li><strong>200 € brut/jour</strong> → ~156 € net/jour → ~4 334 € brut/mois</li>
                    <li><strong>300 € brut/jour</strong> → ~234 € net/jour → ~6 501 € brut/mois</li>
                    <li><strong>500 € brut/jour</strong> → ~390 € net/jour → ~10 835 € brut/mois</li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">TJM Freelance</h3>
                <p>Attention : le TJM (Taux Journalier Moyen) d'un freelance ne se convertit pas de la même façon. Un freelance doit prendre en compte ses charges sociales (environ 22-45% selon le statut), ses congés non payés et ses frais professionnels.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">TJM Freelance : calcul du revenu réel</h2>
                <p>Le <strong>TJM</strong> (Taux Journalier Moyen) est la référence pour les consultants indépendants, freelances et auto-entrepreneurs. Contrairement au salaire journalier d'un salarié, le TJM doit couvrir non seulement votre rémunération, mais aussi vos charges, congés et période d'intermission.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Formule de calcul du TJM nécessaire</h3>
                <p>Pour déterminer le TJM minimum permettant de viser un revenu net équivalent à un salaire :</p>
                <p><strong>TJM = (Salaire mensuel visé × 12 × 1,5) / (Nombre de jours facturables par an)</strong></p>
                <p>Le coefficient 1,5 prend en compte :</p>
                <ul>
                    <li>Les <a href="/cotisations-sociales-salariales/" class="text-brand-600 hover:text-brand-700">charges sociales</a> (22 à 45% selon le statut)</li>
                    <li>Les congés non payés (environ 25 jours/an)</li>
                    <li>Les périodes sans mission (environ 20-40 jours/an)</li>
                    <li>Les frais professionnels (comptable, assurance, matériel)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple concret</h3>
                <p>Un consultant souhaitant l'équivalent de 3 000 € net mensuel en salariat :</p>
                <ul>
                    <li>Objectif annuel : 3 000 × 12 = 36 000 € net</li>
                    <li>Chiffre d'affaires nécessaire : 36 000 × 1,5 = 54 000 €</li>
                    <li>Jours facturables : environ 180 jours/an (hypothèse prudente)</li>
                    <li><strong>TJM minimum : 54 000 / 180 = 300 €/jour</strong></li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparaison salaire journalier salarié vs TJM freelance</h2>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Critère</th>
                            <th class="border border-slate-300 px-4 py-2">Salarié</th>
                            <th class="border border-slate-300 px-4 py-2">Freelance</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Jours travaillés/an</strong></td><td class="border border-slate-300 px-4 py-2">~218 jours (RTT inclus)</td><td class="border border-slate-300 px-4 py-2">~180 jours facturés</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Congés payés</strong></td><td class="border border-slate-300 px-4 py-2">Oui (payés)</td><td class="border border-slate-300 px-4 py-2">Non (à provisionner)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Charges sociales</strong></td><td class="border border-slate-300 px-4 py-2">~22% (salarié)</td><td class="border border-slate-300 px-4 py-2">22-45% (selon statut)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Assurance chômage</strong></td><td class="border border-slate-300 px-4 py-2">Oui</td><td class="border border-slate-300 px-4 py-2">Non (sauf ATI)</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2"><strong>Frais professionnels</strong></td><td class="border border-slate-300 px-4 py-2">Pris en charge</td><td class="border border-slate-300 px-4 py-2">À votre charge</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Grilles de TJM par secteur et expérience</h2>
                <p>Voici des fourchettes indicatives de TJM pratiqués en France en 2026 :</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Développement informatique</h3>
                <ul>
                    <li>Junior (0-3 ans) : 250-400 €/jour</li>
                    <li>Confirmé (3-7 ans) : 400-600 €/jour</li>
                    <li>Senior (7+ ans) : 600-900 €/jour</li>
                    <li>Expert/Architecte : 800-1 200 €/jour</li>
                </ul>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Conseil en management</h3>
                <ul>
                    <li>Consultant junior : 300-500 €/jour</li>
                    <li>Consultant confirmé : 500-800 €/jour</li>
                    <li>Consultant senior : 800-1 200 €/jour</li>
                </ul>
                <p>Pour en savoir plus sur les différents statuts de freelance, consultez notre page sur <a href="/salaire-brut-net-auto-entrepreneur/" class="text-brand-600 hover:text-brand-700">l'auto-entrepreneur</a>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du salaire journalier pour les indemnités</h2>
                <p>Le <strong>salaire journalier</strong> sert de base de calcul pour plusieurs types d'indemnités versées par la Sécurité sociale ou Pôle Emploi. Comprendre son calcul est essentiel pour anticiper vos revenus en cas d'arrêt maladie, maternité ou chômage.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnités journalières maladie (IJSS)</h3>
                <p>En cas d'arrêt maladie, la Sécurité sociale verse des <strong>indemnités journalières</strong> calculées sur la base de votre salaire journalier brut :</p>
                <ul>
                    <li><strong>Salaire journalier de référence</strong> = Salaires bruts des 3 derniers mois / 91,25 jours</li>
                    <li><strong>Indemnité journalière</strong> = 50% du salaire journalier de référence (plafonné à 52,35 € en 2026)</li>
                </ul>
                <p>Exemple : si vous avez gagné 7 500 € brut sur les 3 derniers mois :</p>
                <ul>
                    <li>Salaire journalier de référence : 7 500 / 91,25 = 82,19 €</li>
                    <li>Indemnité journalière : 82,19 × 50% = 41,10 €/jour (plafonné à 52,35 €)</li>
                </ul>
                <p>Les IJSS sont versées après un délai de carence de 3 jours. Elles sont soumises à la CSG et à la CRDS, mais pas aux cotisations sociales normales.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnités journalières maternité</h3>
                <p>Pour un congé maternité, le calcul est similaire mais plus avantageux : l'indemnité représente <strong>100% du salaire journalier net</strong> (dans la limite du plafond). Le salaire journalier de référence est calculé sur les 3 derniers mois précédant le congé.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Indemnités de congés payés</h3>
                <p>Les congés payés sont rémunérés selon la règle du <strong>maintien de salaire</strong> ou du <strong>1/10ème</strong>, selon ce qui est le plus favorable au salarié :</p>
                <ul>
                    <li><strong>Maintien de salaire</strong> : vous percevez votre salaire habituel comme si vous travailliez</li>
                    <li><strong>Règle du 1/10ème</strong> : Salaire brut perçu sur la période de référence × 10%</li>
                </ul>
                <p>Le salaire journalier de congés payés est donc rarement défavorable au salarié.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaire journalier et intérimaires</h2>
                <p>Pour les <strong>travailleurs intérimaires</strong>, le salaire journalier est le mode de rémunération le plus courant. Les missions d'intérim se comptent souvent en jours, avec un taux journalier négocié selon le profil et le poste.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul du salaire journalier en intérim</h3>
                <p>Le salaire journalier brut d'un intérimaire comprend :</p>
                <ul>
                    <li>Le <strong>taux horaire de base</strong> × nombre d'heures travaillées dans la journée (souvent 7h)</li>
                    <li>Les <strong>Indemnités de Fin de Mission (IFM)</strong> : 10% du salaire brut total</li>
                    <li>Les <strong>Indemnités Compensatrices de Congés Payés (ICCP)</strong> : 10% du salaire brut + IFM</li>
                </ul>
                <p>Exemple pour un intérimaire à 15 €/h travaillant 7h/jour :</p>
                <ul>
                    <li>Salaire de base : 15 × 7 = 105 € brut</li>
                    <li>IFM (10%) : 10,50 €</li>
                    <li>ICCP (10% de 105 + 10,50) : 11,55 €</li>
                    <li><strong>Total journalier brut : 127,05 €</strong></li>
                </ul>
                <p>Les IFM et ICCP compensent l'absence de CDI et les périodes d'intermission entre deux missions. Ils sont soumis aux cotisations sociales normales.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le Salaire Journalier de Référence (SJR) pour le chômage</h2>
                <p>En cas de chômage, Pôle Emploi calcule vos allocations (ARE) sur la base de votre <strong>Salaire Journalier de Référence (SJR)</strong>. Ce calcul est crucial car il détermine le montant de vos allocations mensuelles.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul du SJR</h3>
                <p>Le SJR se calcule ainsi :</p>
                <p><strong>SJR = Salaires bruts des 24 ou 36 derniers mois / Nombre de jours travaillés</strong></p>
                <ul>
                    <li>Pour les moins de 53 ans : période de référence de <strong>24 mois</strong></li>
                    <li>Pour les 53 ans et plus : période de référence de <strong>36 mois</strong></li>
                </ul>
                <p>Exemple : vous avez perçu 60 000 € brut sur 24 mois et travaillé 480 jours :</p>
                <ul>
                    <li>SJR = 60 000 / 480 = <strong>125 € brut/jour</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">De SJR à Allocation chômage (ARE)</h3>
                <p>L'ARE est calculée selon la formule la plus avantageuse entre :</p>
                <ul>
                    <li><strong>Formule A</strong> : (SJR × 40,4%) + 13,03 € par jour</li>
                    <li><strong>Formule B</strong> : SJR × 57%</li>
                </ul>
                <p>Exemple avec un SJR de 125 € :</p>
                <ul>
                    <li>Formule A : (125 × 40,4%) + 13,03 = 63,53 €/jour</li>
                    <li>Formule B : 125 × 57% = 71,25 €/jour</li>
                    <li><strong>ARE retenue : 71,25 €/jour</strong> (la plus favorable)</li>
                    <li>Allocation mensuelle : 71,25 × 30 jours = <strong>2 137,50 €/mois</strong></li>
                </ul>
                <p>L'ARE est plafonnée à <strong>75% du SJR</strong> (et ne peut dépasser 276,60 € par jour en 2026). Elle est soumise à CSG et CRDS.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Convertir un salaire journalier en mensuel et annuel</h2>
                <p>Pour estimer votre revenu mensuel ou annuel à partir d'un salaire journalier, utilisez ces formules simples :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Du journalier au mensuel</h3>
                <p><strong>Salaire mensuel brut = Salaire journalier brut × 21,67</strong></p>
                <p>Le nombre 21,67 correspond au nombre moyen de jours ouvrés par mois (260 jours / 12 mois).</p>
                <p>Exemples :</p>
                <ul>
                    <li>80 € brut/jour → 80 × 21,67 = <strong>1 734 € brut/mois</strong></li>
                    <li>120 € brut/jour → 120 × 21,67 = <strong>2 600 € brut/mois</strong></li>
                    <li>180 € brut/jour → 180 × 21,67 = <strong>3 901 € brut/mois</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Du journalier à l'annuel</h3>
                <p><strong>Salaire annuel brut = Salaire journalier brut × 260</strong></p>
                <p>Le nombre 260 correspond au nombre de jours ouvrés dans une année (52 semaines × 5 jours).</p>
                <p>Exemples :</p>
                <ul>
                    <li>80 € brut/jour → 80 × 260 = <strong>20 800 € brut/an</strong></li>
                    <li>120 € brut/jour → 120 × 260 = <strong>31 200 € brut/an</strong></li>
                    <li>180 € brut/jour → 180 × 260 = <strong>46 800 € brut/an</strong></li>
                </ul>
                <p>Ces conversions sont indicatives et ne tiennent pas compte des congés payés, RTT ou primes éventuelles. Pour un calcul précis de votre rémunération annuelle, consultez notre page sur le <a href="/salaire-brut-net-annuel/" class="text-brand-600 hover:text-brand-700">salaire brut net annuel</a>.</p>
            """
        },
        {
            "slug": "taux-horaire-brut-net",
            "title": "Taux Horaire Brut Net 2026 : Convertisseur Horaire",
            "desc": "Convertissez votre taux horaire brut en net et inversement en 2026. Base 35h/semaine, SMIC horaire à 11,88€ et calculateur gratuit avec résultat instantané.",
            "kw": "taux horaire brut net, convertir taux horaire, brut net heure, salaire horaire calcul",
            "h1": "Convertisseur <span class=\"text-brand-600\">Taux Horaire</span> Brut Net",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900 mt-8">Pourquoi convertir son taux horaire ?</h2>
                <p>Connaître son <strong>taux horaire net</strong> est utile pour comparer des offres d'emploi, négocier un salaire ou évaluer la rentabilité d'heures supplémentaires.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Comment calculer</h3>
                <p>Le taux horaire brut se trouve sur votre fiche de paie ou se calcule ainsi :</p>
                <ul>
                    <li><strong>Taux horaire brut</strong> = Salaire brut mensuel / 151,67 heures</li>
                    <li><strong>Taux horaire net</strong> = Taux horaire brut × 0,78 (non-cadre) ou × 0,75 (cadre)</li>
                </ul>
                <p>Pour utiliser notre calculateur ci-dessus, entrez votre salaire mensuel brut (taux horaire × 151,67).</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Grille indicative</h3>
                <ul>
                    <li><strong>SMIC</strong> : 11,88 € brut/h → 9,27 € net/h</li>
                    <li><strong>14 €/h brut</strong> → 10,92 € net/h (2 123 € brut/mois)</li>
                    <li><strong>18 €/h brut</strong> → 14,04 € net/h (2 730 € brut/mois)</li>
                    <li><strong>22 €/h brut</strong> → 17,16 € net/h (3 337 € brut/mois)</li>
                    <li><strong>30 €/h brut</strong> → 23,40 € net/h (4 550 € brut/mois)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Temps partiel et taux horaire</h2>
                <p>Pour les salariés à <strong>temps partiel</strong>, le taux horaire brut reste identique à celui d'un temps plein. Seul le nombre d'heures travaillées change, donc le salaire mensuel est proportionnellement réduit.</p>
                <p>Exemple d'un temps partiel à 28h/semaine (80%) avec un taux de 15 €/h brut :</p>
                <ul>
                    <li>Heures mensuelles : 28h × 52 / 12 = <strong>121,33 heures/mois</strong></li>
                    <li>Salaire brut mensuel : 121,33 × 15 = <strong>1 820 € brut</strong></li>
                    <li>Salaire net : environ <strong>1 420 € net/mois</strong></li>
                </ul>
                <p>Important : les salariés à temps partiel bénéficient des mêmes droits que les temps plein (congés payés, mutuelle, formation) au prorata de leur temps de travail.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparaison des taux horaires en Europe</h2>
                <p>Le <a href="/smic-brut-net-2026/" class="text-brand-600 hover:text-brand-700">SMIC horaire français</a> (11,88 € brut en 2026) se situe dans la moyenne haute européenne. Voici quelques comparaisons :</p>
                <ul>
                    <li><strong>Luxembourg</strong> : ~15,50 € brut/h (salaire minimum le plus élevé d'Europe)</li>
                    <li><strong>France</strong> : 11,88 € brut/h</li>
                    <li><strong>Allemagne</strong> : ~12,00 € brut/h</li>
                    <li><strong>Belgique</strong> : ~11,50 € brut/h</li>
                    <li><strong>Espagne</strong> : ~8,50 € brut/h</li>
                    <li><strong>Portugal</strong> : ~5,50 € brut/h</li>
                </ul>
                <p>Attention : ces comparaisons doivent tenir compte du <a href="/cout-employeur/" class="text-brand-600 hover:text-brand-700">coût total employeur</a>, des cotisations sociales et du coût de la vie, qui varient fortement d'un pays à l'autre.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Négocier son taux horaire</h2>
                <p>Que vous soyez salarié en CDI, intérimaire ou freelance, <a href="/negocier-salaire/" class="text-brand-600 hover:text-brand-700">négocier votre taux horaire</a> peut avoir un impact significatif sur votre revenu annuel :</p>
                <p>Une augmentation de <strong>1 € brut/h</strong> représente :</p>
                <ul>
                    <li>+151,67 € brut/mois (temps plein)</li>
                    <li>+1 820 € brut/an</li>
                    <li>+1 420 € net/an (environ)</li>
                </ul>
                <p>Sur une carrière de 40 ans, 1 € d'augmentation horaire = <strong>+56 800 € de revenus nets cumulés</strong>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux horaire et convention collective</h2>
                <p>Les <strong>conventions collectives</strong> fixent des grilles de salaires minimum par catégorie et niveau, qui s'expriment souvent en taux horaire brut. Chaque branche professionnelle définit ses propres grilles, ce qui peut créer des écarts importants entre secteurs.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Grilles conventionnelles vs SMIC</h3>
                <p>Le salaire minimum conventionnel ne peut être inférieur au SMIC (11,88 € brut/h en 2026). Si la convention collective prévoit un taux horaire inférieur au SMIC pour un niveau donné, c'est le SMIC qui s'appliqué automatiquement.</p>
                <p>Exemples de taux horaires minimums conventionnels dans différentes branches :</p>
                <ul>
                    <li><strong>Commerce de détail</strong> : niveau 1 à 12,10 €/h, niveau 5 (responsable) à 16,50 €/h</li>
                    <li><strong>Métallurgie</strong> : ouvrier niveau I à 12,20 €/h, technicien niveau III à 18,50 €/h</li>
                    <li><strong>Bureaux d'études techniques</strong> : employé niveau A à 13 €/h, ingénieur cadre à 25+ €/h</li>
                </ul>
                <p>Vérifiez toujours la convention collective applicable à votre entreprise pour connaître les minimums garantis.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Négociation collective et revalorisation annuelle</h3>
                <p>Les partenaires sociaux renégocient régulièrement les grilles de salaires conventionnelles. En général, ces revalorisations interviennent <strong>une fois par an</strong> et s'appliquent automatiquement à tous les salariés de la branche. Le taux horaire minimum conventionnel augmente donc mécaniquement chaque année, souvent de 1 à 3% selon l'inflation et les négociations.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact de l'ancienneté sur le taux horaire</h2>
                <p>L'<strong>ancienneté</strong> dans l'entreprise ou dans la profession peut avoir un impact direct sur votre taux horaire, selon les dispositions de votre convention collective ou de votre contrat de travail.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Prime d'ancienneté</h3>
                <p>Certaines conventions collectives prévoient une <strong>prime d'ancienneté</strong> qui s'ajoute au salaire de base. Cette prime est généralement calculée en pourcentage du salaire brut et augmente par paliers :</p>
                <ul>
                    <li><strong>3 ans d'ancienneté</strong> : +3% du salaire brut</li>
                    <li><strong>6 ans</strong> : +6%</li>
                    <li><strong>9 ans</strong> : +9%</li>
                    <li><strong>12 ans</strong> : +12%</li>
                    <li><strong>15 ans et +</strong> : +15%</li>
                </ul>
                <p>Exemple : un salarié à 15 €/h avec 9 ans d'ancienneté et une prime de 9% :</p>
                <ul>
                    <li>Taux horaire de base : 15 €/h</li>
                    <li>Prime d'ancienneté : 15 × 9% = 1,35 €/h</li>
                    <li><strong>Taux horaire total : 16,35 €/h</strong></li>
                </ul>
                <p>Cette prime s'ajoute au brut et est soumise aux mêmes cotisations que le salaire de base.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Progression automatique par l'ancienneté</h3>
                <p>Dans la fonction publique et certaines grandes entreprises, le taux horaire augmente automatiquement selon une grille indiciaire liée à l'ancienneté. Par exemple, un agent de catégorie C échelon 1 progresse automatiquement à l'échelon 2 après 1 an, puis échelon 3 après 2 ans, etc., avec une augmentation du taux horaire à chaque palier.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux horaire brut net pour les intérimaires</h2>
                <p>Les <strong>intérimaires</strong> ont un statut particulier qui impacte leur taux horaire. En plus du salaire de base, ils perçoivent des indemnités spécifiques qui augmentent significativement leur taux horaire brut effectif.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Composition du taux horaire intérimaire</h3>
                <p>Le taux horaire brut global d'un intérimaire comprend :</p>
                <ul>
                    <li><strong>Taux horaire de base</strong> : identique à celui d'un salarié permanent sur un poste équivalent</li>
                    <li><strong>IFM (Indemnité de Fin de Mission)</strong> : 10% du salaire brut total + congés payés</li>
                    <li><strong>ICCP (Indemnité Compensatrice de Congés Payés)</strong> : 10% du salaire brut + IFM</li>
                </ul>
                <p>Au total, ces indemnités représentent environ <strong>+21% du taux horaire de base</strong>.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple de calcul détaillé</h3>
                <p>Pour un intérimaire avec un taux de base de 14 €/h brut :</p>
                <ul>
                    <li>Taux de base : 14 €/h</li>
                    <li>IFM (10%) : 1,40 €/h</li>
                    <li>ICCP (10% de 14 + 1,40) : 1,54 €/h</li>
                    <li><strong>Taux horaire brut total : 16,94 €/h</strong></li>
                    <li>Taux horaire net (×0,78) : <strong>13,21 €/h net</strong></li>
                </ul>
                <p>Pour un mois complet (151,67h), cela représente :</p>
                <ul>
                    <li>Salaire brut mensuel : 16,94 × 151,67 = <strong>2 569 € brut</strong></li>
                    <li>Salaire net mensuel : <strong>2 004 € net</strong></li>
                </ul>
                <p>Les IFM et ICCP compensent la précarité de l'intérim et les périodes d'intermission entre missions.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du coût horaire employeur</h2>
                <p>Du point de vue de l'employeur, le <strong>coût horaire total</strong> (ou "super-brut") est beaucoup plus élevé que le taux horaire brut du salarié, en raison des cotisations patronales.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Formule du coût horaire employeur</h3>
                <p><strong>Coût horaire employeur = Taux horaire brut × 1,42 (non-cadre) ou × 1,45 (cadre)</strong></p>
                <p>Le coefficient 1,42 correspond aux <strong>42% de cotisations patronales</strong> moyennes (Sécurité sociale, retraite complémentaire, assurance chômage, formation, etc.).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de coût employeur</h3>
                <table class="w-full border-collapse border border-slate-300 mt-4">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="border border-slate-300 px-4 py-2">Taux horaire brut</th>
                            <th class="border border-slate-300 px-4 py-2">Taux horaire net</th>
                            <th class="border border-slate-300 px-4 py-2">Coût horaire employeur</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="border border-slate-300 px-4 py-2">11,88 € (SMIC)</td><td class="border border-slate-300 px-4 py-2">9,27 €</td><td class="border border-slate-300 px-4 py-2">16,87 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">15 €</td><td class="border border-slate-300 px-4 py-2">11,70 €</td><td class="border border-slate-300 px-4 py-2">21,30 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">20 €</td><td class="border border-slate-300 px-4 py-2">15,60 €</td><td class="border border-slate-300 px-4 py-2">28,40 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">25 €</td><td class="border border-slate-300 px-4 py-2">19,50 €</td><td class="border border-slate-300 px-4 py-2">35,50 €</td></tr>
                        <tr><td class="border border-slate-300 px-4 py-2">30 €</td><td class="border border-slate-300 px-4 py-2">23,40 €</td><td class="border border-slate-300 px-4 py-2">42,60 €</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Comprendre le <a href="/cout-employeur/" class="text-brand-600 hover:text-brand-700">coût employeur</a> est utile lors d'une négociation salariale : l'employeur raisonne en coût total, pas seulement en brut. Une augmentation de 1 €/h brut lui coûte en réalité environ 1,42 €/h.</p>
            """
        },
    ]

    # Add enrichments
    for p in pages:
        if "mensuel" in p["slug"]:
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 4000, 5000], "non-cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Comment passer du brut mensuel au brut annuel ?", "a": "Multipliez votre salaire brut mensuel par 12. Par exemple, 2 500 € brut/mois = 30 000 € brut/an."},
                {"q": "Le 13ème mois est-il inclus dans le salaire mensuel ?", "a": "Non, le 13ème mois est une prime versée en plus du salaire mensuel habituel, généralement en fin d'année."},
                {"q": "Les primes mensuelles sont-elles incluses dans le brut ?", "a": "Oui, toutes les primes versées régulièrement (prime d'ancienneté, de panier, etc.) s'ajoutent au brut mensuel."},
                {"q": "Comment comparer deux offres d'emploi avec des bruts mensuels différents ?", "a": "Convertissez les deux en net mensuel avec notre calculateur, puis comparez en tenant compte des avantages (tickets restaurant, mutuelle, télétravail)."},
                {"q": "Le brut mensuel change-t-il selon les mois ?", "a": "Le salaire de base reste fixe, mais le brut peut varier avec les heures supplémentaires, primes ponctuelles ou absences non rémunérées."},
            ])
            p["examples"] = generate_examples([
                {"name": "Camille, 30 ans", "situation": "Commercial – 2 500 € brut/mois", "brut": "2 500 €", "net": "1 950 €", "net_apres_impot": "1 852 €"},
                {"name": "Lucas, 27 ans", "situation": "Développeur – 3 200 € brut/mois", "brut": "3 200 €", "net": "2 496 €", "net_apres_impot": "2 296 €"},
                {"name": "Nadia, 38 ans", "situation": "Infirmière – 2 800 € brut/mois", "brut": "2 800 €", "net": "2 184 €", "net_apres_impot": "2 023 €"},
            ])
        elif "annuel" in p["slug"]:
            p["table"] = generate_conversion_table([2000, 2500, 3000, 3500, 4000, 5000], "non-cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Pourquoi les offres d'emploi affichent-elles le salaire annuel ?", "a": "Le brut annuel est devenu la norme car il permet de comparer facilement les offres sans se soucier du nombre de mois (12, 13, 14...)."},
                {"q": "Comment convertir un salaire annuel en mensuel ?", "a": "Divisez le brut annuel par 12 pour obtenir le brut mensuel moyen. Attention au 13ème mois s'il existe."},
                {"q": "Le net annuel inclut-il le 13ème mois ?", "a": "Si le 13ème mois est prévu, il faut l'ajouter au net annuel calculé sur 12 mois."},
                {"q": "Comment négocier son salaire en brut annuel ?", "a": "Renseignez-vous sur les salaires du marché pour votre poste, calculez le net mensuel correspondant, et demandez une fourchette en brut annuel."},
                {"q": "Le salaire annuel change-t-il selon les années ?", "a": "Oui, grâce aux augmentations individuelles, promotions, primes variables ou indexations conventionnelles."},
            ])
            p["examples"] = generate_examples([
                {"name": "Antoine, 26 ans", "situation": "Comptable – 28 000 € brut/an", "brut": "2 333 €", "net": "1 820 €", "net_apres_impot": "1 717 €"},
                {"name": "Sarah, 33 ans", "situation": "Chef de projet – 42 000 € brut/an", "brut": "3 500 €", "net": "2 730 €", "net_apres_impot": "2 485 €"},
                {"name": "Pierre, 29 ans", "situation": "Designer – 32 000 € brut/an", "brut": "2 667 €", "net": "2 080 €", "net_apres_impot": "1 934 €"},
            ])
        elif "horaire" in p["slug"]:
            p["table"] = generate_conversion_table([1800, 2200, 2600, 3000, 3500, 4000], "non-cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Comment calculer le taux horaire à partir du salaire mensuel ?", "a": "Divisez votre salaire brut mensuel par 151,67 heures (base légale 35h/semaine). Par exemple : 2 500 € / 151,67 = 16,48 €/h."},
                {"q": "Le taux horaire est-il négociable ?", "a": "Oui, vous pouvez négocier votre taux horaire à l'embauche ou lors d'un entretien annuel, surtout en CDD ou intérim."},
                {"q": "Les heures supplémentaires augmentent-elles le taux horaire ?", "a": "Oui, les heures supplémentaires sont majorées de 25% (36-43h) ou 50% (au-delà de 43h), ce qui augmente le taux horaire effectif."},
                {"q": "Le SMIC horaire est-il le même partout en France ?", "a": "Oui, le SMIC horaire (11,88 € brut en 2026) est identique dans toute la France métropolitaine. Les DOM ont parfois des SMIC légèrement différents."},
                {"q": "Comment comparer un taux horaire brut et net ?", "a": "Multipliez le taux horaire brut par 0,78 (non-cadre) pour obtenir le taux horaire net approximatif."},
            ])
            p["examples"] = generate_examples([
                {"name": "Lucie, 24 ans", "situation": "Vendeuse – 12,50 €/h brut", "brut": "1 896 €", "net": "1 479 €", "net_apres_impot": "1 419 €"},
                {"name": "Maxime, 31 ans", "situation": "Électricien – 18 €/h brut", "brut": "2 730 €", "net": "2 129 €", "net_apres_impot": "1 973 €"},
                {"name": "Clara, 28 ans", "situation": "Aide-soignante – 15 €/h brut", "brut": "2 275 €", "net": "1 775 €", "net_apres_impot": "1 673 €"},
            ])
        else:
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 3500], "non-cadre")
            p["faqs"] = generate_faq_section([
                {"q": "Comment calculer mon salaire pour cette période ?", "a": "Utilisez notre calculateur ci-dessus en entrant votre salaire brut mensuel."},
                {"q": "Les cotisations sont-elles les mêmes quelle que soit la période ?", "a": "Oui, les taux de cotisations sont fixes et s'appliquent de la même manière sur le brut mensuel, annuel ou horaire."},
                {"q": "Puis-je convertir facilement entre les différentes périodes ?", "a": "Oui : brut horaire × 151,67 = brut mensuel. Brut mensuel × 12 = brut annuel."},
                {"q": "Le calcul change-t-il pour un temps partiel ?", "a": "Le taux de cotisations reste le même, seul le montant brut change proportionnellement au temps de travail."},
                {"q": "Comment vérifier ma fiche de paie ?", "a": "Comparez le brut et le net affichés avec notre calculateur. Un écart de quelques euros est normal (mutuelle, prévoyance)."},
            ])
            p["examples"] = ""

    for p in pages:
        html = page_head(p["title"], p["desc"], f'{BASE_URL}/{p["slug"]}/', p["kw"])
        html += HEADER
        html += breadcrumb(p["h1"].replace('<span class="text-brand-600">', '').replace('</span>', ''))
        html += f'''
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 mb-6">{p["h1"]}</h1>
            </div>
        </section>'''
        html += calculator_widget(2500, "non-cadre", "brut")
        html += f'''
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>'''
        if "table" in p and p["table"]:
            html += f'''
        <section class="py-12 px-4 bg-slate-50">
            <div class="mx-auto max-w-4xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6">Tableau de conversion brut → net</h2>
                {p["table"]}
            </div>
        </section>'''
        if "examples" in p and p["examples"]:
            html += f'''
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl">
                {p["examples"]}
            </div>
        </section>'''
        if "faqs" in p and p["faqs"]:
            html += p["faqs"]
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\n</body></html>"
        write_page(p["slug"], html)


# ── 3. Pages de contenu éducatif ──────────────────────────────────────────────

def gen_content_pages():
    pages = [
        {
            "slug": "différence-salaire-brut-net",
            "title": "Différence Salaire Brut et Net 2026 : Explications",
            "desc": "Comprendre la différence entre salaire brut et net en 2026. Cotisations sociales détaillées, calcul étape par étape et exemples concrets pour chaque statut.",
            "kw": "différence brut net, c'est quoi le salaire brut, salaire brut vs net, explication brut net",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Qu'est-ce que le salaire brut ?</h2>
                <p>Le <strong>salaire brut</strong> est la rémunération totale inscrite sur votre contrat de travail, avant toute déduction. C'est le montant que votre employeur s'engage à vous verser. Il inclut votre salaire de base, les éventuelles primes, heures supplémentaires et avantages en nature.</p>
                <p>Le brut constitue la référence légale de votre rémunération. C'est sur cette base que sont calculées toutes les cotisations sociales (salariales et patronales), les indemnités de licenciement, les primes conventionnelles et l'indemnité de départ à la retraite. Dans les négociations salariales, on parle toujours en brut annuel ou mensuel.</p>
                <p>Le salaire brut comprend plusieurs éléments : le salaire de base (inscrit au contrat), les primes régulières ou exceptionnelles (prime d'ancienneté, prime de 13ème mois, primes de performance), les heures supplémentaires et complémentaires, ainsi que les avantages en nature valorisés (voiture de fonction, logement).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Qu'est-ce que le salaire net ?</h2>
                <p>Le <strong>salaire net</strong> (ou "net à payer avant impôt") est ce que vous recevez effectivement sur votre compte bancaire, après déduction de toutes les cotisations sociales salariales. Depuis 2019, le <strong>net après impôt</strong> tient aussi compte du prélèvement à la source.</p>
                <p>Le salaire net représente votre pouvoir d'achat réel avant impôt sur le revenu. C'est le montant que vous pouvez utiliser pour vos dépenses courantes, votre épargne ou vos investissements. Attention toutefois : ce n'est pas forcément ce qui arrive sur votre compte, car le prélèvement à la source vient ensuite se déduire pour donner le "net à payer" final.</p>
                <p>Dans votre budget personnel, c'est le net mensuel qui compte vraiment. C'est pourquoi il est essentiel de bien le calculer avant d'accepter une offre d'emploi ou de négocier une augmentation. Une différence de 100 € brut représente environ 78 € net pour un non-cadre et 75 € net pour un cadre.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Que se passe-t-il entre le brut et le net ?</h2>
                <p>Entre votre salaire brut et votre salaire net, plusieurs cotisations sociales obligatoires sont prélevées. Ces prélèvements financent l'ensemble du système de protection sociale français : assurance maladie, retraite, chômage, allocations familiales.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Détail des cotisations salariales</h3>
                <ul class="space-y-2">
                    <li><strong>Assurance vieillesse</strong> (retraite de base) : 6,90% sur la tranche 1 (jusqu'à 3 864 €) + 0,40% sur la totalité du salaire. Cette cotisation finance votre retraite de base du régime général de la Sécurité sociale.</li>
                    <li><strong>Retraite complémentaire AGIRC-ARRCO</strong> : 3,15% sur la tranche 1 et 8,64% sur la tranche 2 (au-delà de 3 864 €). Ces cotisations vous donnent des points de retraite complémentaire obligatoire.</li>
                    <li><strong>CSG déductible</strong> (Contribution Sociale Généralisée) : 6,80% sur 98,25% du brut. Cette part est déductible de votre revenu imposable.</li>
                    <li><strong>CSG non déductible</strong> : 2,40% sur 98,25% du brut. Cette part n'est pas déductible et vient augmenter votre net imposable.</li>
                    <li><strong>CRDS</strong> (Contribution au Remboursement de la Dette Sociale) : 0,50% sur 98,25% du brut. Cette contribution sert à rembourser la dette de la Sécurité sociale.</li>
                    <li><strong>CEG</strong> (Contribution d'Équilibre Générale) : 0,86% sur la tranche 1 et 1,08% sur la tranche 2. Cette contribution équilibre les comptes de l'AGIRC-ARRCO.</li>
                    <li><strong>CET pour les cadres uniquement</strong> : 0,14% sur la totalité du salaire. Cette Contribution d'Équilibre Technique finance les droits spécifiques des cadres.</li>
                </ul>

                <p class="mt-4">Au total, ces cotisations représentent environ <strong>22% du brut pour un non-cadre</strong> et <strong>25% du brut pour un cadre</strong>. Le taux exact varie légèrement selon le niveau de salaire, notamment pour les salaires supérieurs au plafond de la Sécurité sociale (3 864 € en 2026).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Tableau de conversion brut → net 2026</h2>
                <p>Voici un tableau de conversion pour les salaires les plus courants, statut non-cadre :</p>
                """ + generate_conversion_table([1802, 2000, 2500, 3000, 3500, 4000, 5000], "non-cadre") + """

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Les différents "nets" sur votre fiche de paie</h2>
                <p>Votre bulletin de salaire affiche plusieurs montants "nets" qui ont chacun une fonction précise. Il est essentiel de bien les distinguer pour comprendre votre rémunération réelle et votre situation fiscale.</p>
                <ul class="space-y-2">
                    <li><strong>Net à payer avant impôt</strong> : brut - cotisations salariales. C'est le "salaire net" classique, celui que tout le monde appelait "net" avant 2019. C'est votre rémunération après déduction des cotisations sociales mais avant l'impôt.</li>
                    <li><strong>Net imposable</strong> : net à payer + CSG non déductible + CRDS. Ce montant sert de base au calcul de votre impôt sur le revenu. Il est supérieur d'environ 2,9% au net à payer. C'est ce montant qui apparaît dans votre déclaration de revenus pré-remplie.</li>
                    <li><strong>Net à payer (final)</strong> : net avant impôt - prélèvement à la source. C'est ce qui arrive effectivement sur votre compte bancaire chaque mois. Depuis janvier 2019, l'impôt sur le revenu est prélevé directement par l'employeur.</li>
                </ul>
                <p class="mt-4">Exemple concret pour un salaire brut de 3 000 € (non-cadre) : Net à payer avant impôt = 2 340 € → Net imposable = 2 408 € → Prélèvement à la source (7,5% par exemple) = 181 € → <strong>Net à payer final = 2 159 €</strong>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différences brut-net selon le statut</h2>
                <p>Le taux de conversion du brut en net varie selon votre statut professionnel. Cette variation s'explique par des cotisations spécifiques à chaque catégorie de salariés.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Secteur privé</h3>
                <ul class="space-y-2">
                    <li><strong>Non-cadre</strong> : environ 78% du brut (22% de cotisations). Par exemple, 2 500 € brut → 1 950 € net.</li>
                    <li><strong>Cadre</strong> : environ 75% du brut (25% de cotisations, incluant la CET). Par exemple, 4 000 € brut → 3 000 € net.</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Fonction publique</h3>
                <p>Les fonctionnaires bénéficient d'un taux de conversion plus avantageux : environ <strong>83% du brut</strong> (17% de cotisations). Les cotisations sont moins élevées car certaines prestations sociales sont gérées différemment. Par exemple, 2 500 € brut → 2 075 € net.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Statuts particuliers</h3>
                <ul class="space-y-2">
                    <li><strong>Alternants (apprentis, contrats de professionnalisation)</strong> : exonération totale ou partielle de cotisations selon l'âge et le salaire. Un apprenti peut toucher près de 100% de son brut en net.</li>
                    <li><strong>Stagiaires</strong> : si la gratification dépassé le seuil légal (4,35 €/h en 2026), elle est soumise aux cotisations sociales au-delà de ce seuil uniquement.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Brut vs net dans différents secteurs</h2>
                <p>Au-delà du statut cadre/non-cadre, certains secteurs professionnels ont des spécificités en matière de cotisations qui impactent le taux de conversion brut-net.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Secteur du bâtiment (BTP)</h3>
                <p>Les salariés du BTP ont des cotisations supplémentaires spécifiques : cotisations patronales de congés payés (caisse de congés payés du BTP) et cotisations pour la médecine du travail BTP. Le taux de conversion reste proche de 78% pour un non-cadre, mais la structure de la fiche de paie est différente.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Secteur de l'intérim</h3>
                <p>Les intérimaires ont une indemnité de fin de mission (IFM) de 10% et une indemnité compensatrice de congés payés (ICCP) de 10%, qui s'ajoutent au brut. Ces indemnités sont soumises aux cotisations sociales. Au final, le "net" d'un intérimaire intègre ces primes de précarité.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Professions libérales</h3>
                <p>Les professionnels libéraux ne sont pas salariés et relèvent d'un régime social différent (URSSAF, CIPAV, CARCDSF selon la profession). Leurs cotisations sont calculées différemment (pourcentage du chiffre d'affaires ou du bénéfice) et ne suivent pas la logique brut/net des salariés.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Historique du système brut-net en France</h2>
                <p>Le système français de séparation entre salaire brut et salaire net découle de l'histoire de notre protection sociale. Après la Seconde Guerre mondiale, les ordonnances de 1945 ont créé la Sécurité sociale pour garantir à tous une couverture santé, retraite et famille.</p>
                <p>Le financement de ce système repose sur des cotisations obligatoires, prélevées sur les salaires. Le choix a été fait de rendre ces cotisations visibles sur la fiche de paie, pour que chaque salarié comprenne comment est financée sa protection sociale. C'est ce qui explique la différence importante entre brut et net en France (environ 22-25%) comparé à d'autres pays.</p>
                <p>En 2018, une réforme a simplifié la lecture des fiches de paie en regroupant les cotisations par risque (santé, retraite, chômage, etc.) plutôt que par organisme collecteur. Cette simplification visuelle n'a pas modifié les montants prélevés, mais a rendu la fiche de paie plus compréhensible.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Formule rapide de conversion</h2>
                <p>Pour une estimation rapide lors d'une négociation salariale ou d'un entretien d'embauche, vous pouvez utiliser ces coefficients multiplicateurs :</p>
                <ul class="space-y-2">
                    <li><strong>Non-cadre</strong> : Salaire net ≈ Salaire brut × 0,78</li>
                    <li><strong>Cadre</strong> : Salaire net ≈ Salaire brut × 0,75</li>
                    <li><strong>Fonction publique</strong> : Salaire net ≈ Salaire brut × 0,83</li>
                </ul>
                <p>Ces formules donnent une approximation rapide. Pour un calcul précis tenant compte des tranches de cotisations et de votre situation exacte, utilisez notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact pratique : exemples chiffrés</h2>
                <p>Comprendre la différence brut-net est essentiel pour évaluer une offre d'emploi ou négocier une augmentation. Voici des exemples concrets :</p>
                <ul class="space-y-3">
                    <li><strong>Offre à 30 000 € brut annuel (non-cadre)</strong> : cela représente 2 500 € brut/mois, soit environ 1 950 € net/mois, soit 23 400 € net annuel. Après impôt (taux moyen de 5% par exemple), cela donne environ 1 852 € net par mois réellement disponible.</li>
                    <li><strong>Augmentation de 200 € brut/mois</strong> : pour un non-cadre, cela représente environ 156 € net supplémentaires par mois, soit 1 872 € net de plus par an.</li>
                    <li><strong>Prime de 1 500 € brut</strong> : après cotisations (~22%), vous toucherez environ 1 170 € net. Si votre taux de prélèvement à la source est de 7,5%, il reste environ 1 082 € après impôt.</li>
                </ul>
            """
        },
        {
            "slug": "cotisations-sociales-salariales",
            "title": "Cotisations Sociales Salariales 2026 : Taux Complets",
            "desc": "Détail complet des cotisations sociales salariales 2026. Taux, assiettes, plafonds et explication de chaque cotisation prélevée sur votre salaire brut.",
            "kw": "cotisations sociales salariales, charges salariales, taux cotisations 2026, détail cotisations",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Les cotisations sociales en France</h2>
                <p>Les <strong>cotisations sociales salariales</strong> sont des prélèvements obligatoires sur votre salaire brut qui financent la protection sociale française : retraite, maladie, chômage, allocations familiales, etc. Ces cotisations représentent la différence entre votre salaire brut (inscrit sur votre contrat) et votre salaire net (versé sur votre compte). En 2026, elles s'élèvent à environ 22% du brut pour un non-cadre et 25% pour un cadre.</p>
                <p>Contrairement aux cotisations patronales (payées par l'employeur), les cotisations salariales sont directement déduites de votre rémunération. Elles apparaissent en détail sur votre fiche de paie et ouvrent des droits sociaux : pensions de retraite, remboursements de soins, indemnités chômage, etc.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Tableau des cotisations salariales 2026</h2>
                <p>Voici le détail exhaustif des cotisations prélevées sur votre salaire brut en 2026 :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Cotisation</th><th class="py-2 text-right">Taux salarial</th><th class="py-2 text-right">Assiette</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Vieillesse plafonnée</td><td class="py-2 text-right">6,90%</td><td class="py-2 text-right">Tranche 1 (≤ PSS)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Vieillesse déplafonnée</td><td class="py-2 text-right">0,40%</td><td class="py-2 text-right">Totalité</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">AGIRC-ARRCO T1</td><td class="py-2 text-right">3,15%</td><td class="py-2 text-right">Tranche 1</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">AGIRC-ARRCO T2</td><td class="py-2 text-right">8,64%</td><td class="py-2 text-right">Tranche 2 (&gt; PSS)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CEG T1</td><td class="py-2 text-right">0,86%</td><td class="py-2 text-right">Tranche 1</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CEG T2</td><td class="py-2 text-right">1,08%</td><td class="py-2 text-right">Tranche 2</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CET (cadres uniquement)</td><td class="py-2 text-right">0,14%</td><td class="py-2 text-right">Totalité</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CSG déductible</td><td class="py-2 text-right">6,80%</td><td class="py-2 text-right">98,25% du brut</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CSG non déductible</td><td class="py-2 text-right">2,40%</td><td class="py-2 text-right">98,25% du brut</td></tr>
                        <tr><td class="py-2">CRDS</td><td class="py-2 text-right">0,50%</td><td class="py-2 text-right">98,25% du brut</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le Plafond de la Sécurité Sociale (PSS)</h2>
                <p>En 2026, le PSS est de <strong>3 864 € par mois</strong> (46 368 € par an). Ce plafond est un seuil de référence essentiel dans le calcul des cotisations sociales. Les cotisations dites "plafonnées" s'appliquent uniquement sur la partie du salaire inférieure ou égale au PSS (Tranche 1), tandis que les cotisations "déplafonnées" s'appliquent sur la totalité du salaire.</p>
                <p>Concrètement, si vous gagnez 5 000 € brut par mois : la Tranche 1 correspond aux premiers 3 864 € et la Tranche 2 aux 1 136 € restants. Les taux de cotisation diffèrent entre ces deux tranches, notamment pour la retraite complémentaire AGIRC-ARRCO (3,15% sur T1, mais 8,64% sur T2).</p>
                <p>Le PSS est revalorisé chaque année en fonction de l'évolution des salaires. Il sert également de base au calcul de nombreuses prestations sociales (indemnités journalières, pensions de retraite, etc.).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cotisations salariales vs cotisations patronales</h2>
                <p>Il existe deux types de cotisations sociales : les cotisations <strong>salariales</strong> (prélevées sur votre brut et déduites de votre net) et les cotisations <strong>patronales</strong> (payées par l'employeur en plus de votre brut). Voici une comparaison :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Tableau comparatif salariales vs patronales</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Type de cotisation</th><th class="py-2 text-right">Part salariale</th><th class="py-2 text-right">Part patronale</th><th class="py-2 text-right">Total</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Maladie-maternité</td><td class="py-2 text-right">0%</td><td class="py-2 text-right">7,00%</td><td class="py-2 text-right">7,00%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Vieillesse plafonnée</td><td class="py-2 text-right">6,90%</td><td class="py-2 text-right">8,55%</td><td class="py-2 text-right">15,45%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Vieillesse déplafonnée</td><td class="py-2 text-right">0,40%</td><td class="py-2 text-right">2,02%</td><td class="py-2 text-right">2,42%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Allocations familiales</td><td class="py-2 text-right">0%</td><td class="py-2 text-right">3,45%-5,25%</td><td class="py-2 text-right">3,45%-5,25%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Chômage</td><td class="py-2 text-right">0%</td><td class="py-2 text-right">4,05%</td><td class="py-2 text-right">4,05%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">AGIRC-ARRCO T1</td><td class="py-2 text-right">3,15%</td><td class="py-2 text-right">4,72%</td><td class="py-2 text-right">7,87%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CSG/CRDS</td><td class="py-2 text-right">9,70%</td><td class="py-2 text-right">0%</td><td class="py-2 text-right">9,70%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Au total, les cotisations patronales représentent environ 42-45% du salaire brut, contre 22-25% pour les cotisations salariales. C'est pourquoi le coût employeur (super-brut) est nettement supérieur au salaire brut.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">À quoi servent ces cotisations ?</h2>
                <p>Chaque cotisation finance une branche spécifique de la protection sociale. Voici le détail de leur utilisation :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Assurance vieillesse (retraite de base)</h3>
                <p>Les cotisations de <strong>vieillesse plafonnée (6,90%)</strong> et <strong>déplafonnée (0,40%)</strong> financent votre retraite de base du régime général de la Sécurité sociale. Chaque trimestre travaillé et cotisé vous donne des droits à pension. Pour une retraite à taux plein, il faut valider entre 166 et 172 trimestres selon votre année de naissance.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Retraite complémentaire AGIRC-ARRCO</h3>
                <p>Les cotisations <strong>AGIRC-ARRCO</strong> (3,15% sur T1 et 8,64% sur T2) vous donnent des points de retraite complémentaire obligatoire. Ces points s'accumulent tout au long de votre carrière. À la retraite, ils sont convertis en pension mensuelle en multipliant le nombre de points acquis par la valeur du point (1,4159 € en 2026).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. CSG et CRDS</h3>
                <p>La <strong>CSG</strong> (Contribution Sociale Généralisée) de 9,20% finance la Sécurité sociale dans son ensemble : assurance maladie, famille, vieillesse et dépendance. Elle se divise en deux parties : 6,80% déductible de votre revenu imposable et 2,40% non déductible.</p>
                <p>La <strong>CRDS</strong> (0,50%) sert exclusivement à rembourser la dette sociale accumulée par la Sécurité sociale. Créée en 1996, elle devait être temporaire mais a été prolongée jusqu'en 2033.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. CEG et CET</h3>
                <p>La <strong>CEG</strong> (Contribution d'Équilibre Générale) équilibre financièrement les comptes de l'AGIRC-ARRCO. La <strong>CET</strong> (Contribution d'Équilibre Technique), réservée aux cadres, finance les droits spécifiques des cadres (GMP - Garantie Minimale de Points).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exonérations et réductions de cotisations</h2>
                <p>Certaines situations donnent droit à des exonérations totales ou partielles de cotisations salariales :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Heures supplémentaires et complémentaires</h3>
                <p>Les heures supplémentaires bénéficient d'une <strong>réduction de cotisations salariales de 11,31%</strong> (exonération de la part salariale de l'assurance vieillesse). De plus, elles sont exonérées d'impôt sur le revenu dans la limite de 7 500 € net par an.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Apprentis</h3>
                <p>Les apprentis sont totalement exonérés de cotisations salariales (hors CSG/CRDS) dans la limite de 79% du SMIC. Au-delà, les cotisations s'appliquent normalement sur la part excédentaire.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Stagiaires</h3>
                <p>La gratification de stage est exonérée de cotisations sociales tant qu'elle ne dépassé pas le seuil légal de 4,35 € par heure (soit 659,03 € pour un mois complet à 35h/semaine en 2026). Au-delà, des cotisations s'appliquent sur la part excédentaire.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Zone de revitalisation rurale (ZRR)</h3>
                <p>Certains employeurs situés en ZRR peuvent bénéficier d'exonérations de cotisations, mais celles-ci concernent principalement les cotisations patronales plutôt que salariales.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact du niveau de salaire sur le taux de cotisations</h2>
                <p>Le taux global de cotisations salariales varie légèrement selon votre niveau de rémunération, en raison du système de tranches :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Salaire inférieur au PSS (≤ 3 864 €)</h3>
                <p>Pour un salaire en Tranche 1 uniquement, le taux global est d'environ <strong>22% pour un non-cadre</strong> et <strong>25% pour un cadre</strong>. C'est le cas de la majorité des salariés français.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Salaire supérieur au PSS (&gt; 3 864 €)</h3>
                <p>Au-delà du plafond, les cotisations de retraite complémentaire augmentent fortement (de 3,15% à 8,64% pour l'AGIRC-ARRCO). Le taux global de cotisations sur la Tranche 2 atteint environ <strong>23-24%</strong>, légèrement supérieur à la Tranche 1.</p>
                <p>Exemple pour 5 000 € brut : T1 (3 864 €) cotisée à ~22% + T2 (1 136 €) cotisée à ~24% → taux moyen de 22,4%.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques pour comprendre vos cotisations</h2>
                <ul class="space-y-3">
                    <li><strong>Vérifiez votre fiche de paie chaque mois</strong> : les cotisations doivent correspondre aux taux légaux. Des erreurs peuvent survenir, notamment lors d'un changement de salaire ou de statut.</li>
                    <li><strong>Distinguez CSG déductible et non déductible</strong> : seule la CSG déductible (6,80%) réduit votre revenu imposable. La CSG non déductible (2,40%) augmente votre net imposable.</li>
                    <li><strong>Consultez vos relevés de points AGIRC-ARRCO</strong> : chaque année, vous recevez un relevé indiquant vos points de retraite complémentaire acquis. Vérifiez qu'ils correspondent bien à vos cotisations.</li>
                    <li><strong>Anticipez l'impact des augmentations</strong> : une augmentation qui vous fait dépasser le PSS entraînera un taux de cotisations légèrement plus élevé sur la partie au-delà du plafond.</li>
                    <li><strong>Utilisez notre calculateur</strong> : pour connaître précisément vos cotisations selon votre salaire et votre statut, utilisez notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net gratuit</a>.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Évolution des taux de cotisations</h2>
                <p>Les taux de cotisations sociales évoluent chaque année, mais généralement de façon marginale. Les dernières réformes majeures ont eu lieu en 2018 avec la suppression des cotisations chômage et maladie salariales (compensées par la hausse de la CSG de 1,7 point).</p>
                <p>Cette réforme a été favorable aux salariés actifs (légère hausse du net d'environ 1,3%) mais défavorable aux retraités (pour qui la CSG a aussi augmenté sans compensation). Le taux global de cotisations salariales est passé d'environ 23% avant 2018 à 22% aujourd'hui pour un non-cadre.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cotisations et bulletin de paie simplifié</h2>
                <p>Depuis le 1er janvier 2018, le <strong>bulletin de paie simplifié</strong> est obligatoire dans toutes les entreprises. Les cotisations y sont regroupées en grandes catégories (santé, retraite, famille, chômage, autres contributions) au lieu d'être détaillées ligne par ligne. Cette simplification facilite la lecture pour le salarié, mais peut masquer certains détails.</p>
                <p>Si vous souhaitez un détail complet de vos cotisations, vous pouvez demander à votre employeur le <strong>bulletin de paie clarifié</strong>, qui conserve le regroupement mais ajoute des sous-totaux plus précis. Les cotisations patronales figurent également sur votre bulletin depuis 2018, ce qui vous permet de connaître le coût total de votre emploi pour l'entreprise.</p>
                <p>Pour vérifier que vos cotisations sont correctes, comparez le taux global de votre fiche de paie avec notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a>. Un écart de 1 à 2% est normal (cotisations de prévoyance, mutuelle obligatoire, titres restaurant), mais au-delà, interrogez votre service paie.</p>
            """
        },
        {
            "slug": "salaire-net-avant-après-impôt",
            "title": "Net Avant et Après Impôt 2026 : Comprendre l'Écart",
            "desc": "Différence entre net avant impôt et net après impôt en 2026. Prélèvement à la source, net imposable et calcul détaillé. Ce que vous touchez chaque mois.",
            "kw": "net avant impôt, net après impôt, prélèvement à la source, net imposable, salaire net impôt",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Net avant impôt vs net après impôt</h2>
                <p>Depuis janvier 2019, l'<strong>impôt sur le revenu</strong> est prélevé directement à la source sur votre salaire chaque mois. Cette réforme a modifié la présentation de votre fiche de paie, qui affiche désormais trois montants distincts : le brut, le net avant impôt et le net après impôt (net à payer). Comprendre ces différences est essentiel pour gérer votre budget et anticiper vos revenus réels.</p>
                <p>Le prélèvement à la source n'a pas créé de nouvel impôt : vous payez le même montant qu'avant, mais de façon échelonnée chaque mois plutôt qu'en une fois l'année suivante. Cette réforme vise à éviter les décalages de trésorerie et à adapter automatiquement l'impôt aux changements de revenus.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le net avant impôt</h2>
                <p>Le <strong>net avant impôt</strong> (ou "net à payer avant impôt sur le revenu") est votre salaire brut moins toutes les cotisations sociales salariales (retraite, CSG, CRDS, etc.). C'est le montant historiquement appelé "salaire net" avant la mise en place du prélèvement à la source.</p>
                <p>Ce montant reste important car il sert de référence dans plusieurs situations : calcul de certaines prestations sociales, indemnités de licenciement, comparaison avec vos anciens salaires d'avant 2019, etc. C'est aussi ce montant que vous communiquez généralement lorsqu'on vous demande votre "salaire net".</p>
                <p><strong>Formule</strong> : Net avant impôt = Salaire brut - Cotisations sociales salariales (environ -22% pour un non-cadre, -25% pour un cadre).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le net imposable : base du prélèvement</h2>
                <p>Le <strong>net imposable</strong> (ou "net fiscal") est le montant qui sert de base au calcul de votre impôt sur le revenu. Il diffère légèrement du net avant impôt car il réintègre certaines cotisations non déductibles fiscalement.</p>
                <p><strong>Formule</strong> : Net imposable = Net avant impôt + CSG non déductible (2,40%) + CRDS (0,50%).</p>
                <p>Concrètement, le net imposable est supérieur d'environ 2,9% au net avant impôt. Par exemple, pour un net de 2 000 €, le net imposable sera d'environ 2 058 €.</p>
                <p>C'est ce montant qui figure dans votre déclaration de revenus pré-remplie et qui détermine votre tranche d'imposition. La CSG déductible (6,80%) est bien déduite du net imposable, contrairement à la CSG non déductible et à la CRDS.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Le prélèvement à la source (PAS)</h2>
                <p>Le <strong>prélèvement à la source</strong> est l'impôt sur le revenu prélevé mensuellement sur votre salaire. Il est calculé en appliquant un taux à votre <strong>net imposable</strong>. Ce taux est déterminé par l'administration fiscale en fonction de vos revenus de l'année N-2 (revenus 2024 pour l'impôt 2026).</p>
                <p>Le prélèvement à la source ne modifié pas le montant total de votre impôt annuel, il modifié seulement la façon dont vous le payez : mensuellement via votre employeur plutôt qu'en une ou plusieurs fois l'année suivante.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Trois options de taux</h3>
                <p>Vous pouvez choisir entre trois types de taux de prélèvement à la source :</p>
                <ul class="space-y-3">
                    <li><strong>Taux personnalisé (par défaut)</strong> : calculé sur les revenus globaux de votre foyer fiscal. C'est le taux appliqué automatiquement. Il est identique pour tous les membres du foyer. Par exemple, si votre foyer à un taux de 7,5%, chacun des conjoints se verra appliquer 7,5% sur son net imposable.</li>
                    <li><strong>Taux individualisé</strong> : option pour les couples avec des revenus très différents. Chaque conjoint à un taux différent, proportionnel à ses revenus. Cela évite qu'un conjoint avec des revenus modestes se voie appliquer un taux élevé lié aux hauts revenus de l'autre. À demander sur votre espace impots.gouv.fr.</li>
                    <li><strong>Taux neutre</strong> : grille par défaut si vous ne souhaitez pas communiquer votre taux à votre employeur (par exemple pour préserver la confidentialité de votre situation familiale). Ce taux ne tient compte que de votre salaire individuel. À la fin de l'année, une régularisation aura lieu pour ajuster à votre taux réel. Demandable sur impots.gouv.fr.</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Modulation du taux en cours d'année</h3>
                <p>Vous pouvez modifier votre taux de prélèvement à tout moment sur votre espace impots.gouv.fr si votre situation change (baisse de revenus, naissance, mariage, divorce, etc.). Cette modulation vous permet d'ajuster immédiatement votre prélèvement sans attendre la déclaration de revenus de l'année suivante.</p>
                <p>En cas de baisse de revenus d'au moins 10%, vous pouvez demander une baisse de votre taux. En cas de hausse, vous pouvez volontairement augmenter votre taux pour éviter un reste à payer important en septembre de l'année suivante.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Barème de l'impôt sur le revenu 2026</h2>
                <p>Le prélèvement à la source est calculé selon le barème progressif de l'impôt sur le revenu. Voici les tranches applicables en 2026 (pour les revenus 2025) :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Tranche de revenu annuel</th>
                        <th class="py-2 text-right">Taux d'imposition</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Jusqu'à 11 497 €</td><td class="py-2 text-right">0%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 11 498 € à 29 315 €</td><td class="py-2 text-right">11%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 29 316 € à 83 823 €</td><td class="py-2 text-right">30%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 83 824 € à 180 294 €</td><td class="py-2 text-right">41%</td></tr>
                        <tr><td class="py-2">Au-delà de 180 294 €</td><td class="py-2 text-right">45%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Ces tranches s'appliquent au revenu imposable par part fiscale (quotient familial). Un couple marié ou pacsé sans enfant à 2 parts, chaque enfant ajoute 0,5 part (1 part à partir du 3ème enfant).</p>
                <p><strong>Exemple</strong> : Pour un célibataire (1 part) avec 30 000 € de revenu imposable annuel, le calcul est : 0% sur 11 497 € + 11% sur (29 315 - 11 497) + 30% sur (30 000 - 29 315) = 0 + 1 960 + 206 = <strong>2 166 € d'impôt annuel</strong>, soit un taux moyen de 7,2%.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exemples concrets à différents niveaux de salaire</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Salaire de 2 000 € brut mensuel (non-cadre, célibataire)</h3>
                <ul class="space-y-1">
                    <li>Net avant impôt : ~1 560 €</li>
                    <li>Net imposable annuel : ~19 331 €</li>
                    <li>Impôt annuel estimé : ~878 € (tranche 11%)</li>
                    <li>Prélèvement mensuel (~4,5%) : ~73 €</li>
                    <li><strong>Net après impôt : ~1 487 €</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Salaire de 3 000 € brut mensuel (non-cadre, célibataire)</h3>
                <ul class="space-y-1">
                    <li>Net avant impôt : ~2 340 €</li>
                    <li>Net imposable annuel : ~29 006 €</li>
                    <li>Impôt annuel estimé : ~1 954 € (tranche 11%)</li>
                    <li>Prélèvement mensuel (~6,7%) : ~163 €</li>
                    <li><strong>Net après impôt : ~2 177 €</strong></li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Salaire de 4 500 € brut mensuel (cadre, célibataire)</h3>
                <ul class="space-y-1">
                    <li>Net avant impôt : ~3 375 €</li>
                    <li>Net imposable annuel : ~41 832 €</li>
                    <li>Impôt annuel estimé : ~5 747 € (tranche 30%)</li>
                    <li>Prélèvement mensuel (~13,7%) : ~479 €</li>
                    <li><strong>Net après impôt : ~2 896 €</strong></li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Optimiser votre net après impôt</h2>
                <p>Plusieurs leviers légaux permettent de réduire votre impôt et donc d'augmenter votre net après impôt :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Versements sur un Plan d'Épargne Retraite (PER)</h3>
                <p>Les versements volontaires sur un PER sont déductibles de votre revenu imposable, dans la limite de 10% de vos revenus professionnels. Pour un salaire net imposable de 40 000 €, vous pouvez déduire jusqu'à 4 000 € de versements PER, ce qui réduit votre impôt de 1 200 € si vous êtes dans la tranche à 30%.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Dons aux associations</h3>
                <p>Les dons aux œuvres d'intérêt général ouvrent droit à une réduction d'impôt de 66% du montant versé (dans la limite de 20% du revenu imposable). Un don de 300 € réduit votre impôt de 198 €.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Emploi à domicile</h3>
                <p>Les dépenses pour l'emploi d'un salarié à domicile (ménage, garde d'enfants, soutien scolaire, jardinage, etc.) donnent droit à un crédit d'impôt de 50% dans la limite de 12 000 € de dépenses annuelles (soit 6 000 € de crédit d'impôt maximum).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Investissements défiscalisants</h3>
                <p>Dispositifs Pinel, Denormandie, FCPI, FIP : ces placements donnent droit à des réductions d'impôt en contrepartie d'un engagement de durée. À étudier avec un conseiller fiscal.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux neutre vs taux personnalisé : que choisir ?</h2>
                <p>Le choix entre taux neutre et taux personnalisé dépend de votre situation :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages du taux personnalisé</h3>
                <ul class="space-y-2">
                    <li>Prélèvement au plus juste : pas de régularisation importante en fin d'année</li>
                    <li>Pas de surprise fiscale en septembre</li>
                    <li>Meilleure visibilité sur votre pouvoir d'achat mensuel réel</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages du taux neutre</h3>
                <ul class="space-y-2">
                    <li>Confidentialité : votre employeur ne connaît pas votre situation familiale globale</li>
                    <li>Utile en cas de revenus du conjoint très élevés : évite un taux trop élevé visible par l'employeur</li>
                    <li>Trésorerie : si le taux neutre est inférieur à votre taux réel, vous payez moins chaque mois (mais devrez régulariser en septembre)</li>
                </ul>

                <p class="mt-4">Dans la majorité des cas, le taux personnalisé est plus avantageux car il évite les mauvaises surprises. Le taux neutre est pertinent surtout pour des raisons de confidentialité.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Grille du taux neutre 2026</h2>
                <p>Si vous optez pour le taux neutre, voici la grille applicable en 2026 (taux appliqué selon le net imposable mensuel) :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Net imposable mensuel</th>
                        <th class="py-2 text-right">Taux de prélèvement</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Jusqu'à 1 591 €</td><td class="py-2 text-right">0%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 1 591 € à 1 721 €</td><td class="py-2 text-right">0,5%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 1 721 € à 1 888 €</td><td class="py-2 text-right">1,3%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 1 888 € à 2 075 €</td><td class="py-2 text-right">2,1%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 2 075 € à 2 489 €</td><td class="py-2 text-right">2,9%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 2 489 € à 2 829 €</td><td class="py-2 text-right">3,5%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 2 829 € à 3 389 €</td><td class="py-2 text-right">4,1%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 3 389 € à 4 211 €</td><td class="py-2 text-right">5,3%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 4 211 € à 5 553 €</td><td class="py-2 text-right">7,5%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 5 553 € à 8 059 €</td><td class="py-2 text-right">9,9%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">De 8 059 € à 13 522 €</td><td class="py-2 text-right">11,9%</td></tr>
                        <tr><td class="py-2">Au-delà de 13 522 €</td><td class="py-2 text-right">20% puis 24% puis 33% puis 38% puis 43%</td></tr>
                    </tbody>
                </table>
            """
        },
        {
            "slug": "coût-employeur",
            "title": "Coût Employeur 2026 : Super-Brut et Charges Patronales",
            "desc": "Calculez le coût total employeur (super-brut) en 2026. Détail de chaque cotisation patronale, charges sociales complètes et simulateur gratuit instantané.",
            "kw": "coût employeur, super brut, charges patronales, cotisations patronales, coût salarié entreprise",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Qu'est-ce que le coût employeur ?</h2>
                <p>Le <strong>coût employeur</strong> (ou "super-brut") est le montant total que l'entreprise dépense pour employer un salarié. Il comprend le salaire brut inscrit au contrat + les cotisations sociales patronales. En moyenne, le coût employeur représente environ <strong>1,42 à 1,45 fois le salaire brut</strong> pour un salarié au SMIC ou salaire moyen, et jusqu'à 1,48 fois pour les hauts salaires.</p>
                <p>Ces cotisations patronales financent la protection sociale (santé, retraite, chômage, famille) au même titre que les cotisations salariales, mais elles sont payées directement par l'employeur et n'apparaissent pas sur votre bulletin de salaire en tant que retenues. Elles constituent un coût "invisible" pour le salarié mais très significatif pour l'entreprise.</p>
                <p>Comprendre le coût employeur est essentiel pour les employeurs lors du recrutement (budgétisation du poste), pour les salariés lors de négociations salariales (comprendre la marge de manœuvre de l'employeur), et pour les créateurs d'entreprise (évaluer le coût réel d'une embauche).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cotisations patronales 2026 : détail complet</h2>
                <p>Voici le détail de toutes les cotisations patronales en vigueur en 2026 :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Cotisation</th><th class="py-2 text-right">Taux patronal</th><th class="py-2 text-right">Assiette</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Maladie-maternité-invalidité-décès</td><td class="py-2 text-right">7,00%</td><td class="py-2 text-right">Totalité</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Vieillesse plafonnée</td><td class="py-2 text-right">8,55%</td><td class="py-2 text-right">Tranche 1 (≤ PSS)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Vieillesse déplafonnée</td><td class="py-2 text-right">2,02%</td><td class="py-2 text-right">Totalité</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Allocations familiales (taux réduit)</td><td class="py-2 text-right">3,45%</td><td class="py-2 text-right">Totalité (si masse salariale &lt; 3,5 SMIC)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Allocations familiales (taux normal)</td><td class="py-2 text-right">5,25%</td><td class="py-2 text-right">Totalité (sinon)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Assurance chômage</td><td class="py-2 text-right">4,05%</td><td class="py-2 text-right">Tranche A (≤ 4 PSS)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">AGIRC-ARRCO Tranche 1</td><td class="py-2 text-right">4,72%</td><td class="py-2 text-right">Tranche 1 (≤ PSS)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">AGIRC-ARRCO Tranche 2</td><td class="py-2 text-right">12,95%</td><td class="py-2 text-right">Tranche 2 (PSS à 8 PSS)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CEG Tranche 1</td><td class="py-2 text-right">1,29%</td><td class="py-2 text-right">Tranche 1</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CEG Tranche 2</td><td class="py-2 text-right">1,62%</td><td class="py-2 text-right">Tranche 2</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">CET (cadres uniquement)</td><td class="py-2 text-right">0,21%</td><td class="py-2 text-right">Totalité</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Accidents du travail / Maladies professionnelles</td><td class="py-2 text-right">0,5% à 3%</td><td class="py-2 text-right">Totalité (varie selon secteur)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">FNAL (Fonds National d'Aide au Logement)</td><td class="py-2 text-right">0,10% ou 0,50%</td><td class="py-2 text-right">Selon taille entreprise</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Contribution solidarité autonomie</td><td class="py-2 text-right">0,30%</td><td class="py-2 text-right">Totalité</td></tr>
                        <tr><td class="py-2">Versement transport</td><td class="py-2 text-right">Variable</td><td class="py-2 text-right">Selon localisation (0 à 2,95%)</td></tr>
                    </tbody>
                </table>
                <p class="mt-4"><strong>Total approximatif</strong> : entre 42% et 45% du salaire brut selon le niveau de salaire, le secteur d'activité (taux AT/MP), la taille de l'entreprise et la localisation (versement transport).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du coût employeur à différents niveaux de salaire</h2>
                <p>Le coût employeur varie selon le niveau de rémunération en raison des allègements de charges et des tranches de cotisations. Voici des exemples détaillés :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">SMIC (1 802 € brut mensuel)</h3>
                <ul class="space-y-1">
                    <li>Salaire brut : 1 802 €</li>
                    <li>Cotisations patronales théoriques : ~760 € (42%)</li>
                    <li>Réduction générale (ex-réduction Fillon) : ~495 €</li>
                    <li><strong>Coût employeur réel : ~2 067 €</strong> (soit 1,15× le brut grâce aux allègements)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2 000 € brut mensuel (non-cadre)</h3>
                <ul class="space-y-1">
                    <li>Salaire brut : 2 000 €</li>
                    <li>Cotisations patronales : ~840 € (42%)</li>
                    <li>Réduction générale : ~350 €</li>
                    <li><strong>Coût employeur : ~2 490 €</strong> (soit 1,25× le brut)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2 500 € brut mensuel (non-cadre)</h3>
                <ul class="space-y-1">
                    <li>Salaire brut : 2 500 €</li>
                    <li>Cotisations patronales : ~1 050 € (42%)</li>
                    <li>Réduction générale : ~100 €</li>
                    <li><strong>Coût employeur : ~3 450 €</strong> (soit 1,38× le brut)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3 500 € brut mensuel (cadre)</h3>
                <ul class="space-y-1">
                    <li>Salaire brut : 3 500 €</li>
                    <li>Cotisations patronales : ~1 540 € (44%)</li>
                    <li>Réduction générale : 0 € (au-delà du seuil)</li>
                    <li><strong>Coût employeur : ~5 040 €</strong> (soit 1,44× le brut)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5 000 € brut mensuel (cadre)</h3>
                <ul class="space-y-1">
                    <li>Salaire brut : 5 000 €</li>
                    <li>Cotisations patronales : ~2 275 € (45,5%)</li>
                    <li>Réduction générale : 0 €</li>
                    <li><strong>Coût employeur : ~7 275 €</strong> (soit 1,46× le brut)</li>
                </ul>

                <p class="mt-4">On observe que le coefficient multiplicateur (coût employeur / brut) diminue pour les bas salaires grâce aux allègements de charges, puis augmente légèrement pour les hauts salaires en raison des taux de cotisations plus élevés sur la Tranche 2.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">La réduction générale de cotisations patronales (ex-réduction Fillon)</h2>
                <p>La <strong>réduction générale</strong> (anciennement "réduction Fillon") est un dispositif d'allègement de charges patronales qui s'appliqué automatiquement aux salaires inférieurs à 1,6 SMIC (soit 2 883 € brut en 2026). Cette réduction est maximale au niveau du SMIC et décroît progressivement jusqu'à s'annuler à 1,6 SMIC.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul de la réduction générale</h3>
                <p>Le montant de la réduction dépend du coefficient de réduction, calculé selon la formule :</p>
                <p><strong>Coefficient = (T/0,6) × [(1,6 × SMIC annuel / rémunération annuelle brute) - 1]</strong></p>
                <p>Où T = 0,3245 (valeur 2026). Le coefficient maximal est donc de 0,3245 au SMIC, et il décroît linéairement.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Impact sur le coût employeur</h3>
                <p>Grâce à la réduction générale, le coût employeur au niveau du SMIC n'est que de 1,15× le brut au lieu de 1,42×. Cette mesure vise à favoriser l'emploi des salariés peu qualifiés et à réduire le coût du travail pour les PME.</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Salaire brut</th>
                        <th class="py-2 text-right">Coefficient multiplicateur</th>
                        <th class="py-2 text-right">Réduction générale</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">1,0 SMIC (1 802 €)</td><td class="py-2 text-right">1,15×</td><td class="py-2 text-right">~495 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">1,2 SMIC (2 162 €)</td><td class="py-2 text-right">1,27×</td><td class="py-2 text-right">~290 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">1,4 SMIC (2 523 €)</td><td class="py-2 text-right">1,37×</td><td class="py-2 text-right">~90 €</td></tr>
                        <tr><td class="py-2">≥ 1,6 SMIC (2 883 €)</td><td class="py-2 text-right">1,42-1,48×</td><td class="py-2 text-right">0 €</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différences de coût employeur : cadre vs non-cadre</h2>
                <p>Le statut cadre entraîne des cotisations patronales légèrement plus élevées, notamment :</p>
                <ul class="space-y-2">
                    <li><strong>CET patronale</strong> (0,21%) : cotisation spécifique aux cadres</li>
                    <li><strong>Garantie Minimale de Points (GMP)</strong> : forfait AGIRC-ARRCO pour les cadres dont le salaire est inférieur à 4 116 € brut (120 points minimum par an)</li>
                    <li><strong>Prévoyance cadre obligatoire</strong> : 1,50% minimum de la Tranche A (non inclus dans les taux ci-dessus, dépend de l'accord d'entreprise)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple comparatif à 3 500 € brut</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Élément</th>
                        <th class="py-2 text-right">Non-cadre</th>
                        <th class="py-2 text-right">Cadre</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Salaire brut</td><td class="py-2 text-right">3 500 €</td><td class="py-2 text-right">3 500 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Cotisations patronales</td><td class="py-2 text-right">~1 505 € (43%)</td><td class="py-2 text-right">~1 540 € (44%)</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Prévoyance obligatoire</td><td class="py-2 text-right">Variable</td><td class="py-2 text-right">~58 € minimum</td></tr>
                        <tr><td class="py-2"><strong>Coût employeur total</strong></td><td class="py-2 text-right"><strong>~5 005 €</strong></td><td class="py-2 text-right"><strong>~5 098 €</strong></td></tr>
                    </tbody>
                </table>
                <p class="mt-4">La différence de coût est faible (environ 2%), mais elle s'accumule sur l'année : ~1 116 € de différence annuelle sur cet exemple.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Autres coûts employeur au-delà des cotisations</h2>
                <p>Le coût total d'un salarié pour l'entreprise ne se limite pas au super-brut. Il faut aussi prendre en compte :</p>
                <ul class="space-y-2">
                    <li><strong>Mutuelle d'entreprise obligatoire</strong> : 50% minimum pris en charge par l'employeur, soit environ 25 à 40 € par mois</li>
                    <li><strong>Tickets restaurant</strong> : 50 à 60% pris en charge par l'employeur, soit 50 à 60 € par mois</li>
                    <li><strong>Prévoyance complémentaire</strong> : variable selon les conventions collectives</li>
                    <li><strong>Formation professionnelle</strong> : contribution obligatoire (0,55% à 1% de la masse salariale)</li>
                    <li><strong>Taxe d'apprentissage</strong> : 0,68% de la masse salariale</li>
                    <li><strong>Participation à l'effort de construction</strong> : 0,45% pour les entreprises de 50 salariés et +</li>
                    <li><strong>Coûts indirects</strong> : équipement informatique, bureau, outils de travail</li>
                </ul>
                <p class="mt-4">En tenant compte de tous ces éléments, le coût réel total d'un salarié peut atteindre <strong>1,6 à 1,8 fois le salaire brut</strong>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact pour l'employeur : de l'embauche à la négociation</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Lors d'un recrutement</h3>
                <p>Un employeur qui budgétise un poste à 4 000 € mensuels doit prévoir un coût employeur d'environ 5 760 € par mois (en comptant les cotisations patronales), soit <strong>69 120 € par an</strong>. Auxquels s'ajoutent les primes de fin d'année, les congés payés, les RTT, etc.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Lors d'une négociation salariale</h3>
                <p>Lorsqu'un salarié demande une augmentation de 200 € brut, le coût réel pour l'employeur est d'environ <strong>284 €</strong> (200 € + 42% de charges). Sur l'année, cela représente 3 408 € de coût supplémentaire pour l'entreprise, pour seulement 1 872 € net de plus pour le salarié (156 € × 12).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Stratégies d'optimisation</h3>
                <p>Les entreprises peuvent optimiser le coût employeur en jouant sur plusieurs leviers :</p>
                <ul class="space-y-2">
                    <li><strong>Prime de Partage de la Valeur (PPV)</strong> : exonérée de cotisations dans la limite de 3 000 ou 6 000 € selon les cas</li>
                    <li><strong>Intéressement et participation</strong> : exonérés de cotisations patronales (sauf forfait social de 20% dans certains cas)</li>
                    <li><strong>Titres-restaurant, chèques-vacances</strong> : exonérés de cotisations dans certaines limites</li>
                    <li><strong>Prise en charge des frais de transport</strong> : exonérée jusqu'à 75% de l'abonnement</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Tableau récapitulatif coût employeur 2026</h2>
                """ + generate_conversion_table([1802, 2000, 2500, 3000, 3500, 4000, 5000, 6000], "non-cadre") + """
                <p class="mt-4 text-sm text-slate-600">Note : Ces montants sont indicatifs et ne tiennent pas compte des cotisations conventionnelles spécifiques, de la mutuelle, des tickets restaurant, ni du versement transport qui varie selon la localisation de l'entreprise.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques</h2>
                <ul class="space-y-3">
                    <li><strong>Pour les salariés</strong> : Comprendre le coût employeur vous aide à mieux négocier. Au lieu de demander "200 € de plus", vous pouvez proposer un package global (rémunération + avantages) qui coûte moins cher à l'employeur tout en vous étant plus favorable fiscalement.</li>
                    <li><strong>Pour les employeurs</strong> : Anticipez le coût réel lors des budgets de recrutement. Un poste à 40 000 € brut annuel coûtera plutôt 57 000 à 60 000 € charges comprises.</li>
                    <li><strong>Pour les créateurs d'entreprise</strong> : Votre première embauche coûtera environ 1,4 fois le brut affiché. Prévoyez une trésorerie suffisante.</li>
                    <li><strong>Utilisez notre calculateur</strong> : Pour estimer précisément le coût employeur selon votre situation, utilisez notre <a href="/calculateur-cout-employeur/" class="text-brand-600 hover:text-brand-700">calculateur coût employeur gratuit</a>.</li>
                </ul>
            """
        },
        {
            "slug": "lire-fiche-de-paie",
            "title": "Comprendre sa Fiche de Paie 2026 : Guide Ligne par Ligne",
            "desc": "Guide complet pour lire et comprendre votre fiche de paie en 2026. Chaque ligne expliquée : salaire brut, cotisations salariales, net imposable et net à payer.",
            "kw": "comprendre fiche de paie, lire bulletin de salaire, explication fiche de paie, bulletin de paie 2026",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Pourquoi comprendre sa fiche de paie ?</h2>
                <p>Votre <strong>bulletin de salaire</strong> est un document essentiel qui récapitule votre rémunération et vos droits sociaux. Savoir le lire vous permet de vérifier que vous êtes payé correctement, de comprendre vos cotisations sociales, de détecter d'éventuelles erreurs et de préparer votre déclaration d'impôts. C'est aussi un document juridique à conserver sans limite de durée.</p>
                <p>Depuis 2018, les fiches de paie ont été simplifiées pour être plus lisibles. Les cotisations sont regroupées par thématique (santé, retraite, chômage) plutôt que par organisme collecteur. Malgré cette simplification, le bulletin reste complexe. Ce guide vous aide à décrypter chaque section.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Les 6 zones de votre fiche de paie</h2>
                <p>Votre bulletin se divise en plusieurs zones distinctes, chacune ayant un rôle précis. Voici un guide pour comprendre chacune d'entre elles.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. En-tête : identification employeur et salarié</h3>
                <p>Cette zone contient les informations légales obligatoires :</p>
                <ul class="space-y-2">
                    <li><strong>Informations employeur</strong> : raison sociale, adresse, numéro SIRET (14 chiffres), code APE/NAF (activité de l'entreprise), numéro d'identification URSSAF</li>
                    <li><strong>Convention collective applicable</strong> : indique quelle convention régit votre contrat (métallurgie, commerce, syntec, etc.). Important car elle définit vos droits (primes, grilles salariales, classifications)</li>
                    <li><strong>Informations salarié</strong> : nom, prénom, numéro de Sécurité sociale (NIR), emploi occupé, classification/coefficient (selon la convention collective), date d'entrée, ancienneté</li>
                    <li><strong>Période et date de paiement</strong> : mois concerné et date de versement du salaire</li>
                </ul>
                <p><strong>À vérifier</strong> : que votre classification correspond à votre poste réel. Une mauvaise classification peut vous priver de certaines primes ou d'une rémunération minimale conventionnelle supérieure au SMIC.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Rémunération brute</h3>
                <p>Cette section détaille tous les éléments qui composent votre salaire brut avant toute déduction :</p>
                <ul class="space-y-2">
                    <li><strong>Salaire de base</strong> : rémunération contractuelle, souvent exprimée en "Nombre d'heures × Taux horaire" ou en "Salaire mensuel forfaitaire"</li>
                    <li><strong>Heures supplémentaires</strong> : heures au-delà de 35h/semaine (ou durée conventionnelle), avec majoration de 25% ou 50%</li>
                    <li><strong>Heures complémentaires</strong> : pour les temps partiels, avec majoration de 10% à 25%</li>
                    <li><strong>Primes</strong> : ancienneté, objectifs, 13ème mois, prime exceptionnelle, etc.</li>
                    <li><strong>Avantages en nature</strong> : valeur forfaitaire de la voiture de fonction, du logement, des repas, etc. (ajouté au brut puis retiré du net)</li>
                    <li><strong>Indemnités</strong> : transport, télétravail, panier repas (si non exonérées)</li>
                </ul>
                <p><strong>Total brut</strong> : somme de tous ces éléments. C'est la base de calcul des cotisations sociales.</p>
                <p><strong>À vérifier</strong> : le nombre d'heures travaillées, le taux horaire (doit correspondre au contrat et à la grille conventionnelle), les primes dues (vérifiez votre convention collective).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Cotisations sociales : le cœur de la fiche de paie</h3>
                <p>Depuis 2018, les cotisations sont présentées de façon simplifiée et regroupées en 5 grandes catégories (ou "risques"). Pour chaque ligne, vous voyez : la base de calcul, le taux salarial, le montant salarial, le taux patronal, le montant patronal.</p>

                <h4 class="font-semibold text-slate-900 mt-4">A. Santé</h4>
                <ul class="space-y-1">
                    <li><strong>Maladie-maternité-invalidité-décès</strong> : cotisation patronale uniquement (7% du brut). Finance l'assurance maladie (remboursements de soins, indemnités journalières).</li>
                    <li><strong>Complémentaire santé (mutuelle)</strong> : cotisation patronale (minimum 50% du coût) + part salariale éventuelle. Obligatoire dans toutes les entreprises.</li>
                </ul>

                <h4 class="font-semibold text-slate-900 mt-4">B. Accidents du travail / Maladies professionnelles</h4>
                <ul class="space-y-1">
                    <li><strong>AT/MP</strong> : cotisation patronale uniquement (0,5% à 3% selon le risque du secteur). Finance les indemnisations en cas d'accident du travail.</li>
                </ul>

                <h4 class="font-semibold text-slate-900 mt-4">C. Retraite</h4>
                <ul class="space-y-1">
                    <li><strong>Vieillesse plafonnée</strong> : 6,90% salarial + 8,55% patronal sur la Tranche 1 (jusqu'à 3 864 €). Finance la retraite de base du régime général.</li>
                    <li><strong>Vieillesse déplafonnée</strong> : 0,40% salarial + 2,02% patronal sur la totalité du salaire.</li>
                    <li><strong>Retraite complémentaire AGIRC-ARRCO</strong> : 3,15% salarial + 4,72% patronal sur T1 ; 8,64% salarial + 12,95% patronal sur T2. Vous donne des points de retraite complémentaire.</li>
                    <li><strong>CEG (Contribution d'Équilibre Générale)</strong> : 0,86% à 1,08% salarial + 1,29% à 1,62% patronal. Équilibre les comptes AGIRC-ARRCO.</li>
                    <li><strong>CET (cadres uniquement)</strong> : 0,14% salarial + 0,21% patronal. Finance la Garantie Minimale de Points des cadres.</li>
                </ul>

                <h4 class="font-semibold text-slate-900 mt-4">D. Famille</h4>
                <ul class="space-y-1">
                    <li><strong>Allocations familiales</strong> : cotisation patronale uniquement (3,45% ou 5,25%). Finance les prestations familiales (allocations, CAF).</li>
                </ul>

                <h4 class="font-semibold text-slate-900 mt-4">E. Assurance chômage</h4>
                <ul class="space-y-1">
                    <li><strong>Chômage</strong> : cotisation patronale uniquement (4,05%). Finance Pôle emploi et les allocations chômage. Depuis 2018, il n'y a plus de part salariale.</li>
                </ul>

                <h4 class="font-semibold text-slate-900 mt-4">F. Autres contributions (CSG/CRDS)</h4>
                <ul class="space-y-1">
                    <li><strong>CSG déductible</strong> : 6,80% sur 98,25% du brut. Déductible du revenu imposable.</li>
                    <li><strong>CSG non déductible</strong> : 2,40% sur 98,25% du brut. Non déductible fiscalement.</li>
                    <li><strong>CRDS</strong> : 0,50% sur 98,25% du brut. Rembourse la dette sociale.</li>
                </ul>

                <p class="mt-4"><strong>Total des cotisations salariales</strong> : environ 22% du brut (non-cadre) ou 25% (cadre). Ce total est retranché du brut pour obtenir le net avant impôt.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Net imposable et prélèvement à la source</h3>
                <p>Après les cotisations sociales, plusieurs montants "nets" apparaissent :</p>
                <ul class="space-y-2">
                    <li><strong>Net à payer avant impôt sur le revenu</strong> : c'est le "salaire net" classique = brut - cotisations salariales.</li>
                    <li><strong>Net imposable</strong> : net à payer + CSG non déductible + CRDS. Sert de base au calcul de l'impôt. C'est ce montant qui apparaît dans votre déclaration de revenus pré-remplie.</li>
                    <li><strong>Impôt sur le revenu prélevé à la source</strong> : montant de l'impôt retenu ce mois-ci (= net imposable × taux de prélèvement).</li>
                    <li><strong>Net à payer (en euros)</strong> : c'est le montant final viré sur votre compte = net avant impôt - prélèvement à la source - éventuelles autres retenues (saisie sur salaire, acompte, etc.).</li>
                </ul>
                <p><strong>À vérifier</strong> : que votre taux de prélèvement à la source correspond bien à celui communiqué par les impôts. Un taux erroné peut créer un reste à payer important en septembre.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5. Net à payer et mode de paiement</h3>
                <p>Cette zone indique :</p>
                <ul class="space-y-1">
                    <li><strong>Net à payer en euros</strong> : montant final versé (gros caractère, mis en évidence)</li>
                    <li><strong>Mode de paiement</strong> : virement bancaire (RIB utilisé), chèque (rare désormais)</li>
                    <li><strong>Date de paiement</strong> : jour de mise à disposition des fonds</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">6. Cumuls annuels (depuis le 1er janvier)</h3>
                <p>En bas de la fiche de paie, vous trouvez les totaux cumulés depuis le début de l'année civile :</p>
                <ul class="space-y-2">
                    <li><strong>Brut cumulé</strong> : somme de tous vos salaires bruts depuis janvier</li>
                    <li><strong>Cotisations salariales cumulées</strong> : total des cotisations prélevées</li>
                    <li><strong>Net imposable cumulé</strong> : base d'imposition annuelle (utile pour votre déclaration de revenus)</li>
                    <li><strong>Impôt cumulé prélevé à la source</strong> : total de l'impôt retenu depuis janvier</li>
                    <li><strong>Congés payés</strong> : jours acquis, jours pris, solde restant</li>
                    <li><strong>RTT</strong> : jours acquis, jours pris, solde (si applicable)</li>
                </ul>
                <p><strong>Utilité</strong> : ces cumuls vous permettent de vérifier votre déclaration de revenus pré-remplie, de suivre votre rémunération annuelle et de connaître votre solde de congés.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Walkthrough : exemple de fiche de paie décryptée</h2>
                <p>Prenons l'exemple d'une fiche de paie fictive pour mieux comprendre :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Profil</h3>
                <ul class="space-y-1">
                    <li>Salarié : Marie Dupont, cadre</li>
                    <li>Salaire brut mensuel : 3 500 €</li>
                    <li>Prime d'ancienneté : 200 €</li>
                    <li>Tickets restaurant : 100 € (60% employeur)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Section Rémunération brute</h3>
                <ul class="space-y-1">
                    <li>Salaire de base : 3 500,00 €</li>
                    <li>Prime d'ancienneté : 200,00 €</li>
                    <li><strong>Total brut</strong> : 3 700,00 €</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Section Cotisations</h3>
                <ul class="space-y-1">
                    <li>Santé (mutuelle part salariale) : -30,00 €</li>
                    <li>Vieillesse plafonnée (6,90%) : -252,34 €</li>
                    <li>Vieillesse déplafonnée (0,40%) : -14,80 €</li>
                    <li>AGIRC-ARRCO T1 (3,15%) : -115,29 €</li>
                    <li>CEG T1 (0,86%) : -31,48 €</li>
                    <li>CET cadre (0,14%) : -5,18 €</li>
                    <li>CSG déductible (6,80% × 98,25%) : -246,98 €</li>
                    <li>CSG non déductible (2,40% × 98,25%) : -87,16 €</li>
                    <li>CRDS (0,50% × 98,25%) : -18,16 €</li>
                    <li><strong>Total cotisations salariales</strong> : -801,39 € (21,66%)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Montants nets</h3>
                <ul class="space-y-1">
                    <li>Net à payer avant impôt : 2 898,61 €</li>
                    <li>+ CSG/CRDS non déductibles : +105,32 €</li>
                    <li><strong>Net imposable</strong> : 3 003,93 €</li>
                    <li>Prélèvement à la source (7,5%) : -225,29 €</li>
                    <li>Part salariale tickets restaurant : -40,00 €</li>
                    <li><strong>Net à payer final</strong> : 2 633,32 €</li>
                </ul>

                <p class="mt-4">Sur son compte bancaire, Marie recevra donc <strong>2 633,32 €</strong>. L'écart avec le brut (3 700 €) s'explique par les cotisations sociales (801 €), l'impôt (225 €) et les tickets restaurant (40 €).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Erreurs courantes à vérifier sur votre fiche de paie</h2>
                <p>Les erreurs de paie sont fréquentes. Voici les points de vigilance :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Taux horaire et heures travaillées</h3>
                <p>Vérifiez que le taux horaire correspond à votre contrat et que le nombre d'heures est exact. Une erreur d'une heure par mois représente 12 heures par an non payées.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Heures supplémentaires</h3>
                <p>Les heures sup doivent être majorées (au minimum +10%, souvent +25% ou +50%). Vérifiez le calcul : heures × taux horaire × coefficient de majoration.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Primes obligatoires</h3>
                <p>Consultez votre convention collective : certaines primes sont obligatoires (ancienneté, 13ème mois, panier repas). Leur absence est illégale.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Classification et coefficient</h3>
                <p>Votre classification doit correspondre à vos fonctions réelles. Une mauvaise classification peut vous priver d'un salaire minimum conventionnel plus élevé.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5. Congés payés</h3>
                <p>Vous devez acquérir 2,5 jours ouvrables par mois travaillé (soit 30 jours par an). Vérifiez le compteur.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">6. Avantages en nature</h3>
                <p>Si vous avez une voiture de fonction ou un logement, l'avantage doit être valorisé et apparaître : +X € en brut, puis -X € en net.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Fiche de paie papier vs dématérialisée</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Fiche de paie électronique (dématérialisée)</h3>
                <p>Depuis 2017, l'employeur peut vous envoyer votre fiche de paie par voie électronique (email, coffre-fort numérique), sauf opposition de votre part. Les avantages : archivage automatique, accessibilité à tout moment, écologie. Le format PDF doit être sécurisé et horodaté.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Conservation des fiches de paie</h3>
                <p>Vous devez <strong>conserver vos bulletins de salaire sans limite de durée</strong>. Ils servent de justificatifs pour :</p>
                <ul class="space-y-1">
                    <li>Le calcul de votre retraite (reconstitution de carrière)</li>
                    <li>Un prêt bancaire ou un dossier de location</li>
                    <li>Une demande d'allocations chômage ou de RSA</li>
                    <li>Un contentieux avec l'employeur (rappel de salaire, prud'hommes)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Obligations légales de l'employeur</h2>
                <p>L'employeur à l'obligation de vous remettre une fiche de paie <strong>à chaque versement de salaire</strong>, même si le montant est nul (absence non rémunérée). Le bulletin doit comporter toutes les mentions obligatoires sous peine de sanctions (amende de 450 €).</p>
                <p>Mentions obligatoires : identité employeur/salarié, période de paie, détail des éléments de rémunération, détail des cotisations, net imposable, net à payer, cumuls annuels, mention de conservation sans limite, mention de recours au CSE en cas de difficultés.</p>
                <p><strong>Mentions interdites</strong> : il est interdit de mentionner l'exercice du droit de grève ou l'activité de représentation du personnel.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Que faire en cas d'erreur ?</h2>
                <ol class="space-y-3">
                    <li><strong>1. Signalez rapidement</strong> : prévenez votre service RH ou paie dès que vous détectez une anomalie. Les corrections sont plus faciles à faire dans le mois en cours.</li>
                    <li><strong>2. Demandez un bulletin rectificatif</strong> : en cas d'erreur avérée, l'employeur doit émettre un bulletin de paie rectificatif. Conservez les deux versions.</li>
                    <li><strong>3. Rappel de salaire</strong> : si vous avez été sous-payé, vous pouvez demander un rappel de salaire. Le délai de prescription est de 3 ans.</li>
                    <li><strong>4. Recours au CSE</strong> : votre représentant du personnel peut vous assister dans vos démarches.</li>
                    <li><strong>5. Conseil de prud'hommes</strong> : en dernier recours, en cas de litige persistant sur votre rémunération.</li>
                </ol>
            """
        },
        {
            "slug": "smic-brut-net-2026",
            "title": "SMIC 2026 Brut et Net : Montant Mensuel, Horaire et Annuel",
            "desc": "SMIC 2026 : 1 801,80€ brut soit 1 426€ net par mois, 11,88€ brut de l'heure. Montant annuel, calcul détaillé des cotisations et évolution depuis 2020.",
            "kw": "smic 2026, smic brut net, smic mensuel 2026, smic horaire 2026, smic net",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Le SMIC en 2026 : définition et montants</h2>
                <p>Le <strong>SMIC</strong> (Salaire Minimum Interprofessionnel de Croissance) est le salaire horaire minimum légal en France. Aucun employeur ne peut vous payer en dessous de ce montant pour une heure de travail effectif (sauf exceptions très rares : apprentis mineurs, travailleurs handicapés avec autorisation). Le SMIC est revalorisé chaque année au 1er janvier, et peut faire l'objet de revalorisations exceptionnelles en cours d'année si l'inflation dépassé 2%.</p>
                <p>Le SMIC est un outil de politique sociale majeur : il garantit un revenu minimum aux salariés, lutte contre la pauvreté au travail et sert de référence pour de nombreuses prestations sociales (RSA, prime d'activité, APL). Il concerne environ 3 millions de salariés en France.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Montants du SMIC 2026</h2>
                <p>Au 1er janvier 2026, le SMIC a été revalorisé à <strong>11,88 € brut de l'heure</strong>. Voici les montants correspondants pour différentes durées de travail :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Période</th>
                        <th class="py-2 text-right">Brut</th>
                        <th class="py-2 text-right">Net avant impôt</th>
                        <th class="py-2 text-right">Net après impôt (0%)*</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Horaire</td><td class="py-2 text-right">11,88 €</td><td class="py-2 text-right">9,27 €</td><td class="py-2 text-right">9,27 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Journalier (7h)</td><td class="py-2 text-right">83,16 €</td><td class="py-2 text-right">64,89 €</td><td class="py-2 text-right">64,89 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Hebdomadaire (35h)</td><td class="py-2 text-right">415,80 €</td><td class="py-2 text-right">324,45 €</td><td class="py-2 text-right">324,45 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Mensuel (151,67h)</td><td class="py-2 text-right">1 801,80 €</td><td class="py-2 text-right">1 426 €</td><td class="py-2 text-right">1 426 €</td></tr>
                        <tr><td class="py-2">Annuel (1 820h)</td><td class="py-2 text-right">21 621,60 €</td><td class="py-2 text-right">17 112 €</td><td class="py-2 text-right">17 112 €</td></tr>
                    </tbody>
                </table>
                <p class="mt-2 text-sm text-slate-600">* Un salarié au SMIC seul et sans autres revenus n'est généralement pas imposable (sous le seuil de la première tranche à 11 497 € de revenu imposable par part).</p>

                <p class="mt-4"><strong>Calcul du SMIC mensuel</strong> : Le SMIC mensuel correspond à 151,67 heures × 11,88 € = 1 801,80 € brut. Les 151,67 heures représentent la durée légale mensuelle moyenne (35h × 52 semaines / 12 mois = 151,67h).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Évolution historique du SMIC (2019-2026)</h2>
                <p>Le SMIC a progressé de <strong>14,3% en 7 ans</strong>, principalement sous l'effet de l'inflation. Voici l'historique complet :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Année</th>
                        <th class="py-2 text-right">SMIC horaire brut</th>
                        <th class="py-2 text-right">SMIC mensuel brut</th>
                        <th class="py-2 text-right">Hausse annuelle</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">2026</td><td class="py-2 text-right">11,88 €</td><td class="py-2 text-right">1 801,80 €</td><td class="py-2 text-right">+2,0%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2025</td><td class="py-2 text-right">11,65 €</td><td class="py-2 text-right">1 766,92 €</td><td class="py-2 text-right">+1,1%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2024</td><td class="py-2 text-right">11,52 €</td><td class="py-2 text-right">1 747,20 €</td><td class="py-2 text-right">+1,1%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2023</td><td class="py-2 text-right">11,27 €</td><td class="py-2 text-right">1 709,28 €</td><td class="py-2 text-right">+1,8%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2022</td><td class="py-2 text-right">10,85 €</td><td class="py-2 text-right">1 645,58 €</td><td class="py-2 text-right">+0,9%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2021</td><td class="py-2 text-right">10,25 €</td><td class="py-2 text-right">1 554,58 €</td><td class="py-2 text-right">+0,99%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2020</td><td class="py-2 text-right">10,15 €</td><td class="py-2 text-right">1 539,42 €</td><td class="py-2 text-right">+1,2%</td></tr>
                        <tr><td class="py-2">2019</td><td class="py-2 text-right">10,03 €</td><td class="py-2 text-right">1 521,25 €</td><td class="py-2 text-right">+1,5%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Entre 2019 et 2026, le SMIC brut mensuel est passé de 1 521 € à 1 802 €, soit une augmentation de <strong>281 € brut par mois (+18,5%)</strong>. En termes de pouvoir d'achat réel, l'augmentation est plus modeste après prise en compte de l'inflation cumulée sur la période.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Qui gagne le SMIC en France ?</h2>
                <p>En 2026, environ <strong>3 millions de salariés</strong> sont rémunérés au SMIC ou très proche du SMIC (dans une fourchette de 1 à 1,05 SMIC), soit environ <strong>17% des salariés du secteur privé</strong>. Ce pourcentage varie fortement selon les secteurs et les profils.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Par secteur d'activité</h3>
                <ul class="space-y-2">
                    <li><strong>Hôtellerie-restauration</strong> : 45% des salariés au SMIC (serveurs, commis, agents d'entretien)</li>
                    <li><strong>Commerce de détail</strong> : 30% des salariés au SMIC (caissiers, vendeurs, employés de rayon)</li>
                    <li><strong>Services à la personne</strong> : 35% des salariés au SMIC (aides à domicile, assistantes maternelles)</li>
                    <li><strong>Agriculture</strong> : 25% des salariés au SMIC (ouvriers agricoles saisonniers)</li>
                    <li><strong>Industrie</strong> : 8% des salariés au SMIC (grâce aux grilles conventionnelles plus élevées)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Par profil démographique</h3>
                <ul class="space-y-2">
                    <li><strong>Jeunes de moins de 25 ans</strong> : 30% sont rémunérés au SMIC (premiers emplois, faible expérience)</li>
                    <li><strong>Femmes</strong> : 20% sont au SMIC, contre 14% des hommes (surreprésentation dans les secteurs à bas salaires)</li>
                    <li><strong>Temps partiel</strong> : 40% sont rémunérés au SMIC horaire (contre 12% des temps pleins)</li>
                    <li><strong>CDD et intérimaires</strong> : 25% sont au SMIC (contre 15% des CDI)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact du SMIC sur d'autres prestations sociales</h2>
                <p>Le SMIC sert de référence pour calculer de nombreuses prestations et aides sociales. Toute revalorisation du SMIC a donc des effets en cascade :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Prime d'activité</h3>
                <p>La prime d'activité est versée aux travailleurs modestes. Elle est maximale pour un SMIC et décroît jusqu'à environ 1,5 SMIC. Un salarié seul au SMIC peut toucher environ 200 € de prime d'activité par mois en 2026.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Aides au logement (APL)</h3>
                <p>Les plafonds de ressources pour bénéficier des APL sont indexés sur le SMIC. Une hausse du SMIC peut donc élargir le nombre de bénéficiaires.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. RSA</h3>
                <p>Le montant du RSA (635 € en 2026 pour une personne seule) est équivalent à environ <strong>44% du SMIC net</strong>. Cette proportion est restée stable au fil des revalorisations.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Plafonds de cotisations (réduction générale)</h3>
                <p>La réduction générale de cotisations patronales s'appliqué jusqu'à 1,6 SMIC (2 883 € brut en 2026). Au-delà, l'entreprise paie les cotisations pleines. Toute hausse du SMIC augmente donc le seuil d'exonération.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">SMIC vs salaire médian</h2>
                <p>Le <strong>salaire médian</strong> en France (celui qui divise les salariés en deux groupes égaux) est d'environ <strong>2 100 € brut mensuel</strong> en 2026, soit <strong>1,17 fois le SMIC</strong>. Cela signifie que la moitié des salariés gagnent moins de 2 100 € brut.</p>
                <p>Cette proximité entre SMIC et salaire médian est une spécificité française : dans d'autres pays, l'écart est plus important. Cela témoigne à la fois d'un SMIC relativement élevé et d'une compression de la hiérarchie salariale dans le bas de l'échelle.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exceptions et cas particuliers</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Apprentis et contrats de professionnalisation</h3>
                <p>Les apprentis perçoivent un pourcentage du SMIC selon leur âge et leur année de formation :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Âge / Année</th>
                        <th class="py-2 text-right">1ère année</th>
                        <th class="py-2 text-right">2ème année</th>
                        <th class="py-2 text-right">3ème année</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Moins de 18 ans</td><td class="py-2 text-right">27% SMIC</td><td class="py-2 text-right">39% SMIC</td><td class="py-2 text-right">55% SMIC</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">18-20 ans</td><td class="py-2 text-right">43% SMIC</td><td class="py-2 text-right">51% SMIC</td><td class="py-2 text-right">67% SMIC</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">21-25 ans</td><td class="py-2 text-right">53% SMIC*</td><td class="py-2 text-right">61% SMIC*</td><td class="py-2 text-right">78% SMIC*</td></tr>
                        <tr><td class="py-2">26 ans et +</td><td class="py-2 text-right">100% SMIC</td><td class="py-2 text-right">100% SMIC</td><td class="py-2 text-right">100% SMIC</td></tr>
                    </tbody>
                </table>
                <p class="mt-2 text-sm text-slate-600">* Ou pourcentage du salaire minimum conventionnel si plus favorable</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Jeunes de moins de 18 ans</h3>
                <p>Un abattement peut s'appliquer aux jeunes sans qualification :</p>
                <ul class="space-y-1">
                    <li>Moins de 17 ans : abattement de 10% (SMIC à 10,69 € brut/h)</li>
                    <li>17-18 ans : abattement de 10% si moins de 6 mois d'expérience</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Stagiaires</h3>
                <p>Les stagiaires ne sont pas soumis au SMIC mais à une <strong>gratification minimale de 15% du plafond horaire de la Sécurité sociale</strong>, soit <strong>4,35 € par heure</strong> en 2026 (pour les stages de plus de 2 mois).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaires minimums conventionnels</h2>
                <p>De nombreuses conventions collectives prévoient des <strong>salaires minimums supérieurs au SMIC</strong> pour certains postes. Par exemple :</p>
                <ul class="space-y-2">
                    <li><strong>Métallurgie</strong> : niveau I échelon 1 = 1 850 € brut (SMIC + 2,7%)</li>
                    <li><strong>Bâtiment</strong> : niveau I = 1 900 € brut (SMIC + 5,4%)</li>
                    <li><strong>Banques</strong> : niveau 1 = 2 100 € brut (SMIC + 16,5%)</li>
                </ul>
                <p>Si votre convention collective prévoit un minimum supérieur au SMIC pour votre classification, c'est ce minimum qui s'appliqué. Vérifiez votre grille conventionnelle !</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Peut-on vivre avec un SMIC en 2026 ?</h2>
                <p>Le SMIC net mensuel (1 426 €) permet de couvrir les besoins essentiels, mais laisse peu de marge pour l'épargne ou les imprévus. Voici un budget type :</p>
                <ul class="space-y-2">
                    <li>Loyer (hors Paris) : 600-800 € (avec APL)</li>
                    <li>Alimentation : 300 €</li>
                    <li>Transports : 80 € (abonnement + essence)</li>
                    <li>Assurances : 100 € (logement, voiture, santé)</li>
                    <li>Téléphone/Internet : 50 €</li>
                    <li>Énergie : 80 €</li>
                    <li><strong>Total charges fixes</strong> : ~1 210 €</li>
                    <li><strong>Reste pour vivre</strong> : ~216 €</li>
                </ul>
                <p>Heureusement, les salariés au SMIC peuvent bénéficier de la <strong>prime d'activité</strong> (~200 €/mois), qui porte le revenu disponible à environ 1 626 € net. Cela reste serré, surtout avec des enfants ou dans les grandes villes.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comment est calculée la revalorisation du SMIC ?</h2>
                <p>La revalorisation annuelle du SMIC au 1er janvier est calculée selon une formule légale qui prend en compte deux critères :</p>
                <ul class="space-y-2">
                    <li><strong>L'inflation mesurée pour les 20% de ménages les plus modestes</strong> : c'est l'indice des prix à la consommation (hors tabac) pondéré par la structure de consommation des ménages à bas revenus</li>
                    <li><strong>La moitié du gain de pouvoir d'achat du salaire horaire de base ouvrier et employé (SHBOE)</strong> : cette composante assure que le SMIC progresse avec les salaires</li>
                </ul>
                <p>Le gouvernement peut également décider d'un <strong>"coup de pouce"</strong> supplémentaire, c'est-à-dire une revalorisation allant au-delà de la formule légale. En pratique, aucun coup de pouce n'a été donné depuis 2012, les gouvernements successifs préférant s'en tenir à la formule automatique.</p>
                <p>Une revalorisation <strong>exceptionnelle en cours d'année</strong> est déclenchée automatiquement si l'inflation dépassé 2% depuis la dernière revalorisation. C'est ce qui s'est produit en mai 2022 et août 2022 en raison de la forte poussée inflationniste.</p>
            """
        },
        {
            "slug": "salaire-moyen-france",
            "title": "Salaire Moyen en France 2026 : Statistiques Brut et Net",
            "desc": "Salaire moyen et médian en France en 2026 : statistiques détaillées par âge, secteur d'activité et région. Brut et net comparés avec écarts cadre et non-cadre.",
            "kw": "salaire moyen france, salaire médian france, salaire moyen 2026, statistiques salaire",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Salaire moyen vs salaire médian : quelle différence ?</h2>
                <p>Le <strong>salaire moyen</strong> est la moyenne arithmétique de tous les salaires : on additionne tous les salaires et on divise par le nombre de salariés. Il est fortement tiré vers le haut par les très hauts revenus (dirigeants, cadres supérieurs). Par exemple, un seul salaire de 100 000 € dans un groupe de 10 personnes fait grimper artificiellement la moyenne.</p>
                <p>Le <strong>salaire médian</strong> est plus représentatif de la réalité : c'est le salaire qui divise les salariés en deux groupes égaux. 50% des salariés gagnent plus, 50% gagnent moins. Il n'est pas influencé par les valeurs extrêmes et donne une meilleure image du salaire "typique" en France.</p>
                <p><strong>Exemple concret</strong> : Si 9 personnes gagnent 2 000 € et 1 personne gagne 20 000 €, la moyenne est de 3 800 € (peu représentatif), mais la médiane est de 2 000 € (beaucoup plus réaliste).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Chiffres clés 2026 : secteur privé, temps plein</h2>
                <p>Voici les statistiques salariales nationales pour 2026, basées sur les données INSEE (équivalent temps plein, secteur privé) :</p>
                <ul class="space-y-2">
                    <li><strong>Salaire brut moyen</strong> : environ 2 630 € par mois</li>
                    <li><strong>Salaire net moyen avant impôt</strong> : environ 2 050 € par mois</li>
                    <li><strong>Salaire brut médian</strong> : environ 2 100 € par mois</li>
                    <li><strong>Salaire net médian avant impôt</strong> : environ 1 640 € par mois</li>
                </ul>
                <p><strong>Interprétation</strong> : Le salaire médian est nettement inférieur au salaire moyen (2 100 € vs 2 630 €), ce qui montre que la distribution des salaires est asymétrique, avec une concentration dans le bas de l'échelle et une longue queue de hauts salaires.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaire moyen par catégorie socioprofessionnelle</h2>
                <p>Les salaires varient considérablement selon la catégorie socioprofessionnelle (CSP). Voici les moyennes 2026 :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Catégorie</th>
                        <th class="py-2 text-right">Brut mensuel moyen</th>
                        <th class="py-2 text-right">Net mensuel moyen</th>
                        <th class="py-2 text-right">% de la population</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Cadres et professions intellectuelles supérieures</td><td class="py-2 text-right">4 500 €</td><td class="py-2 text-right">3 375 €</td><td class="py-2 text-right">19%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Professions intermédiaires</td><td class="py-2 text-right">2 600 €</td><td class="py-2 text-right">2 028 €</td><td class="py-2 text-right">26%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Employés</td><td class="py-2 text-right">1 900 €</td><td class="py-2 text-right">1 482 €</td><td class="py-2 text-right">28%</td></tr>
                        <tr><td class="py-2">Ouvriers</td><td class="py-2 text-right">2 000 €</td><td class="py-2 text-right">1 560 €</td><td class="py-2 text-right">22%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">L'écart entre cadres et employés est de <strong>2,4×</strong> en brut. Les cadres représentent près de 20% des salariés, mais captent une part disproportionnée de la masse salariale totale.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaire moyen par secteur d'activité</h2>
                <p>Les rémunérations varient fortement d'un secteur à l'autre. Voici un panorama des secteurs qui paient le mieux et le moins bien :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Secteurs les mieux rémunérés</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Secteur</th>
                        <th class="py-2 text-right">Brut mensuel moyen</th>
                        <th class="py-2 text-right">Net mensuel moyen</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Finance et assurance</td><td class="py-2 text-right">4 200 €</td><td class="py-2 text-right">3 150 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Information et communication (IT, médias)</td><td class="py-2 text-right">3 800 €</td><td class="py-2 text-right">2 850 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Activités scientifiques et techniques</td><td class="py-2 text-right">3 500 €</td><td class="py-2 text-right">2 625 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Énergie (électricité, gaz)</td><td class="py-2 text-right">3 400 €</td><td class="py-2 text-right">2 550 €</td></tr>
                        <tr><td class="py-2">Industrie pharmaceutique</td><td class="py-2 text-right">3 300 €</td><td class="py-2 text-right">2 475 €</td></tr>
                    </tbody>
                </table>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Secteurs les moins rémunérés</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Secteur</th>
                        <th class="py-2 text-right">Brut mensuel moyen</th>
                        <th class="py-2 text-right">Net mensuel moyen</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Hébergement et restauration</td><td class="py-2 text-right">1 850 €</td><td class="py-2 text-right">1 443 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Commerce de détail</td><td class="py-2 text-right">1 950 €</td><td class="py-2 text-right">1 521 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Services à la personne</td><td class="py-2 text-right">1 900 €</td><td class="py-2 text-right">1 482 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Agriculture</td><td class="py-2 text-right">1 950 €</td><td class="py-2 text-right">1 521 €</td></tr>
                        <tr><td class="py-2">Textile et habillement</td><td class="py-2 text-right">2 000 €</td><td class="py-2 text-right">1 560 €</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">L'écart entre le secteur le mieux payé (finance, 4 200 €) et le moins bien payé (hôtellerie-restauration, 1 850 €) est de <strong>2,3×</strong>. Ce facteur monte à plus de 3× si on compare les cadres de la finance aux employés de l'hôtellerie.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaire moyen par région</h2>
                <p>Les salaires varient aussi géographiquement, principalement en raison de la concentration d'emplois qualifiés dans certaines régions et du coût de la vie différencié.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Régions les mieux rémunérées</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Région</th>
                        <th class="py-2 text-right">Brut mensuel moyen</th>
                        <th class="py-2 text-right">Écart vs moyenne nationale</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Île-de-France</td><td class="py-2 text-right">3 200 €</td><td class="py-2 text-right">+22%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Auvergne-Rhône-Alpes</td><td class="py-2 text-right">2 550 €</td><td class="py-2 text-right">-3%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Provence-Alpes-Côte d'Azur</td><td class="py-2 text-right">2 500 €</td><td class="py-2 text-right">-5%</td></tr>
                        <tr><td class="py-2">Nouvelle-Aquitaine</td><td class="py-2 text-right">2 400 €</td><td class="py-2 text-right">-9%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">L'<strong>Île-de-France</strong> se démarque nettement avec un salaire moyen 22% supérieur à la moyenne nationale, mais le coût de la vie (logement surtout) y est également beaucoup plus élevé (+40 à 50% pour le logement).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Régions les moins rémunérées</h3>
                <ul class="space-y-1">
                    <li><strong>Bretagne</strong> : 2 350 € brut/mois (-11%)</li>
                    <li><strong>Centre-Val de Loire</strong> : 2 380 € brut/mois (-10%)</li>
                    <li><strong>Corse</strong> : 2 300 € brut/mois (-13%)</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Salaire moyen par tranche d'âge</h2>
                <p>L'expérience professionnelle à un impact majeur sur les salaires. Voici l'évolution du salaire brut moyen au cours de la carrière :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Tranche d'âge</th>
                        <th class="py-2 text-right">Brut mensuel moyen</th>
                        <th class="py-2 text-right">Évolution</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Moins de 25 ans</td><td class="py-2 text-right">1 900 €</td><td class="py-2 text-right">Base</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">25-29 ans</td><td class="py-2 text-right">2 200 €</td><td class="py-2 text-right">+16%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">30-39 ans</td><td class="py-2 text-right">2 600 €</td><td class="py-2 text-right">+37%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">40-49 ans</td><td class="py-2 text-right">2 900 €</td><td class="py-2 text-right">+53%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">50-59 ans</td><td class="py-2 text-right">3 000 €</td><td class="py-2 text-right">+58%</td></tr>
                        <tr><td class="py-2">60 ans et plus</td><td class="py-2 text-right">2 950 €</td><td class="py-2 text-right">+55%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Le pic salarial se situe entre <strong>50 et 59 ans</strong>, avec une progression de +58% par rapport aux moins de 25 ans. Après 60 ans, le salaire moyen baisse légèrement (certains salariés seniors acceptent des postes moins rémunérés pour finir leur carrière).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Écart de rémunération femmes-hommes</h2>
                <p>Malgré les lois sur l'égalité salariale, un écart de rémunération persiste entre les femmes et les hommes en France :</p>
                <ul class="space-y-2">
                    <li><strong>Tous salariés confondus</strong> : les femmes gagnent en moyenne <strong>16,5% de moins</strong> que les hommes (2 190 € vs 2 625 € brut/mois)</li>
                    <li><strong>À poste et expérience équivalents</strong> : l'écart se réduit à environ <strong>5-6%</strong>, mais persiste</li>
                    <li><strong>Temps partiel</strong> : 28% des femmes travaillent à temps partiel, contre seulement 8% des hommes, ce qui explique en partie l'écart global</li>
                    <li><strong>Secteurs moins rémunérés</strong> : les femmes sont surreprésentées dans les secteurs les moins payés (services à la personne, commerce, santé)</li>
                </ul>
                <p><strong>Évolution positive</strong> : L'écart salarial se réduit progressivement. Il était de 19% en 2010, contre 16,5% en 2026. Les jeunes générations (moins de 30 ans) connaissent un écart plus faible (environ 8%), signe d'une amélioration progressive.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Comparez votre salaire aux statistiques</h2>
                <p>Pour savoir où vous vous situez par rapport aux moyennes nationales, voici quelques repères :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Déciles de salaire (10% des salariés gagnent moins que...)</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Décile</th>
                        <th class="py-2 text-right">Salaire brut mensuel</th>
                        <th class="py-2 text-right">Interprétation</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">D1 (10%)</td><td class="py-2 text-right">1 400 €</td><td class="py-2 text-right">10% gagnent moins</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">D2 (20%)</td><td class="py-2 text-right">1 600 €</td><td class="py-2 text-right">20% gagnent moins</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">D3 (30%)</td><td class="py-2 text-right">1 750 €</td><td class="py-2 text-right">30% gagnent moins</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">D5 (50%, médiane)</td><td class="py-2 text-right">2 100 €</td><td class="py-2 text-right">50% gagnent moins</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">D7 (70%)</td><td class="py-2 text-right">2 700 €</td><td class="py-2 text-right">30% gagnent plus</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">D9 (90%)</td><td class="py-2 text-right">4 000 €</td><td class="py-2 text-right">10% gagnent plus</td></tr>
                        <tr><td class="py-2">Top 1%</td><td class="py-2 text-right">&gt; 9 000 €</td><td class="py-2 text-right">1% gagnent plus</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Si vous gagnez <strong>2 700 € brut</strong>, vous êtes dans le 7ème décile : 70% des salariés gagnent moins que vous. Si vous gagnez <strong>4 000 € brut</strong>, vous faites partie des 10% les mieux payés.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pour se positionner</h2>
                <ul class="space-y-3">
                    <li><strong>Utilisez notre calculateur</strong> : Convertissez votre salaire brut en net avec notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur gratuit</a> pour comparer avec les statistiques nettes.</li>
                    <li><strong>Consultez votre convention collective</strong> : Les grilles salariales conventionnelles donnent des repères précis pour votre métier et votre ancienneté.</li>
                    <li><strong>Utilisez les sites spécialisés</strong> : Glassdoor, Indeed, Talent.com publient des salaires moyens par poste et par entreprise (données déclaratives).</li>
                    <li><strong>Comparez à expérience égale</strong> : Un salaire "moyen" pour un profil junior n'a rien à voir avec un profil senior. Ajustez vos comparaisons selon votre expérience.</li>
                    <li><strong>Tenez compte du coût de la vie</strong> : Un salaire de 2 500 € net à Paris ne donne pas le même pouvoir d'achat qu'à Toulouse ou Nantes.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Pouvoir d'achat : au-delà du salaire brut</h2>
                <p>Le salaire brut ne reflète qu'une partie de votre rémunération globale. Pour comparer votre situation réelle, tenez également compte de ces éléments :</p>
                <ul class="space-y-2">
                    <li><strong>Avantages en nature</strong> : voiture de fonction, téléphone, ordinateur portable, logement de fonction</li>
                    <li><strong>Épargne salariale</strong> : intéressement, participation, abondement employeur sur PEE/PERCO</li>
                    <li><strong>Avantages sociaux</strong> : mutuelle d'entreprise (part employeur), prévoyance, tickets restaurant, remboursement transport</li>
                    <li><strong>Temps de travail</strong> : RTT, télétravail, horaires flexibles, semaine de 4 jours</li>
                    <li><strong>Formation</strong> : budget formation, certifications, conférences financées par l'employeur</li>
                </ul>
                <p>Selon une étude de l'INSEE, les avantages non salariaux représentent en moyenne <strong>8 à 15% de la rémunération totale</strong> dans les grandes entreprises, et seulement 2 à 5% dans les TPE/PME. Ces écarts expliquent en partie pourquoi les salaires bruts affichés dans les petites structures sont parfois supérieurs : ils compensent l'absence d'avantages.</p>
            """
        },
        {
            "slug": "négocier-salaire",
            "title": "Négocier son Salaire 2026 : Guide et Conseils Pratiques",
            "desc": "Comment négocier son salaire brut à l'embauche ou lors d'un entretien annuel en 2026. Conseils pratiques, arguments chiffrés et erreurs courantes à éviter.",
            "kw": "négocier salaire, négociation salaire embauche, augmentation salaire, demander augmentation",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Pourquoi il est essentiel de négocier son salaire</h2>
                <p>Ne pas négocier son salaire peut vous coûter <strong>des dizaines de milliers d'euros</strong> sur l'ensemble de votre carrière. Pourquoi ? Parce que votre salaire de départ sert de base à toutes vos augmentations futures. Une différence de seulement <strong>100 € brut par mois</strong> représente :</p>
                <ul class="space-y-2">
                    <li>1 200 € brut par an</li>
                    <li>36 000 € brut sur 30 ans de carrière (sans compter les augmentations en %)</li>
                    <li>Environ <strong>60 000 € brut au total</strong> si on intègre les augmentations futures calculées en pourcentage de ce salaire initial</li>
                </ul>
                <p>Pourtant, selon une étude de 2025, <strong>58% des salariés français n'osent pas négocier</strong> leur salaire, par peur de paraître trop gourmands ou de perdre l'opportunité. C'est une erreur : la négociation salariale est une étape normale et attendue du processus de recrutement et d'évolution professionnelle.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Négocier à l'embauche : stratégies et scripts</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Faites vos recherches en amont</h3>
                <p>Avant de négocier, renseignez-vous sur les <strong>salaires du marché</strong> pour votre poste, votre secteur et votre région :</p>
                <ul class="space-y-2">
                    <li>Consultez les sites spécialisés : Glassdoor, Indeed, Talent.com, Welcome to the Jungle (grilles salariales par poste et entreprise)</li>
                    <li>Utilisez les études de rémunération de cabinets de recrutement (Robert Half, PageGroup, Michael Page publient des guides annuels)</li>
                    <li>Vérifiez les grilles salariales de votre convention collective</li>
                    <li>Demandez à votre réseau professionnel (LinkedIn, anciens collègues)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Demandez toujours en brut annuel</h3>
                <p>En France, la norme est de parler en <strong>brut annuel</strong>. Dire "38 000 € brut annuel" sonne plus professionnel que "2 360 € net par mois". Cela évite aussi les erreurs de calcul et les malentendus.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Donnez une fourchette, pas un chiffre fixe</h3>
                <p>Au lieu de dire "Je veux 40 000 €", dites <strong>"Je vise une rémunération entre 38 000 et 42 000 € brut annuel"</strong>. Cela laisse une marge de négociation et montre que vous êtes flexible. L'employeur proposera souvent un chiffre dans le bas de votre fourchette, d'où l'importance de placer le plancher au niveau de votre objectif réel.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Scripts de négociation à l'embauche</h3>
                <p><strong>Quand le recruteur demande vos prétentions salariales</strong> :</p>
                <blockquote class="border-l-4 border-brand-500 pl-4 italic text-slate-700">
                "D'après mes recherches sur le marché et compte tenu de mon expérience de [X années] dans [domaine], je vise une rémunération entre [Y] et [Z] € brut annuel. Cela correspond aux standards du marché pour ce type de poste. Qu'en pensez-vous ?"
                </blockquote>

                <p class="mt-4"><strong>Quand l'offre est inférieure à vos attentes</strong> :</p>
                <blockquote class="border-l-4 border-brand-500 pl-4 italic text-slate-700">
                "Je vous remercie pour cette proposition. Le poste m'intéresse beaucoup, mais j'espérais une rémunération plus proche de [X] € brut annuel, compte tenu de [arguments : expérience, compétences rares, marché]. Serait-il possible d'ajuster l'offre ?"
                </blockquote>

                <p class="mt-4"><strong>Si le recruteur ne peut pas monter en salaire</strong> :</p>
                <blockquote class="border-l-4 border-brand-500 pl-4 italic text-slate-700">
                "Je comprends la contrainte budgétaire. Serait-il possible de compenser par d'autres avantages : jours de télétravail supplémentaires, tickets restaurant, participation, prime d'intéressement, ou un premier bilan d'augmentation dans 6 mois ?"
                </blockquote>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Négocier une augmentation : méthode et timing</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Préparez un dossier solide</h3>
                <p>Pour obtenir une augmentation, vous devez prouver que vous <strong>créez de la valeur</strong>. Préparez des arguments factuels :</p>
                <ul class="space-y-2">
                    <li><strong>Résultats chiffrés</strong> : "J'ai augmenté les ventes de 15% sur mon secteur", "J'ai réduit les délais de livraison de 20%"</li>
                    <li><strong>Responsabilités élargies</strong> : "Je manage désormais une équipe de 3 personnes", "Je pilote le projet X en autonomie"</li>
                    <li><strong>Compétences acquises</strong> : "J'ai obtenu la certification Y", "Je maîtrise maintenant l'outil Z essentiel à l'équipe"</li>
                    <li><strong>Comparaison au marché</strong> : "Le salaire moyen pour mon poste et mon expérience est de X €, je suis actuellement en-dessous"</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Choisissez le bon moment</h3>
                <p>Le timing est crucial. Demandez une augmentation :</p>
                <ul class="space-y-2">
                    <li><strong>Lors de l'entretien annuel d'évaluation</strong> : c'est le moment prévu pour parler évolution professionnelle et salaire</li>
                    <li><strong>Après un succès majeur</strong> : projet livré avec succès, objectifs dépassés, client important signé</li>
                    <li><strong>Lors d'une prise de responsabilités</strong> : nouvelle mission, nouveau périmètre, nouveau management</li>
                    <li><strong>À la fin des NAO (Négociations Annuelles Obligatoires)</strong> : période où les budgets d'augmentation sont décidés (généralement janvier-mars)</li>
                </ul>

                <p class="mt-4"><strong>Évitez</strong> : demander une augmentation pendant une période difficile pour l'entreprise (plan social, baisse d'activité), juste après un échec, ou moins de 6 mois après votre dernière augmentation.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Quantifiez votre demande</h3>
                <p>Ne dites jamais "J'aimerais une petite augmentation". Soyez précis : <strong>"Je souhaite une augmentation de 8%, soit 200 € brut par mois"</strong>. Une demande chiffrée montre que vous avez réfléchi et que vous êtes sérieux.</p>
                <p>Quelle augmentation demander ? En France, les augmentations annuelles moyennes sont de :</p>
                <ul class="space-y-1">
                    <li><strong>Augmentation générale (inflation)</strong> : 1,5 à 3% par an</li>
                    <li><strong>Augmentation individuelle (mérite)</strong> : 3 à 5% par an</li>
                    <li><strong>Augmentation exceptionnelle (promotion)</strong> : 8 à 15%</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Script de demande d'augmentation</h3>
                <blockquote class="border-l-4 border-brand-500 pl-4 italic text-slate-700">
                "Bonjour [Manager], j'aimerais échanger avec vous sur mon évolution professionnelle et ma rémunération. Cette année, j'ai [résultats concrets]. Mes responsabilités ont évolué avec [nouvelles missions]. Compte tenu de ces éléments et du marché, je souhaiterais discuter d'une revalorisation de ma rémunération à hauteur de [X%] ou [Y €] brut mensuel. Qu'en pensez-vous ?"
                </blockquote>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Ne négociez pas que le salaire : package de rémunération global</h2>
                <p>Si votre employeur ne peut pas augmenter votre salaire brut, vous pouvez négocier d'autres avantages qui ont de la valeur sans coûter autant à l'entreprise :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages financiers</h3>
                <ul class="space-y-2">
                    <li><strong>Prime de Partage de la Valeur (PPV)</strong> : jusqu'à 3 000 ou 6 000 € exonérés de cotisations et d'impôt</li>
                    <li><strong>Intéressement et participation</strong> : épargne salariale exonérée de cotisations si placée sur PEE/PERCO</li>
                    <li><strong>Tickets restaurant</strong> : 60% pris en charge par l'employeur, exonérés dans la limite de 7,26 € par titre</li>
                    <li><strong>Prime d'ancienneté, prime de performance, 13ème mois</strong> : primes récurrentes qui augmentent le brut</li>
                    <li><strong>Chèques-vacances, chèques-cadeaux</strong> : exonérés dans certaines limites (montant limité, conditions de ressources)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages en nature et services</h3>
                <ul class="space-y-2">
                    <li><strong>Voiture de fonction</strong> : économie de 300 à 600 € par mois (mais soumise à cotisations)</li>
                    <li><strong>Téléphone professionnel</strong> : économie de 50 à 80 € par mois</li>
                    <li><strong>Ordinateur portable</strong> : pour usage mixte pro/perso</li>
                    <li><strong>Parking ou abonnement transport</strong> : prise en charge à 100% possible (obligatoire à 50% minimum pour les transports en commun)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages en temps et qualité de vie</h3>
                <ul class="space-y-2">
                    <li><strong>Jours de télétravail</strong> : 2-3 jours par semaine (économie de transport, meilleure QVT)</li>
                    <li><strong>RTT supplémentaires</strong> : ou horaires aménagés (semaine de 4,5 jours, finish à 16h le vendredi)</li>
                    <li><strong>Compte Épargne Temps (CET)</strong> : possibilité d'épargner des jours pour des projets futurs</li>
                    <li><strong>Flexibilité horaire</strong> : arrivée/départ décalés, horaires libres</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages en développement professionnel</h3>
                <ul class="space-y-2">
                    <li><strong>Formation</strong> : certification, MBA, formation longue prise en charge</li>
                    <li><strong>Conférences et événements</strong> : participation à des salons, congrès professionnels</li>
                    <li><strong>Coaching professionnel</strong> : accompagnement personnalisé</li>
                    <li><strong>Clause de revoyure</strong> : engagement de revoir la rémunération dans 6 mois après une période d'essai réussie</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Quand NE PAS négocier</h2>
                <p>Parfois, la négociation peut être contre-productive. Évitez de négocier dans ces situations :</p>
                <ul class="space-y-2">
                    <li><strong>Offre déjà au-dessus du marché</strong> : si l'offre est généreuse et alignée avec vos recherches, acceptez sans marchandage excessif</li>
                    <li><strong>Contexte de crise</strong> : si l'entreprise est en difficulté (plan social, licenciements), ce n'est pas le moment</li>
                    <li><strong>Poste à forte concurrence</strong> : si le recruteur à 50 candidats qualifiés, votre marge de manœuvre est faible</li>
                    <li><strong>Junior sans expérience</strong> : pour un premier emploi, la marge de négociation est limitée. Privilégiez la montée en compétences et négociez dans 1-2 ans</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Négocier en télétravail / remote : spécificités</h2>
                <p>Avec l'essor du télétravail, de nouvelles opportunités et contraintes apparaissent dans la négociation salariale :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Négocier un poste full remote</h3>
                <ul class="space-y-2">
                    <li><strong>Élargissez votre recherche géographique</strong> : un poste parisien en remote depuis la province peut vous offrir un salaire parisien avec un coût de vie provincial</li>
                    <li><strong>Demandez une indemnité télétravail</strong> : 10 à 50 € par mois pour couvrir électricité, internet, etc. (exonérée jusqu'à 580 € par an en 2026)</li>
                    <li><strong>Négociez le matériel</strong> : bureau, chaise ergonomique, écran, casque, éclairage pris en charge par l'employeur</li>
                    <li><strong>Attention à la clause de mobilité</strong> : si vous êtes en remote, assurez-vous que votre contrat ne vous oblige pas à venir au bureau 2-3 fois par semaine</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Ajustement salarial selon la localisation</h3>
                <p>Certaines entreprises pratiquent des <strong>salaires ajustés à la localisation</strong> : un développeur à Paris gagnera plus qu'à Nantes pour le même poste, même en remote. D'autres pratiquent un <strong>salaire unique</strong> quel que soit le lieu. Renseignez-vous sur la politique de l'entreprise avant de négocier.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Brut vs net : toujours penser en pouvoir d'achat réel</h2>
                <p>Une erreur fréquente est de se focaliser uniquement sur le brut. Or, ce qui compte pour votre budget, c'est le <strong>net après impôt</strong>.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de conversion</h3>
                <ul class="space-y-2">
                    <li>Augmentation de <strong>100 € brut/mois</strong> = environ 78 € net (non-cadre) ou 75 € net (cadre)</li>
                    <li>Augmentation de <strong>200 € brut/mois</strong> = environ 156 € net (non-cadre) ou 150 € net (cadre)</li>
                    <li>Augmentation de <strong>500 € brut/mois</strong> = environ 390 € net (non-cadre) ou 375 € net (cadre)</li>
                </ul>
                <p>Avant d'accepter une augmentation, vérifiez son impact réel avec notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a>. N'oubliez pas que l'augmentation peut aussi vous faire changer de tranche d'imposition et réduire l'impact net final.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Erreurs à éviter absolument</h2>
                <ul class="space-y-3">
                    <li><strong>Mentir sur son salaire actuel</strong> : si le recruteur demande votre bulletin de salaire, il découvrira la supercherie. Soyez honnête.</li>
                    <li><strong>Accepter la première offre sans négocier</strong> : même si elle vous convient, testez la marge de manœuvre. Souvent, 5 à 10% supplémentaires sont possibles.</li>
                    <li><strong>Comparer son salaire à celui des collègues</strong> : argument faible et maladroit. Focalisez-vous sur VOTRE valeur et VOS résultats.</li>
                    <li><strong>Négocier par email</strong> : préférez toujours un échange en face-à-face ou en visio pour la négociation salariale. L'écrit peut être mal interprété.</li>
                    <li><strong>Menacer de partir</strong> : "Si je n'ai pas X €, je démissionne" est une stratégie à double tranchant. N'utilisez cette carte que si vous êtes réellement prêt à partir.</li>
                    <li><strong>Accepter des promesses orales</strong> : toute augmentation doit être actée par écrit (avenant au contrat, email de confirmation).</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Checklist : êtes-vous prêt à négocier ?</h2>
                <ul class="space-y-2">
                    <li>✅ J'ai fait des recherches sur les salaires du marché pour mon poste</li>
                    <li>✅ J'ai préparé une liste de mes réalisations et résultats chiffrés</li>
                    <li>✅ Je connais ma fourchette salariale cible (min-max)</li>
                    <li>✅ J'ai converti mon objectif en brut annuel ET en net mensuel</li>
                    <li>✅ J'ai identifié des avantages alternatifs à négocier si le salaire est bloqué</li>
                    <li>✅ J'ai répété ma demande à voix haute (ou avec un proche) pour être à l'aise</li>
                    <li>✅ Je suis prêt à accepter un "non" et à proposer une clause de revoyure</li>
                </ul>
            """
        },
        {
            "slug": "salaire-net-imposable",
            "title": "Salaire Net Imposable 2026 : Définition et Calcul Détaillé",
            "desc": "Qu'est-ce que le salaire net imposable en 2026 ? Différence avec le net à payer, calcul détaillé et impact direct sur votre prélèvement à la source chaque mois.",
            "kw": "salaire net imposable, net imposable calcul, différence net imposable net à payer",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Qu'est-ce que le salaire net imposable ?</h2>
                <p>Le <strong>salaire net imposable</strong> (aussi appelé "net fiscal" ou "revenu imposable") est le montant qui sert de base au calcul de votre <strong>impôt sur le revenu</strong> et de votre <strong>prélèvement à la source</strong>. C'est la somme que l'administration fiscale prend en compte pour déterminer dans quelle tranche d'imposition vous vous situez et quel sera votre taux de prélèvement mensuel.</p>
                <p>Le net imposable est différent du "net à payer" (le montant versé sur votre compte) car certaines cotisations sociales sont fiscalement déductibles tandis que d'autres ne le sont pas. Il est toujours <strong>supérieur au net à payer</strong> d'environ 2,9%.</p>
                <p>Comprendre votre net imposable est essentiel pour anticiper votre impôt, remplir correctement votre déclaration de revenus et optimiser votre fiscalité.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Formule de calcul du net imposable</h2>
                <p>Le net imposable se calcule en plusieurs étapes. La formule simplifiée est :</p>
                <p class="font-semibold">Net imposable = Salaire brut - Cotisations sociales déductibles</p>
                <p>Ou de manière équivalente :</p>
                <p class="font-semibold">Net imposable = Net à payer + CSG non déductible + CRDS</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Détail du calcul</h3>
                <p>Voici ce qui est déduit du brut pour obtenir le net imposable :</p>
                <ul class="space-y-2">
                    <li><strong>Cotisations de Sécurité sociale</strong> (vieillesse, retraite complémentaire, etc.) : 100% déductibles</li>
                    <li><strong>CSG déductible</strong> (6,80% sur 98,25% du brut) : 100% déductible</li>
                    <li><strong>CSG non déductible</strong> (2,40% sur 98,25% du brut) : NON déductible → réintégrée au net imposable</li>
                    <li><strong>CRDS</strong> (0,50% sur 98,25% du brut) : NON déductible → réintégrée au net imposable</li>
                </ul>

                <p class="mt-4">Résultat : le net imposable est supérieur au net à payer d'environ <strong>2,9%</strong> (CSG non déductible 2,4% + CRDS 0,5% = 2,9% de 98,25% du brut).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exemple de calcul détaillé</h2>
                <p>Prenons un salaire brut de <strong>2 500 € par mois</strong> (non-cadre). Voici le calcul complet :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 1 : Du brut au net à payer</h3>
                <ul class="space-y-1">
                    <li>Salaire brut : 2 500 €</li>
                    <li>Cotisations sociales salariales : -550 € (environ 22%)</li>
                    <li><strong>Net à payer avant impôt</strong> : 1 950 €</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 2 : Calcul des cotisations non déductibles</h3>
                <ul class="space-y-1">
                    <li>Assiette CSG/CRDS : 2 500 € × 98,25% = 2 456 €</li>
                    <li>CSG non déductible : 2 456 € × 2,40% = 59 €</li>
                    <li>CRDS : 2 456 € × 0,50% = 12 €</li>
                    <li>Total non déductible : 59 + 12 = 71 €</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Étape 3 : Net imposable</h3>
                <ul class="space-y-1">
                    <li>Net à payer : 1 950 €</li>
                    <li>+ CSG non déductible + CRDS : + 71 €</li>
                    <li><strong>Net imposable</strong> : 2 021 €</li>
                </ul>

                <p class="mt-4">Vérification : 2 021 / 1 950 = 1,036, soit <strong>+3,6% par rapport au net à payer</strong>.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différence entre net imposable et net fiscal</h2>
                <p>Les termes "net imposable" et "net fiscal" désignent la même chose dans le langage courant. Cependant, il existe une subtilité :</p>
                <ul class="space-y-2">
                    <li><strong>Net imposable</strong> : montant indiqué sur votre fiche de paie, qui sert de base au prélèvement à la source mensuel</li>
                    <li><strong>Net fiscal annuel</strong> : montant annuel pris en compte dans votre déclaration de revenus (somme des nets imposables mensuels + primes annuelles)</li>
                </ul>
                <p>Pour votre déclaration, l'administration fiscale appliqué ensuite un <strong>abattement forfaitaire de 10%</strong> pour frais professionnels (sauf si vous optez pour les frais réels), ce qui donne le "revenu imposable" final.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact sur le prélèvement à la source</h2>
                <p>Votre prélèvement à la source mensuel est calculé en appliquant votre taux de prélèvement au <strong>net imposable</strong>, pas au net à payer. Cela à un impact direct sur le montant prélevé.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple concret</h3>
                <p>Pour un salaire de 2 500 € brut (célibataire, taux de prélèvement de 5%) :</p>
                <ul class="space-y-1">
                    <li>Net imposable mensuel : 2 021 €</li>
                    <li>Prélèvement à la source : 2 021 € × 5% = 101 €</li>
                    <li>Net à payer avant impôt : 1 950 €</li>
                    <li><strong>Net à payer final</strong> : 1 950 - 101 = 1 849 €</li>
                </ul>
                <p>Si le prélèvement était calculé sur le net à payer (erreur), il serait de 1 950 × 5% = 97,50 €, soit 3,50 € de moins. Sur l'année, cela ferait 42 € de différence et un reste à payer en septembre.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Net imposable annuel et déclaration de revenus</h2>
                <p>Chaque année, vous devez déclarer vos revenus aux impôts. Le montant pré-rempli dans votre déclaration correspond au <strong>net imposable annuel</strong>, soit la somme de tous vos nets imposables mensuels de l'année.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Où trouver votre net imposable annuel ?</h3>
                <ul class="space-y-2">
                    <li><strong>Sur votre dernière fiche de paie de l'année</strong> : ligne "Net imposable cumulé" ou "Cumul imposable"</li>
                    <li><strong>Dans votre déclaration pré-remplie</strong> : case 1AJ (pour le déclarant 1) ou 1BJ (pour le déclarant 2)</li>
                    <li><strong>Sur votre espace impots.gouv.fr</strong> : rubrique "Consulter mes données fiscales"</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Abattement de 10% pour frais professionnels</h3>
                <p>Par défaut, l'administration fiscale appliqué un <strong>abattement forfaitaire de 10%</strong> sur votre net imposable pour tenir compte de vos frais professionnels (transport, repas, etc.). Cet abattement est plafonné à 13 522 € en 2026.</p>
                <p><strong>Exemple</strong> : Net imposable annuel de 25 000 € → Abattement de 10% = 2 500 € → <strong>Revenu imposable</strong> = 22 500 €</p>
                <p>Vous pouvez aussi opter pour la <strong>déduction des frais réels</strong> si vos dépenses professionnelles dépassent 10% de votre net imposable (trajets domicile-travail longs, déplacements professionnels, achat de matériel, etc.).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différence avec le salaire net à payer</h2>
                <p>Pour récapituler, voici les trois "nets" à bien distinguer :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Type de net</th>
                        <th class="py-2 text-right">Formule</th>
                        <th class="py-2 text-right">Utilisation</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Net à payer avant impôt</td><td class="py-2 text-right">Brut - cotisations salariales</td><td class="py-2 text-right">Salaire "net" classique</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Net imposable</td><td class="py-2 text-right">Net + CSG ND + CRDS</td><td class="py-2 text-right">Base du prélèvement à la source</td></tr>
                        <tr><td class="py-2">Net à payer (final)</td><td class="py-2 text-right">Net avant impôt - PAS</td><td class="py-2 text-right">Montant viré sur votre compte</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact sur les tranches d'imposition</h2>
                <p>Votre net imposable annuel (multiplié par 12 si vous êtes payé mensuellement) détermine votre tranche marginale d'imposition. Voici comment cela fonctionne pour un célibataire en 2026 :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Net imposable annuel</th>
                        <th class="py-2 text-right">Tranche marginale</th>
                        <th class="py-2 text-right">Taux de PAS estimé</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Moins de 11 497 €</td><td class="py-2 text-right">0%</td><td class="py-2 text-right">0%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">11 497 - 29 315 €</td><td class="py-2 text-right">11%</td><td class="py-2 text-right">0 à 7,5%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">29 315 - 83 823 €</td><td class="py-2 text-right">30%</td><td class="py-2 text-right">7,5 à 20%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">83 823 - 180 294 €</td><td class="py-2 text-right">41%</td><td class="py-2 text-right">20 à 35%</td></tr>
                        <tr><td class="py-2">Plus de 180 294 €</td><td class="py-2 text-right">45%</td><td class="py-2 text-right">35% et +</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Attention : la tranche marginale et le taux moyen sont différents. Par exemple, si vous êtes dans la tranche à 30%, votre taux moyen effectif sera plus faible (10-15%) car les premières tranches sont taxées à 0% et 11%.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cas particuliers et éléments à intégrer</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Primes et éléments variables</h3>
                <p>Les primes (13ème mois, prime exceptionnelle, intéressement placé hors PEE/PERCO, etc.) sont soumises au même calcul : elles augmentent votre net imposable du mois où elles sont versées. Attention aux effets de seuil : une grosse prime peut temporairement augmenter votre taux de prélèvement à la source le mois suivant.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantages en nature</h3>
                <p>Les avantages en nature (voiture de fonction, logement) sont ajoutés au brut puis déduits du net, mais ils <strong>restent dans le net imposable</strong>. Vous payez donc des impôts sur un revenu que vous ne touchez pas en cash.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Heures supplémentaires</h3>
                <p>Les heures supplémentaires sont <strong>exonérées d'impôt sur le revenu</strong> dans la limite de 7 500 € net par an. Elles n'entrent donc pas dans votre net imposable jusqu'à ce seuil. Au-delà, elles sont imposées normalement.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques pour gérer votre net imposable</h2>
                <ul class="space-y-3">
                    <li><strong>Vérifiez votre déclaration pré-remplie</strong> : chaque année, comparez le montant pré-rempli avec la ligne "cumul imposable" de votre dernière fiche de paie de l'année. Des erreurs sont possibles.</li>
                    <li><strong>Anticipez votre impôt</strong> : multipliez votre net imposable mensuel par 12, appliquez l'abattement de 10%, puis utilisez un simulateur d'impôt pour estimer votre imposition annuelle.</li>
                    <li><strong>Optimisez vos déductions</strong> : versements sur un PER, dons aux associations, emploi à domicile, garde d'enfants... Ces dépenses réduisent votre impôt final.</li>
                    <li><strong>Modulez votre taux si nécessaire</strong> : en cas de changement de situation (mariage, naissance, hausse/baisse de revenus), modifiez votre taux de prélèvement sur impots.gouv.fr pour éviter un reste à payer ou un trop-perçu important.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Tableau récapitulatif : exemples de conversion</h2>
                <p>Voici des exemples concrets de conversion brut → net à payer → net imposable pour différents salaires (non-cadre) :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Brut mensuel</th>
                        <th class="py-2 text-right">Net à payer</th>
                        <th class="py-2 text-right">Net imposable</th>
                        <th class="py-2 text-right">Écart</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">1 802 € (SMIC)</td><td class="py-2 text-right">1 426 €</td><td class="py-2 text-right">1 467 €</td><td class="py-2 text-right">+2,9%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2 000 €</td><td class="py-2 text-right">1 560 €</td><td class="py-2 text-right">1 605 €</td><td class="py-2 text-right">+2,9%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2 500 €</td><td class="py-2 text-right">1 950 €</td><td class="py-2 text-right">2 007 €</td><td class="py-2 text-right">+2,9%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">3 000 €</td><td class="py-2 text-right">2 340 €</td><td class="py-2 text-right">2 408 €</td><td class="py-2 text-right">+2,9%</td></tr>
                        <tr><td class="py-2">4 000 €</td><td class="py-2 text-right">3 120 €</td><td class="py-2 text-right">3 211 €</td><td class="py-2 text-right">+2,9%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">L'écart net imposable / net à payer est constant à environ +2,9% quel que soit le niveau de salaire (tant que vous restez dans le régime général).</p>
            """
        },
        {
            "slug": "avantages-en-nature",
            "title": "Avantages en Nature 2026 : Impact sur le Salaire Brut Net",
            "desc": "Comment les avantages en nature (voiture, logement, repas) impactent votre salaire brut et net en 2026. Barèmes d'évaluation forfaitaire et fiscalité détaillée.",
            "kw": "avantages en nature, voiture de fonction brut net, logement de fonction, avantages salaire",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Qu'est-ce qu'un avantage en nature ?</h2>
                <p>Un <strong>avantage en nature</strong> est un bien ou service fourni gratuitement (ou à prix réduit) par l'employeur au salarié : voiture de fonction, logement, repas fournis, téléphone portable, ordinateur, etc. Juridiquement, ces avantages constituent un complément de rémunération et sont donc soumis aux cotisations sociales et à l'impôt sur le revenu, au même titre que le salaire en espèces.</p>
                <p>L'avantage en nature est doublement imposé : il augmente votre brut (donc les cotisations) ET votre net imposable (donc l'impôt). Paradoxalement, il peut réduire votre net à payer car vous ne touchez pas cet avantage en cash, mais vous payez des charges dessus.</p>
                <p>Comprendre leur impact sur votre fiche de paie est essentiel pour évaluer votre rémunération réelle et négocier intelligemment.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Principaux avantages en nature et méthodes d'évaluation</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Voiture de fonction</h3>
                <p>C'est l'avantage en nature le plus fréquent. Deux méthodes d'évaluation existent :</p>

                <h4 class="font-semibold text-slate-900 mt-4">Méthode forfaitaire (la plus utilisée)</h4>
                <ul class="space-y-2">
                    <li><strong>Voiture possédée par l'employeur</strong> : 9% du coût d'achat TTC par an (ou 12% si le véhicule a plus de 5 ans)</li>
                    <li><strong>Voiture louée par l'employeur</strong> : 30% du coût total annuel (loyer + entretien + assurance)</li>
                </ul>
                <p><strong>Exemple</strong> : Voiture achetée 30 000 € TTC → Avantage annuel = 30 000 × 9% = 2 700 € → soit <strong>225 € par mois</strong> ajoutés au brut.</p>
                <p>Si l'employeur paie aussi le carburant, l'assurance ou l'entretien pour usage personnel, ces montants s'ajoutent à l'avantage.</p>

                <h4 class="font-semibold text-slate-900 mt-4">Méthode des dépenses réelles</h4>
                <p>L'avantage correspond aux frais réellement engagés par l'employeur pour l'usage personnel (carburant perso, péages, etc.). Cette méthode est rarement utilisée car plus complexe à justifier.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Logement de fonction</h3>
                <p>Le logement fourni par l'employeur est évalué selon un barème URSSAF qui dépend du nombre de pièces et de la rémunération :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Type de logement</th>
                        <th class="py-2 text-right">Avantage mensuel (% de la rémunération)</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">1 pièce principale</td><td class="py-2 text-right">3,85%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2 pièces principales</td><td class="py-2 text-right">5,15%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">3 pièces principales</td><td class="py-2 text-right">6,95%</td></tr>
                        <tr><td class="py-2">4 pièces et plus</td><td class="py-2 text-right">8,70%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4"><strong>Exemple</strong> : Salaire de 3 000 € brut + logement de 3 pièces → Avantage = 3 000 × 6,95% = <strong>209 € par mois</strong>.</p>
                <p>Si l'employeur paie aussi les charges (eau, électricité, chauffage), elles s'ajoutent à l'avantage pour leur montant réel.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Repas</h3>
                <p>Les repas fournis gratuitement par l'employeur sont évalués forfaitairement à <strong>5,35 € par repas</strong> en 2026 (valeur URSSAF). Si l'employeur pratique une participation, seule la différence constitue un avantage.</p>
                <p><strong>Exemple</strong> : Cantine d'entreprise gratuite, 20 repas par mois → Avantage = 20 × 5,35 = <strong>107 € par mois</strong>.</p>
                <p>À distinguer des <strong>tickets restaurant</strong> : ceux-ci ne sont pas un avantage en nature mais une prestation sociale exonérée de cotisations dans la limite de 7,26 € par titre (avec 60% max pris en charge par l'employeur).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. Téléphone et ordinateur (NTIC)</h3>
                <p>Pour un usage mixte professionnel/personnel :</p>
                <ul class="space-y-1">
                    <li><strong>Forfait téléphonique</strong> : si usage majoritairement professionnel, pas d'avantage en nature</li>
                    <li><strong>Ordinateur portable/tablette</strong> : 10% du prix d'achat TTC par an si usage mixte</li>
                </ul>
                <p><strong>Exemple</strong> : Ordinateur à 1 200 € → Avantage annuel = 120 € → soit <strong>10 € par mois</strong>.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5. Autres avantages courants</h3>
                <ul class="space-y-2">
                    <li><strong>Parking</strong> : valeur de la place de parking si fournie gratuitement (évaluation au marché local)</li>
                    <li><strong>Outils de travail à usage perso</strong> : matériel, abonnements, etc.</li>
                    <li><strong>Électricité/chauffage</strong> : montant réel des factures si pris en charge</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact sur votre fiche de paie</h2>
                <p>L'avantage en nature suit un circuit spécifique sur votre bulletin de salaire :</p>
                <ol class="space-y-2">
                    <li><strong>1. Ajout au brut</strong> : la valeur de l'avantage est ajoutée à votre salaire brut de base</li>
                    <li><strong>2. Calcul des cotisations</strong> : les cotisations sociales sont calculées sur ce brut augmenté</li>
                    <li><strong>3. Retrait du net</strong> : l'avantage est ensuite retiré du net à payer (vous ne le touchez pas en cash)</li>
                    <li><strong>4. Intégration au net imposable</strong> : l'avantage reste dans le net imposable → vous payez l'impôt dessus</li>
                </ol>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple chiffré détaillé</h3>
                <p>Salarié avec 2 500 € brut + voiture de fonction évaluée à 300 € :</p>
                <ul class="space-y-1">
                    <li>Salaire de base : 2 500 €</li>
                    <li>+ Avantage en nature voiture : +300 €</li>
                    <li><strong>Brut total</strong> : 2 800 €</li>
                    <li>Cotisations sociales (22%) : -616 €</li>
                    <li>Net avant retrait avantage : 2 184 €</li>
                    <li>- Retrait avantage : -300 €</li>
                    <li><strong>Net à payer avant impôt</strong> : 1 884 €</li>
                </ul>
                <p class="mt-4"><strong>Conséquence</strong> : votre net à payer diminue de 66 € (passage de 1 950 € sans voiture à 1 884 € avec voiture), mais vous disposez d'une voiture payée par l'employeur, ce qui compense largement. En revanche, vous payez 66 € de cotisations sur un revenu que vous ne touchez pas en espèces.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Avantage en nature vs prime : comparaison fiscale</h2>
                <p>Un employeur peut choisir de vous donner soit un avantage en nature, soit une prime équivalente. Voici la différence de coût :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemple : voiture vs prime de 300 € brut</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Élément</th>
                        <th class="py-2 text-right">Avantage voiture</th>
                        <th class="py-2 text-right">Prime 300 € brut</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Valeur ajoutée au brut</td><td class="py-2 text-right">300 €</td><td class="py-2 text-right">300 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Cotisations salariales</td><td class="py-2 text-right">-66 €</td><td class="py-2 text-right">-66 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Avantage reçu en nature</td><td class="py-2 text-right">Voiture</td><td class="py-2 text-right">-</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Net à payer cash</td><td class="py-2 text-right">-300 €</td><td class="py-2 text-right">+234 €</td></tr>
                        <tr><td class="py-2">Valeur réelle</td><td class="py-2 text-right">Voiture (valeur locative ~500-600 €)</td><td class="py-2 text-right">234 € en cash</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Si la voiture vous aurait coûté 500 € par mois en location, l'avantage en nature est plus intéressant (vous "gagnez" 500 € de valeur pour 66 € de cotisations). Si vous n'avez pas besoin de voiture, la prime en cash est préférable.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Optimisation fiscale des avantages en nature</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Négociez la prise en charge partielle</h3>
                <p>Vous pouvez demander à participer financièrement à l'avantage pour réduire sa valeur imposable. Exemple : payer 100 € par mois pour la voiture réduit l'avantage de 300 € à 200 €.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Préférez les exonérations</h3>
                <p>Certains avantages sont totalement ou partiellement exonérés de cotisations :</p>
                <ul class="space-y-2">
                    <li><strong>Tickets restaurant</strong> : exonérés jusqu'à 7,26 € par titre (dont max 60% employeur)</li>
                    <li><strong>Chèques-vacances</strong> : exonérés dans certaines limites</li>
                    <li><strong>Participation employeur à la mutuelle</strong> : exonérée (dans la limite du contrat responsable)</li>
                    <li><strong>Indemnité télétravail</strong> : exonérée jusqu'à 580 € par an</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Pour les dirigeants : arbitrage rémunération/avantages</h3>
                <p>Les dirigeants peuvent optimiser leur package en mixant salaire brut faible + avantages en nature + dividendes (pour les gérants majoritaires de SARL ou présidents de SAS actionnaires). Consultez un expert-comptable pour optimiser.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Titres-restaurant : cas particulier</h2>
                <p>Les <strong>titres-restaurant</strong> ne sont PAS des avantages en nature mais des <strong>titres spéciaux de paiement</strong> exonérés de cotisations dans certaines limites. Voici les règles 2026 :</p>
                <ul class="space-y-2">
                    <li><strong>Valeur faciale maximum</strong> : 14 € par titre (au-delà, l'excédent est soumis à cotisations)</li>
                    <li><strong>Part employeur exonérée</strong> : entre 50% et 60% de la valeur faciale</li>
                    <li><strong>Plafond d'exonération</strong> : 7,26 € par titre en 2026</li>
                </ul>
                <p><strong>Exemple optimal</strong> : Titre de 12 € → 60% employeur (7,20 €) + 40% salarié (4,80 €). La part employeur (7,20 €) est sous le seuil de 7,26 €, donc totalement exonérée.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Avantage réel pour le salarié</h3>
                <p>Pour 20 jours travaillés par mois avec des titres de 12 € :</p>
                <ul class="space-y-1">
                    <li>Valeur totale : 20 × 12 = 240 €</li>
                    <li>Coût salarié : 20 × 4,80 = 96 €</li>
                    <li>Gain salarié : 240 - 96 = <strong>144 € de pouvoir d'achat repas par mois</strong></li>
                    <li>Pas de cotisations sociales ni d'impôt sur cette somme</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Contrôle URSSAF et justificatifs</h2>
                <p>L'employeur doit pouvoir justifier la valorisation des avantages en nature en cas de contrôle URSSAF :</p>
                <ul class="space-y-2">
                    <li><strong>Voiture</strong> : facture d'achat ou contrat de location, carte grise, contrat d'entretien</li>
                    <li><strong>Logement</strong> : bail, justificatif de propriété, avis de taxe foncière</li>
                    <li><strong>Repas</strong> : relevés de cantine, factures</li>
                </ul>
                <p>En cas de sous-évaluation, l'URSSAF peut redresser l'employeur et réclamer les cotisations manquantes avec pénalités (jusqu'à 3 ans rétroactif).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Avantages en nature et rupture du contrat</h2>
                <p>En cas de licenciement ou démission, les avantages en nature cessent généralement à la fin du contrat. Attention aux points suivants :</p>
                <ul class="space-y-2">
                    <li><strong>Voiture</strong> : restitution immédiate ou location possible pendant le préavis</li>
                    <li><strong>Logement</strong> : délai de préavis pour quitter (souvent 1 à 3 mois selon le contrat)</li>
                    <li><strong>Indemnités de licenciement</strong> : calculées sur le brut y compris avantages en nature</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques</h2>
                <ul class="space-y-3">
                    <li><strong>Vérifiez votre fiche de paie</strong> : assurez-vous que la valorisation de vos avantages correspond aux barèmes légaux. Une surévaluation vous coûte en cotisations.</li>
                    <li><strong>Négociez intelligemment</strong> : un avantage en nature peut être plus intéressant qu'une prime brute si sa valeur d'usage dépassé largement sa valorisation fiscale (voiture, logement).</li>
                    <li><strong>Calculez le coût net</strong> : utilisez notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a> pour comparer un salaire avec et sans avantages.</li>
                    <li><strong>Anticipez la fin du contrat</strong> : si vous démissionnez, vous perdez les avantages. Prévoyez le budget pour les remplacer (location voiture, loyer).</li>
                </ul>
            """
        },
        {
            "slug": "heures-supplémentaires-brut-net",
            "title": "Heures Sup Brut en Net 2026 : Calcul et Exonérations",
            "desc": "Calculez vos heures supplémentaires brut en net en 2026. Majoration de 25% à 50%, exonération fiscale jusqu'à 7 500€/an et simulateur gratuit instantané.",
            "kw": "heures supplémentaires brut net, calcul heures sup, majoration heures supplémentaires, exonération heures sup",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Qu'est-ce qu'une heure supplémentaire ?</h2>
                <p>Les <strong>heures supplémentaires</strong> sont les heures de travail effectuées au-delà de la durée légale de travail, fixée à <strong>35 heures par semaine</strong> (ou 1 607 heures par an). Elles donnent droit à une majoration de salaire et bénéficient d'avantages fiscaux et sociaux importants depuis 2019.</p>
                <p>Les heures supplémentaires sont à distinguer des <strong>heures complémentaires</strong> (pour les temps partiels) et des <strong>heures au forfait</strong> (pour les cadres en forfait jours).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Taux de majoration des heures supplémentaires</h2>
                <p>Les heures travaillées au-delà de 35h par semaine sont obligatoirement majorées. Le taux légal de majoration est :</p>
                <ul class="space-y-2">
                    <li><strong>De la 36e à la 43e heure</strong> : +25% du taux horaire normal</li>
                    <li><strong>À partir de la 44e heure</strong> : +50% du taux horaire normal</li>
                </ul>
                <p>Une convention collective ou un accord d'entreprise peut prévoir des taux différents, mais ils ne peuvent pas être inférieurs à <strong>10%</strong>.</p>
                <p><strong>Exemples de taux conventionnels</strong> : Métallurgie (+25% puis +50%), Commerce (+25%), BTP (+25% puis +50%), Banque (+25%).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Contingent annuel d'heures supplémentaires</h2>
                <p>Le <strong>contingent annuel</strong> est le nombre maximum d'heures supplémentaires que l'employeur peut demander sans autorisation de l'inspection du travail ni contrepartie obligatoire en repos. Il est fixé à <strong>220 heures par an</strong> par défaut, mais peut être modifié par accord collectif.</p>
                <p>Au-delà du contingent, les heures supplémentaires donnent droit à une <strong>contrepartie obligatoire en repos</strong> de 100% (1 heure travaillée = 1 heure de repos en plus de la rémunération).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exonération fiscale et sociale des heures supplémentaires</h2>
                <p>Depuis janvier 2019, les heures supplémentaires bénéficient d'un régime fiscal et social très avantageux :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Réduction de cotisations salariales</h3>
                <p>Les heures supplémentaires bénéficient d'une <strong>réduction de cotisations salariales de 11,31%</strong> (exonération de la part salariale de l'assurance vieillesse). Cette réduction s'appliqué sur la rémunération des heures sup (y compris la majoration).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Exonération d'impôt sur le revenu</h3>
                <p>Les heures supplémentaires sont <strong>exonérées d'impôt sur le revenu</strong> dans la limite de <strong>7 500 € net par an et par salarié</strong> (montant 2026). Au-delà de ce plafond, elles sont imposées normalement.</p>
                <p>Cette exonération s'appliqué automatiquement : les heures sup n'entrent pas dans votre net imposable (jusqu'au plafond), donc ne sont pas prises en compte pour le prélèvement à la source.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cotisations patronales</h3>
                <p>Les heures supplémentaires ouvrent aussi droit à une <strong>déduction forfaitaire de cotisations patronales</strong> de 1,50 € par heure (dans les entreprises de moins de 20 salariés). Pour les plus grandes entreprises, pas de déduction patronale spécifique.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exemple de calcul détaillé</h2>
                <p>Salarié non-cadre avec un taux horaire de <strong>15 € brut</strong>, faisant <strong>4 heures supplémentaires par semaine</strong> (majorées à +25%) :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul du brut mensuel en heures sup</h3>
                <ul class="space-y-1">
                    <li>Taux horaire normal : 15 €</li>
                    <li>Taux majoré (+25%) : 15 € × 1,25 = 18,75 €/heure</li>
                    <li>Heures sup par mois : 4h × 4,33 semaines = 17,32 heures</li>
                    <li><strong>Brut heures sup</strong> : 17,32 × 18,75 = 324,75 € brut</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Passage en net</h3>
                <ul class="space-y-1">
                    <li>Cotisations salariales normales : ~22% = 71,45 €</li>
                    <li>Réduction de cotisations (-11,31%) : -36,73 €</li>
                    <li>Cotisations réelles : 71,45 - 36,73 = 34,72 €</li>
                    <li><strong>Net avant impôt</strong> : 324,75 - 34,72 = 290,03 €</li>
                    <li>Exonération d'impôt : pas de prélèvement à la source</li>
                    <li><strong>Net final</strong> : 290,03 €</li>
                </ul>

                <p class="mt-4"><strong>Taux de conversion effectif</strong> : 290,03 / 324,75 = <strong>89,3%</strong> (contre 78% pour un salaire normal). Les heures sup sont donc beaucoup plus rentables en net !</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Tableaux de conversion à différents taux horaires</h2>
                <p>Voici le gain net mensuel pour différentes configurations (majoration +25%, 4h sup/semaine) :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Taux horaire brut</th>
                        <th class="py-2 text-right">Brut heures sup/mois</th>
                        <th class="py-2 text-right">Net heures sup/mois</th>
                        <th class="py-2 text-right">Taux de conversion</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">11,88 € (SMIC)</td><td class="py-2 text-right">257 €</td><td class="py-2 text-right">229 €</td><td class="py-2 text-right">89,1%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">15,00 €</td><td class="py-2 text-right">325 €</td><td class="py-2 text-right">290 €</td><td class="py-2 text-right">89,3%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">20,00 €</td><td class="py-2 text-right">433 €</td><td class="py-2 text-right">387 €</td><td class="py-2 text-right">89,4%</td></tr>
                        <tr><td class="py-2">25,00 € (cadre)</td><td class="py-2 text-right">541 €</td><td class="py-2 text-right">476 €</td><td class="py-2 text-right">88,0%</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Les cadres ont un taux légèrement inférieur en raison de la CET (0,14%) qui n'est pas exonérée.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Repos compensateur de remplacement</h2>
                <p>Au lieu de payer les heures supplémentaires, l'employeur peut, sous conditions, les compenser par un <strong>repos compensateur équivalent</strong> (RCE). Le salarié prend alors des jours de repos au lieu de toucher une rémunération majorée.</p>
                <p><strong>Calcul du repos</strong> : 1 heure sup majorée à 25% = 1h15 de repos (1h + 25%). Le salarié récupère donc plus de temps de repos que le temps travaillé.</p>
                <p>Cette option doit être prévue par accord collectif ou, à défaut, acceptée par le salarié.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Heures supplémentaires et impact sur la retraite</h2>
                <p>Les heures supplémentaires comptent pour le calcul de votre retraite. Même si elles bénéficient d'une réduction de cotisations salariales, elles sont soumises aux cotisations patronales de retraite complètes, ce qui vous donne des droits identiques à un salaire normal.</p>
                <p>Concrètement : faire des heures sup n'impacte pas négativement votre future pension de retraite, au contraire, cela l'augmente (légèrement) grâce au revenu supplémentaire.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Plafonds et limites</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Durée maximale de travail</h3>
                <p>Malgré les heures supplémentaires, vous ne pouvez pas dépasser :</p>
                <ul class="space-y-1">
                    <li><strong>10 heures par jour</strong> (12h exceptionnellement avec accord)</li>
                    <li><strong>48 heures par semaine</strong> (ou 44h en moyenne sur 12 semaines)</li>
                    <li><strong>Repos quotidien</strong> : minimum 11 heures entre 2 journées de travail</li>
                    <li><strong>Repos hebdomadaire</strong> : minimum 35 heures consécutives (24h + 11h)</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Plafond d'exonération fiscale</h3>
                <p>Rappel : l'exonération d'impôt est plafonnée à <strong>7 500 € net par an</strong>. Si vous dépassez ce montant, l'excédent est imposable.</p>
                <p><strong>Exemple</strong> : Vous avez touché 8 200 € net en heures sup dans l'année → 7 500 € exonérés + 700 € imposables.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différence avec les heures complémentaires</h2>
                <p>À ne pas confondre avec les <strong>heures complémentaires</strong>, réservées aux salariés à temps partiel :</p>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Critère</th>
                        <th class="py-2 text-right">Heures supplémentaires</th>
                        <th class="py-2 text-right">Heures complémentaires</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">Pour qui ?</td><td class="py-2 text-right">Temps plein (35h+)</td><td class="py-2 text-right">Temps partiel</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Majoration</td><td class="py-2 text-right">+25% ou +50%</td><td class="py-2 text-right">+10% ou +25%</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Exonération d'impôt</td><td class="py-2 text-right">Oui (7 500 €)</td><td class="py-2 text-right">Oui (7 500 €)</td></tr>
                        <tr><td class="py-2">Limite</td><td class="py-2 text-right">Contingent 220h/an</td><td class="py-2 text-right">1/10 de la durée du contrat</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Refus des heures supplémentaires : vos droits</h2>
                <p>Pouvez-vous refuser de faire des heures supplémentaires ? Cela dépend :</p>
                <ul class="space-y-2">
                    <li><strong>Dans la limite du contingent (220h/an)</strong> : les heures sup sont en principe obligatoires si demandées par l'employeur avec un délai de prévenance raisonnable (3 jours ouvrés minimum)</li>
                    <li><strong>Au-delà du contingent</strong> : vous pouvez refuser sans risque de sanction, sauf urgence ou circonstances exceptionnelles</li>
                    <li><strong>Dépassement des durées maximales</strong> : vous pouvez toujours refuser si cela vous fait dépasser les 10h/jour ou 48h/semaine</li>
                    <li><strong>Motifs légitimes</strong> : raisons familiales impérieuses, santé, impossibilité matérielle (transport, garde d'enfants)</li>
                </ul>
                <p>Un refus abusif (sans motif légitime) peut constituer une faute, mais un licenciement pour ce seul motif est généralement jugé sans cause réelle et sérieuse par les prud'hommes.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques</h2>
                <ul class="space-y-3">
                    <li><strong>Vérifiez votre fiche de paie</strong> : les heures sup doivent être détaillées avec le taux de majoration appliqué. Vérifiez que la réduction de cotisations de 11,31% est bien appliquée.</li>
                    <li><strong>Comptabilisez vos heures</strong> : tenez un registre personnel de vos heures sup pour éviter les litiges. L'employeur doit aussi tenir un décompte précis.</li>
                    <li><strong>Anticipez le plafond fiscal</strong> : si vous approchez des 7 500 € net en heures sup, l'excédent sera imposable. Discutez avec votre employeur pour éventuellement basculer sur du repos compensateur.</li>
                    <li><strong>Négociez le taux</strong> : si votre convention collective prévoit un taux supérieur à 25%, réclamez-le. Certains secteurs accordent +50% dès la première heure.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Heures supplémentaires et cadres au forfait jours</h2>
                <p>Les cadres en <strong>forfait jours</strong> (218 jours par an maximum) ne comptabilisent pas d'heures supplémentaires au sens strict. Leur temps de travail est décompté en jours, pas en heures. Cependant, ils peuvent bénéficier de <strong>jours de repos compensateurs</strong> (RTT) au-delà des congés payés.</p>
                <p>Si un cadre en forfait jours travaille au-delà de 218 jours, il peut renoncer à certains jours de repos en échange d'une <strong>majoration de 10% minimum</strong> par jour travaillé en plus. Cette renonciation doit faire l'objet d'un accord écrit entre le salarié et l'employeur, et ne peut pas dépasser 235 jours par an.</p>
                <p>Pour les cadres au <strong>forfait heures</strong> (plus rare), les heures au-delà du forfait sont bien des heures supplémentaires avec majoration et exonérations classiques.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Heures supplémentaires et chômage partiel</h2>
                <p>En cas d'activité partielle (chômage partiel), les heures supplémentaires habituelles ne sont pas indemnisées par l'État. Seules les heures correspondant à la durée légale (35h) ou conventionnelle sont compensées. C'est un point important à considérer : un salarié qui dépend fortement des heures sup pour son budget peut voir son revenu chuter davantage que prévu en cas de chômage partiel.</p>
            """
        },
        {
            "slug": "prime-brut-en-net",
            "title": "Prime Brut en Net 2026 : Calcul des Primes et Cotisations",
            "desc": "Convertissez une prime brute en net en 2026. Primes exceptionnelles, 13ème mois, intéressement et participation : cotisations sociales et fiscalité détaillées.",
            "kw": "prime brut en net, calcul prime nette, prime exceptionnelle cotisations, convertir prime",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Comment convertir une prime brute en net ?</h2>
                <p>Les primes versées par l'employeur sont en principe soumises aux <strong>mêmes cotisations sociales</strong> que le salaire de base : cotisations de Sécurité sociale, retraite complémentaire, CSG/CRDS. Pour convertir une prime brute en net, appliquez le même taux de conversion que pour votre salaire : environ <strong>22% de cotisations pour un non-cadre</strong> et <strong>25% pour un cadre</strong>.</p>
                <p>Cependant, certaines primes bénéficient d'exonérations totales ou partielles de cotisations et d'impôt, ce qui améliore significativement le taux de conversion brut-net. Il est donc essentiel de connaître la nature exacte de votre prime avant de calculer le net.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Types de primes et leur traitement fiscal</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Prime classique (prime d'objectifs, performance, etc.)</h3>
                <p><strong>Traitement</strong> : soumise à cotisations sociales (22-25%) + impôt sur le revenu via le prélèvement à la source.</p>
                <p><strong>Exemple</strong> : Prime de 1 000 € brut (non-cadre) → 1 000 - 220 (cotisations) = 780 € net avant impôt → 780 - 7,5% PAS = ~722 € net après impôt.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Prime de Partage de la Valeur (PPV)</h3>
                <p>Créée en 2022 et pérennisée, la <strong>PPV</strong> (anciennement "PEPA") est exonérée de cotisations sociales ET d'impôt sur le revenu dans certaines limites :</p>
                <ul class="space-y-2">
                    <li><strong>Plafond standard</strong> : 3 000 € par an et par bénéficiaire</li>
                    <li><strong>Plafond majoré</strong> : 6 000 € si l'entreprise à un accord d'intéressement ou de participation</li>
                    <li><strong>Conditions</strong> : entreprise de moins de 50 salariés, ou salariés rémunérés moins de 3× le SMIC annuel (64 865 € brut en 2026)</li>
                </ul>
                <p><strong>Avantage</strong> : une PPV de 3 000 € = 3 000 € net versés, sans aucune cotisation ni impôt. C'est le dispositif le plus avantageux actuellement.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Intéressement et Participation</h3>
                <p>L'<strong>intéressement</strong> et la <strong>participation</strong> sont des primes collectives liées aux résultats de l'entreprise. Leur traitement dépend du choix du salarié :</p>
                <ul class="space-y-2">
                    <li><strong>Versement immédiat</strong> : soumis à cotisations sociales (hors assurance chômage) + impôt → taux de cotisations ~10-12% + impôt</li>
                    <li><strong>Placement sur PEE/PERCO</strong> : exonéré de cotisations sociales (sauf CSG/CRDS à 9,7%) + exonéré d'impôt → gain fiscal important</li>
                    <li><strong>Forfait social employeur</strong> : 20% de la somme versée (payé par l'employeur, pas par vous)</li>
                </ul>
                <p><strong>Exemple</strong> : Participation de 2 000 €. Si placée sur PEE → 2 000 - 194 € (CSG/CRDS) = 1 806 € disponibles en épargne. Si versée cash → 2 000 - 220 (cotisations) - 150 (impôt) = 1 630 € net.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">4. 13ème mois, prime de vacances, prime de fin d'année</h3>
                <p>Ces primes contractuelles ou conventionnelles sont traitées comme du salaire : cotisations pleines (22-25%) + impôt. Pas d'exonération.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">5. Prime d'ancienneté</h3>
                <p>Souvent intégrée au salaire mensuel de base. Cotisations et impôt normaux.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Exemples de conversion brut → net</h2>
                <p>Voici des exemples concrets pour différents montants de primes classiques (soumises à cotisations pleines) :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Non-cadre (22% de cotisations, taux PAS 5%)</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Prime brute</th>
                        <th class="py-2 text-right">Cotisations (22%)</th>
                        <th class="py-2 text-right">Net avant impôt</th>
                        <th class="py-2 text-right">Impôt (5%)</th>
                        <th class="py-2 text-right">Net après impôt</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">500 €</td><td class="py-2 text-right">-110 €</td><td class="py-2 text-right">390 €</td><td class="py-2 text-right">-19,50 €</td><td class="py-2 text-right">370,50 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">1 000 €</td><td class="py-2 text-right">-220 €</td><td class="py-2 text-right">780 €</td><td class="py-2 text-right">-39 €</td><td class="py-2 text-right">741 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2 000 €</td><td class="py-2 text-right">-440 €</td><td class="py-2 text-right">1 560 €</td><td class="py-2 text-right">-78 €</td><td class="py-2 text-right">1 482 €</td></tr>
                        <tr><td class="py-2">5 000 €</td><td class="py-2 text-right">-1 100 €</td><td class="py-2 text-right">3 900 €</td><td class="py-2 text-right">-195 €</td><td class="py-2 text-right">3 705 €</td></tr>
                    </tbody>
                </table>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Cadre (25% de cotisations, taux PAS 7,5%)</h3>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Prime brute</th>
                        <th class="py-2 text-right">Cotisations (25%)</th>
                        <th class="py-2 text-right">Net avant impôt</th>
                        <th class="py-2 text-right">Impôt (7,5%)</th>
                        <th class="py-2 text-right">Net après impôt</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">500 €</td><td class="py-2 text-right">-125 €</td><td class="py-2 text-right">375 €</td><td class="py-2 text-right">-28,13 €</td><td class="py-2 text-right">346,87 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">1 000 €</td><td class="py-2 text-right">-250 €</td><td class="py-2 text-right">750 €</td><td class="py-2 text-right">-56,25 €</td><td class="py-2 text-right">693,75 €</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">2 000 €</td><td class="py-2 text-right">-500 €</td><td class="py-2 text-right">1 500 €</td><td class="py-2 text-right">-112,50 €</td><td class="py-2 text-right">1 387,50 €</td></tr>
                        <tr><td class="py-2">5 000 €</td><td class="py-2 text-right">-1 250 €</td><td class="py-2 text-right">3 750 €</td><td class="py-2 text-right">-281,25 €</td><td class="py-2 text-right">3 468,75 €</td></tr>
                    </tbody>
                </table>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact sur le prélèvement à la source</h2>
                <p>Attention : une prime importante peut <strong>augmenter temporairement votre taux de prélèvement à la source</strong> le mois où elle est versée. Pourquoi ? Parce que l'administration fiscale calcule votre taux en fonction du revenu du mois précédent.</p>
                <p><strong>Exemple</strong> : Vous gagnez habituellement 2 500 € net imposable. En décembre, vous touchez une prime de 3 000 € brut (2 340 € net imposable). Votre net imposable total pour décembre sera de 4 840 €. Si le système calcule un taux basé sur ce revenu "annualisé" (4 840 × 12 = 58 080 €), votre taux peut bondir de 7,5% à 12-15% le mois suivant.</p>
                <p><strong>Régularisation</strong> : Pas de panique, ce trop-prélevé sera régularisé en septembre de l'année suivante lors de votre déclaration de revenus. Mais cela peut créer un coup dur de trésorerie.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Optimisation fiscale des primes</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Privilégiez la PPV si possible</h3>
                <p>Si votre employeur peut vous verser une prime exceptionnelle, demandez qu'elle soit versée sous forme de <strong>Prime de Partage de la Valeur</strong> dans la limite de 3 000 ou 6 000 €. Vous économisez 22-25% de cotisations + 5-15% d'impôt = 30-40% de gain net !</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Placez l'intéressement/participation sur PEE</h3>
                <p>Ne demandez pas le versement immédiat. Placez sur un PEE : vous économisez les cotisations sociales (hors CSG/CRDS) et l'impôt, et l'épargne est disponible après 5 ans (ou immédiatement en cas de déblocage anticipé : achat résidence principale, mariage, etc.).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Étalez les primes si possible</h3>
                <p>Si vous négociez une prime importante (ex : 10 000 €), demandez à votre employeur de l'étaler sur 2-3 mois pour limiter l'impact sur votre taux de prélèvement à la source et éviter de passer dans une tranche d'imposition supérieure ponctuellement.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Primes et ancienneté / démission</h2>
                <p>Certaines primes sont conditionnées à une <strong>condition de présence</strong> dans l'entreprise à la date de versement :</p>
                <ul class="space-y-2">
                    <li><strong>Prime de fin d'année</strong> : souvent conditionnée à être présent au 31/12. Si vous démissionnez en novembre, vous la perdez (sauf clause contraire dans votre contrat ou convention collective).</li>
                    <li><strong>13ème mois</strong> : peut être proratisé en cas de départ en cours d'année (ex : 6 mois travaillés = 6/12 du 13ème mois).</li>
                    <li><strong>Intéressement/participation</strong> : droits généralement acquis même en cas de départ, mais vérifiez l'accord d'entreprise.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Timing de versement et stratégie</h2>
                <p>Le moment où la prime est versée peut avoir un impact fiscal :</p>
                <ul class="space-y-2">
                    <li><strong>Prime versée en décembre N</strong> : imposable sur les revenus N, déclarés en N+1, impôt payé en N+1</li>
                    <li><strong>Prime versée en janvier N+1</strong> : imposable sur les revenus N+1, déclarés en N+2, impôt payé en N+2 → différé d'un an</li>
                </ul>
                <p>Si vous anticipez une baisse de revenus l'année suivante (congé parental, passage à temps partiel, retraite), il peut être judicieux de demander le versement de la prime en janvier plutôt qu'en décembre pour bénéficier d'un taux d'imposition plus faible.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques</h2>
                <ul class="space-y-3">
                    <li><strong>Vérifiez votre fiche de paie</strong> : assurez-vous que la prime est bien mentionnée avec le bon montant brut et que les cotisations appliquées sont correctes.</li>
                    <li><strong>Calculez le net réel</strong> : utilisez notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a> pour estimer précisément ce que vous toucherez après cotisations et impôt.</li>
                    <li><strong>Négociez le type de prime</strong> : si votre employeur vous propose une prime, suggérez une PPV ou un intéressement plutôt qu'une prime classique pour optimiser le net.</li>
                    <li><strong>Anticipez l'impôt</strong> : si la prime est importante, provisionnez pour le trop-prélevé d'impôt le mois suivant ou demandez une modulation de votre taux sur impots.gouv.fr.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Primes et cotisations retraite</h2>
                <p>Un point souvent négligé : les primes soumises à cotisations <strong>augmentent vos droits à la retraite</strong>. Chaque euro de prime cotisé à l'AGIRC-ARRCO vous rapporte des points de retraite complémentaire supplémentaires. À l'inverse, les primes exonérées (PPV, intéressement placé) ne génèrent pas de droits retraite.</p>
                <p>Sur une carrière de 40 ans, la différence peut être significative : un salarié recevant 3 000 € de primes cotisées chaque année accumule environ 80 points AGIRC-ARRCO de plus qu'un salarié recevant la même somme en PPV. À la retraite, ces 80 points représentent environ <strong>113 € de pension annuelle supplémentaire</strong>, soit 9,40 € par mois à vie.</p>
                <p>Ce calcul illustre le <strong>dilemme classique entre net immédiat et droits futurs</strong> : les primes exonérées sont plus avantageuses à court terme, mais les primes cotisées construisent des droits de retraite. Selon votre horizon de temps et votre stratégie patrimoniale, le meilleur choix peut varier.</p>
            """
        },
        {
            "slug": "13eme-mois-brut-net",
            "title": "13ème Mois Brut Net 2026 : Calcul Gratuit et Cotisations",
            "desc": "Calculez votre 13ème mois brut en net en 2026. Cotisations sociales détaillées, impact sur votre impôt sur le revenu et modalités de versement. Calcul gratuit.",
            "kw": "13ème mois brut net, treizième mois cotisations, prime 13eme mois net, calcul 13eme mois",
            "content": """
                <h2 class="text-xl font-semibold text-slate-900">Qu'est-ce que le 13ème mois ?</h2>
                <p>Le <strong>13ème mois</strong> (ou "treizième mois") est une <strong>prime équivalant à un mois de salaire supplémentaire</strong> versée par l'employeur. Contrairement à ce que son nom suggère, ce n'est pas un mois de travail en plus, mais une gratification financière qui s'ajoute aux 12 mois de salaire normal.</p>
                <p>Le 13ème mois <strong>n'est pas obligatoire légalement</strong>. Il doit être prévu soit par :</p>
                <ul class="space-y-1">
                    <li>Votre <strong>convention collective</strong> (ex : Syntec, Métallurgie, Banque)</li>
                    <li>Votre <strong>contrat de travail</strong></li>
                    <li>Un <strong>usage d'entreprise</strong> (pratique répétée, générale et constante)</li>
                    <li>Un <strong>accord d'entreprise</strong></li>
                </ul>
                <p>Environ <strong>35% des salariés</strong> bénéficient d'un 13ème mois en France, principalement dans les grandes entreprises et certains secteurs (banque, assurance, industrie).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Cotisations sociales sur le 13ème mois</h2>
                <p>Le 13ème mois est traité fiscalement et socialement comme du salaire classique. Il est soumis à :</p>
                <ul class="space-y-2">
                    <li><strong>Cotisations sociales salariales</strong> : environ 22% (non-cadre) ou 25% (cadre)</li>
                    <li><strong>Cotisations patronales</strong> : environ 42-45% (payées par l'employeur)</li>
                    <li><strong>Impôt sur le revenu</strong> : via le prélèvement à la source, au taux habituel</li>
                </ul>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Exemples de conversion brut → net</h3>
                <p>Pour un 13ème mois de <strong>2 500 € brut</strong> (non-cadre, taux PAS 5%) :</p>
                <ul class="space-y-1">
                    <li>Brut : 2 500 €</li>
                    <li>Cotisations salariales (22%) : -550 €</li>
                    <li><strong>Net avant impôt</strong> : 1 950 €</li>
                    <li>Prélèvement à la source (5% du net imposable) : ~100 €</li>
                    <li><strong>Net après impôt</strong> : ~1 850 €</li>
                </ul>

                <p class="mt-4">Pour un 13ème mois de <strong>4 000 € brut</strong> (cadre, taux PAS 10%) :</p>
                <ul class="space-y-1">
                    <li>Brut : 4 000 €</li>
                    <li>Cotisations salariales (25%) : -1 000 €</li>
                    <li><strong>Net avant impôt</strong> : 3 000 €</li>
                    <li>Prélèvement à la source (10% du net imposable) : ~308 €</li>
                    <li><strong>Net après impôt</strong> : ~2 692 €</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Modalités de versement du 13ème mois</h2>
                <p>Le 13ème mois peut être versé selon différentes modalités, définies par la convention collective ou le contrat de travail :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">1. Versement en une fois</h3>
                <p>Le plus courant : versement en <strong>décembre</strong> (souvent avec le salaire de décembre ou début janvier). Certaines entreprises versent en novembre ou à une autre période définie.</p>
                <p><strong>Avantage</strong> : grosse rentrée d'argent pour les fêtes de fin d'année. <strong>Inconvénient</strong> : impact fiscal important ce mois-là (prélèvement à la source plus élevé).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">2. Versement en deux fois</h3>
                <p>Pratique fréquente : <strong>moitié en juin/juillet</strong> (prime de vacances) + <strong>moitié en décembre</strong> (prime de fin d'année).</p>
                <p><strong>Avantage</strong> : étalement de la trésorerie et du prélèvement à la source. <strong>Inconvénient</strong> : moins spectaculaire qu'un versement unique.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">3. Mensualisation (lissage)</h3>
                <p>Le 13ème mois est divisé par 12 et <strong>ajouté chaque mois au salaire de base</strong>. Par exemple, pour un salaire de 2 400 € brut, vous toucherez 2 400 + 200 = 2 600 € brut chaque mois.</p>
                <p><strong>Avantage</strong> : régularité du revenu, pas de variation du prélèvement à la source. <strong>Inconvénient</strong> : psychologiquement moins gratifiant (pas d'effet "prime").</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Calcul du 13ème mois : sur quelle base ?</h2>
                <p>Le 13ème mois correspond généralement à <strong>un mois de salaire brut de base</strong>, mais les modalités de calcul varient selon les accords :</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Méthode 1 : Salaire fixe du mois</h3>
                <p>Le 13ème mois = salaire brut du mois de référence (souvent décembre). Simple et direct.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Méthode 2 : Moyenne des 12 derniers mois</h3>
                <p>Le 13ème mois = (somme des 12 salaires bruts) / 12. Avantage : lisse les variations (primes, heures sup).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Méthode 3 : Salaire de base uniquement</h3>
                <p>Le 13ème mois = salaire de base hors primes, heures sup et avantages. Moins favorable pour le salarié.</p>

                <p class="mt-4"><strong>Vérifiez votre convention collective</strong> pour connaître la méthode applicable dans votre secteur.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Prorata et conditions d'ancienneté</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Prorata en cas d'année incomplète</h3>
                <p>Si vous n'avez pas travaillé toute l'année (embauche en cours d'année, démission, licenciement), le 13ème mois est généralement calculé <strong>au prorata temporis</strong> :</p>
                <p><strong>Formule</strong> : 13ème mois = (salaire mensuel brut) × (nombre de mois travaillés) / 12</p>
                <p><strong>Exemple</strong> : Embauché le 1er avril, salaire de 3 000 € brut. Vous avez travaillé 9 mois (avril à décembre). 13ème mois = 3 000 × 9/12 = <strong>2 250 € brut</strong>.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Conditions de présence</h3>
                <p>Certains accords prévoient une <strong>condition de présence</strong> au moment du versement. Si vous démissionnez en novembre et que le 13ème mois est versé en décembre, vous pourriez le perdre (sauf clause de proratisation dans la convention collective ou le contrat).</p>
                <p><strong>Conseil</strong> : si vous envisagez de démissionner en fin d'année, vérifiez les conditions de votre 13ème mois. Parfois, attendre janvier peut vous faire gagner un mois de salaire supplémentaire.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Impact fiscal du 13ème mois</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Prélèvement à la source</h3>
                <p>Si votre 13ème mois est versé en une fois en décembre, votre <strong>net imposable du mois</strong> double environ. Conséquence : votre prélèvement à la source sera calculé sur ce montant gonflé, ce qui peut créer un prélèvement important en janvier.</p>
                <p><strong>Exemple</strong> : Net imposable habituel de 2 000 €, taux PAS de 5% → prélèvement de 100 € par mois. En décembre avec 13ème mois : net imposable de 4 000 € → prélèvement de 200 € ce mois-là.</p>
                <p><strong>Régularisation</strong> : le surplus sera régularisé lors de votre déclaration de revenus en septembre N+1. Vous ne payez pas plus d'impôt au total, juste de manière anticipée.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Risque de changement de tranche</h3>
                <p>Si vous êtes proche d'un seuil de tranche d'imposition, le 13ème mois peut vous faire basculer dans la tranche supérieure pour l'année. Cependant, seule la partie au-delà du seuil est taxée au taux supérieur (impôt progressif), donc l'impact est limité.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">13ème mois vs autres primes : comparaison</h2>
                <table class="w-full text-sm border-collapse mt-4">
                    <thead><tr class="border-b-2 border-slate-300">
                        <th class="py-2 text-left">Type de prime</th>
                        <th class="py-2 text-right">Cotisations</th>
                        <th class="py-2 text-right">Impôt</th>
                        <th class="py-2 text-right">Conditions</th>
                    </tr></thead>
                    <tbody>
                        <tr class="border-b border-slate-100"><td class="py-2">13ème mois</td><td class="py-2 text-right">22-25%</td><td class="py-2 text-right">Oui</td><td class="py-2 text-right">Conventionnel/contractuel</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Prime de vacances</td><td class="py-2 text-right">22-25%</td><td class="py-2 text-right">Oui</td><td class="py-2 text-right">Usage/accord</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">Prime de performance</td><td class="py-2 text-right">22-25%</td><td class="py-2 text-right">Oui</td><td class="py-2 text-right">Objectifs atteints</td></tr>
                        <tr class="border-b border-slate-100"><td class="py-2">PPV (Prime Partage Valeur)</td><td class="py-2 text-right">0%</td><td class="py-2 text-right">Non</td><td class="py-2 text-right">Limite 3 000-6 000 €</td></tr>
                        <tr><td class="py-2">Intéressement (sur PEE)</td><td class="py-2 text-right">9,7%</td><td class="py-2 text-right">Non</td><td class="py-2 text-right">Accord d'intéressement</td></tr>
                    </tbody>
                </table>
                <p class="mt-4">Le 13ème mois est moins avantageux fiscalement que la PPV ou l'intéressement placé, mais c'est une prime garantie et versée en cash.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Spécificités sectorielles</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Convention collective Syntec</h3>
                <p>13ème mois obligatoire pour les ETAM (employés, techniciens, agents de maîtrise). Versement en décembre, prorata si ancienneté < 1 an.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Convention collective de la Métallurgie</h3>
                <p>Prime de fin d'année obligatoire (équivalent du 13ème mois) pour les ouvriers et ETAM. Montant variable selon les régions et les accords locaux.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Secteur bancaire</h3>
                <p>13ème mois quasi systématique, souvent complété par une prime de vacances (14ème mois partiel).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Fonction publique</h3>
                <p>Pas de 13ème mois dans la fonction publique, mais existence d'une <strong>prime annuelle</strong> (anciennement "prime de fin d'année") d'environ 1 mois de traitement pour certaines catégories.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">13ème mois et rupture du contrat</h2>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">En cas de licenciement</h3>
                <p>Le 13ème mois proratisé est généralement dû, même si vous partez avant la date de versement habituelle (sauf clause contraire explicite).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">En cas de démission</h3>
                <p>Dépend des clauses de votre contrat ou convention collective. Certains accords prévoient une perte totale si départ avant la date de versement, d'autres un prorata.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">En cas de retraite</h3>
                <p>Généralement, prorata jusqu'à la date de départ effectif.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Conseils pratiques</h2>
                <ul class="space-y-3">
                    <li><strong>Vérifiez vos droits</strong> : consultez votre convention collective sur Légifrance ou demandez au service RH pour savoir si vous avez droit au 13ème mois.</li>
                    <li><strong>Calculez le net</strong> : utilisez notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a> pour estimer précisément ce que vous toucherez.</li>
                    <li><strong>Anticipez le prélèvement à la source</strong> : si le 13ème mois est important, provisionnez pour le prélèvement du mois suivant ou modulez votre taux sur impots.gouv.fr.</li>
                    <li><strong>Privilégiez la mensualisation si disponible</strong> : cela évite les à-coups de trésorerie et lisse l'impact fiscal.</li>
                    <li><strong>En cas de départ</strong> : anticipez la date pour ne pas perdre votre 13ème mois. Parfois, attendre 1 mois de plus peut rapporter gros.</li>
                </ul>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">13ème mois et congés maladie / maternité</h2>
                <p>Le traitement du 13ème mois pendant les périodes d'absence (maladie, maternité, paternité) dépend des dispositions de votre convention collective :</p>
                <ul class="space-y-2">
                    <li><strong>Congé maladie</strong> : certains accords prévoient un abattement proportionnel à la durée d'absence. Par exemple, 1 mois de maladie = réduction de 1/12 du 13ème mois. D'autres accords maintiennent le 13ème mois intégralement.</li>
                    <li><strong>Congé maternité/paternité</strong> : ces absences sont assimilées à du temps de travail effectif dans la plupart des conventions collectives. Le 13ème mois est donc maintenu intégralement.</li>
                    <li><strong>Accident du travail</strong> : les périodes d'arrêt pour accident du travail sont généralement assimilées à du temps de travail, sans impact sur le 13ème mois.</li>
                </ul>
                <p>En cas de doute, consultez l'article de votre convention collective relatif au 13ème mois ou à la prime annuelle. Les dispositions varient considérablement d'un secteur à l'autre.</p>
            """
        },
    ]

    # Add FAQs to content pages
    for p in pages:
        if "différence" in p["slug"]:
            p["faqs"] = generate_faq_section([
                {"q": "Pourquoi y a-t-il une différence entre brut et net ?", "a": "La différence correspond aux cotisations sociales (retraite, santé, chômage, CSG/CRDS) qui financent notre protection sociale."},
                {"q": "Le brut ou le net est-il mentionné sur le contrat de travail ?", "a": "Le contrat mentionne toujours le salaire brut. Le net varie selon les cotisations et ne peut être garanti à l'avance."},
                {"q": "Peut-on négocier son salaire en net ?", "a": "Non, on négocie toujours en brut. Les cotisations étant obligatoires, l'employeur ne peut pas garantir un net fixe."},
                {"q": "La différence brut-net est-elle la même pour tous ?", "a": "Non, elle varie selon le statut (cadre/non-cadre), le niveau de salaire et certaines cotisations conventionnelles."},
                {"q": "Comment vérifier le calcul sur ma fiche de paie ?", "a": "Utilisez notre calculateur avec votre brut mensuel. Un écart de quelques euros est normal (mutuelle, tickets restaurant, prévoyance)."},
            ])
        elif "cotisations" in p["slug"]:
            p["faqs"] = generate_faq_section([
                {"q": "À quoi servent les cotisations sociales ?", "a": "Elles financent la Sécurité sociale : retraite, maladie, chômage, allocations familiales. C'est le modèle de protection sociale français."},
                {"q": "Peut-on être exonéré de cotisations sociales ?", "a": "Certains contrats (apprentissage, stage sous seuil) bénéficient d'exonérations partielles ou totales."},
                {"q": "Les cotisations changent-elles chaque année ?", "a": "Les taux sont révisés annuellement par décret, généralement avec de faibles variations."},
                {"q": "Où voir le détail des cotisations ?", "a": "Votre fiche de paie détaille toutes les cotisations salariales et patronales, ligne par ligne."},
                {"q": "Les cotisations sont-elles déductibles des impôts ?", "a": "Une partie de la CSG (6,80%) est déductible du revenu imposable. Le reste ne l'est pas."},
            ])
        elif "smic" in p["slug"]:
            p["faqs"] = generate_faq_section([
                {"q": "Le SMIC augmente-t-il chaque année ?", "a": "Oui, le SMIC est revalorisé au minimum au 1er janvier de chaque année, en fonction de l'inflation."},
                {"q": "Peut-on être payé moins que le SMIC ?", "a": "Non, sauf exceptions très rares (apprentis sous 18 ans, travailleurs handicapés avec autorisation). Le SMIC est le minimum légal."},
                {"q": "Le SMIC est-il le même en brut et en net ?", "a": "Non, le SMIC affiché (1 801,80 € en 2026) est le brut. Le net est d'environ 1 426 € après cotisations."},
                {"q": "Les primes sont-elles incluses dans le SMIC ?", "a": "Non, le SMIC est le salaire de base. Les primes (panier, transport, 13ème mois) s'ajoutent au SMIC."},
                {"q": "Le SMIC horaire permet-il de calculer les heures sup ?", "a": "Oui, les heures supplémentaires sont calculées sur la base du taux horaire brut, avec une majoration de 25% ou 50%."},
            ])
        else:
            p["faqs"] = generate_faq_section([
                {"q": "Cette information est-elle à jour pour 2026 ?", "a": "Oui, tous les taux et plafonds sont actualisés pour l'année 2026."},
                {"q": "Puis-je utiliser ces informations pour ma déclaration d'impôts ?", "a": "Ces informations sont indicatives. Pour votre déclaration, référez-vous aux montants exacts de votre fiche de paie."},
                {"q": "Ces calculs s'appliquent-ils à tous les secteurs ?", "a": "Les cotisations de base sont identiques. Certaines conventions collectives ajoutent des cotisations spécifiques."},
                {"q": "Comment obtenir un calcul personnalisé ?", "a": "Utilisez notre calculateur en haut de page avec vos données réelles (brut, statut, temps de travail)."},
                {"q": "Ces règles s'appliquent-elles aux indépendants ?", "a": "Non, les indépendants et auto-entrepreneurs ont des régimes de cotisations différents, avec des taux forfaitaires."},
            ])

    for p in pages:
        html = page_head(p["title"], p["desc"], f'{BASE_URL}/{p["slug"]}/', p["kw"])
        html += HEADER
        html += breadcrumb(p["title"].split(" :")[0].split(" 2026")[0])
        html += f'''
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 mb-6">{p["title"].split(" :")[0]}</h1>
            </div>
        </section>'''
        html += calculator_widget(2500, "non-cadre", "brut")
        html += f'''
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>'''
        if "faqs" in p and p["faqs"]:
            html += p["faqs"]
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\n</body></html>"
        write_page(p["slug"], html)


# ── 4. Pages outils complémentaires ──────────────────────────────────────────

def gen_tool_pages():
    # Calculateur coût employeur
    html = page_head(
        "Calculateur Coût Employeur 2026 : Simulez le Super-Brut",
        "Calculez le coût total employeur (super-brut) pour un salarié en 2026. Cotisations patronales détaillées, charges sociales et simulateur gratuit instantané.",
        f"{BASE_URL}/calculateur-cout-employeur/",
        "calculateur coût employeur, super brut, charges patronales, coût salarié"
    )
    html += HEADER
    html += breadcrumb("Calculateur Coût Employeur")
    html += '''
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 mb-6">Calculateur <span class="text-brand-600">Coût Employeur</span> 2026</h1>
                <p class="text-slate-500">Calculez le coût total pour l'entreprise (super-brut) en incluant les cotisations patronales.</p>
            </div>
        </section>

        <section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-xs text-brand-600 font-medium">Coût employeur</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-coût">–</p>
                            <p class="text-xs text-slate-500">par mois</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-xs text-slate-600 font-medium">Cotisations patronales</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-patron">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-xs text-slate-600 font-medium">Net salarié</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const sel = document.getElementById('widget-statut');
        function calc() {
            const r = calculerBrutVersNet(parseFloat(inp.value)||0, sel.value, 1);
            document.getElementById('res-coût').textContent = formatMoney(r.coutEmployeur);
            document.getElementById('res-patron').textContent = formatMoney(r.totalPatronal);
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>

        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                <h2 class="text-xl font-semibold text-slate-900">Comprendre le coût employeur</h2>
                <p>Le <strong>coût employeur</strong> représente le montant total que l'entreprise dépense pour un salarié. Il comprend le salaire brut auquel s'ajoutent les cotisations patronales (environ 45% du brut).</p>
                <p>Pour un salaire brut de 2 500 €, le coût employeur est d'environ <strong>3 625 €</strong>. L'entreprise dépense donc 45% de plus que ce qu'elle vous verse en brut.</p>
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Ratio net perçu / coût employeur</h3>
                <p>Sur les 3 625 € dépensés par l'employeur, le salarié ne perçoit qu'environ 1 950 € net. Cela signifie que le salarié touche environ <strong>54% du coût total</strong>. Le reste finance la protection sociale.</p>
            </div>
        </section>'''
    html += links_grid("Pages connexes", RELATED_LINKS)
    html += FOOTER
    html += "\n</body></html>"
    write_page("calculateur-coût-employeur", html)

    # Calculateur heures supplémentaires
    html = page_head(
        "Heures Supplémentaires 2026 : Calcul Brut Net et Coût",
        "Calculez le montant brut, net et coût employeur de vos heures supplémentaires en 2026. CDI, CDD, intérim. Majoration 25% à 50% et exonération fiscale.",
        f"{BASE_URL}/calculateur-heures-supplementaires/",
        "calculateur heures supplémentaires, heures sup brut net, majoration heures supplémentaires, coût employeur heures sup"
    )
    html += HEADER
    html += breadcrumb("Calculateur Heures Supplémentaires")
    html += '''
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 mb-4">Calculateur <span class="text-brand-600">Heures Supplémentaires</span> 2026</h1>
                <p class="text-slate-500">Calculez le brut, le net salarié et le coût employeur de vos heures supplémentaires selon votre contrat (CDI, CDD, Intérim).</p>
            </div>
        </section>

        <section class="py-8 px-4">
            <div class="mx-auto max-w-4xl">
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                        <div>
                            <label for="hs-brut" class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel (base 35h)</label>
                            <input type="number" id="hs-brut" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label for="hs-heures" class="block text-sm font-medium text-slate-700 mb-1">Heures sup / semaine</label>
                            <input type="number" id="hs-heures" value="4" min="1" max="20" step="1"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label for="hs-contrat" class="block text-sm font-medium text-slate-700 mb-1">Type de contrat</label>
                            <select id="hs-contrat" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="cdi" selected>CDI</option>
                                <option value="cdd">CDD</option>
                                <option value="interim">Intérim</option>
                            </select>
                        </div>
                        <div>
                            <label for="hs-statut" class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="hs-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>

                    <h3 class="text-sm font-semibold text-slate-900 mb-3">Vos heures supplémentaires vous rapportent</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-xs text-brand-600 font-medium">Brut heures sup / mois</p>
                            <p class="text-2xl font-bold text-slate-900" id="hs-res-brut">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-xs text-emerald-700 font-medium">Net heures sup / mois</p>
                            <p class="text-2xl font-bold text-slate-900" id="hs-res-net">–</p>
                            <p class="text-xs text-slate-500">exonéré d'impôt</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-xs text-slate-600 font-medium">Coût employeur heures sup</p>
                            <p class="text-2xl font-bold text-slate-900" id="hs-res-coût">–</p>
                        </div>
                    </div>

                    <h3 class="text-sm font-semibold text-slate-900 mb-3">Total (base + heures sup)</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-xs text-slate-600 font-medium">Total brut / mois</p>
                            <p class="text-2xl font-bold text-slate-900" id="hs-tot-brut">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-xs text-slate-600 font-medium">Total net / mois</p>
                            <p class="text-2xl font-bold text-slate-900" id="hs-tot-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-xs text-slate-600 font-medium">Total coût employeur</p>
                            <p class="text-2xl font-bold text-slate-900" id="hs-tot-coût">–</p>
                        </div>
                    </div>

                    <div id="hs-primes" class="hidden mt-6 rounded-xl bg-amber-50 border border-amber-200 p-4">
                        <h3 class="text-sm font-semibold text-slate-900 mb-3">Primes de fin de contrat</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="hs-primes-grid"></div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        var brut = document.getElementById('hs-brut');
        var heures = document.getElementById('hs-heures');
        var contrat = document.getElementById('hs-contrat');
        var statut = document.getElementById('hs-statut');

        function calc() {
            var salaireBrut = parseFloat(brut.value) || 0;
            var hsSemaine = Math.min(Math.max(parseInt(heures.value) || 0, 0), 20);
            var st = statut.value;
            var ct = contrat.value;

            // Taux horaire et volume mensuel
            var tauxH = salaireBrut / 151.67;
            var hsMois = hsSemaine * 52 / 12;

            // Majoration : premières 8h à +25%, au-delà à +50%
            var h25 = Math.min(hsSemaine, 8);
            var h50 = Math.max(hsSemaine - 8, 0);
            var brutHS = (h25 * tauxH * 1.25 + h50 * tauxH * 1.50) * 52 / 12;

            // Cotisations salariales réduites sur HS (exonération vieillesse + retraite complémentaire)
            // Reste CSG/CRDS : 9.7% × 98.25% ≈ 9.53%, + CET 0.14% si cadre
            var tauxCotisHS = st === 'cadre' ? 0.0967 : 0.0953;
            var netHS = brutHS * (1 - tauxCotisHS);

            // Coût employeur HS via calculerBrutVersNet (différentiel)
            var rBase = calculerBrutVersNet(salaireBrut, st, 1);
            var rTotal = calculerBrutVersNet(salaireBrut + brutHS, st, 1);
            var coutHS = rTotal.coutEmployeur - rBase.coutEmployeur;

            // Totaux
            var totBrut = salaireBrut + brutHS;
            var totNet = rBase.netAvantImpot + netHS;
            var totCout = rTotal.coutEmployeur;

            document.getElementById('hs-res-brut').textContent = formatMoney(brutHS);
            document.getElementById('hs-res-net').textContent = formatMoney(netHS);
            document.getElementById('hs-res-coût').textContent = formatMoney(coutHS);
            document.getElementById('hs-tot-brut').textContent = formatMoney(totBrut);
            document.getElementById('hs-tot-net').textContent = formatMoney(totNet);
            document.getElementById('hs-tot-coût').textContent = formatMoney(totCout);

            // Primes CDD / Intérim
            var primesDiv = document.getElementById('hs-primes');
            var primesGrid = document.getElementById('hs-primes-grid');
            if (ct === 'cdd') {
                var precarite = totBrut * 0.10;
                primesGrid.innerHTML = '<div class="text-center"><p class="text-xs text-amber-700 font-medium">Prime de précarité (10%)</p><p class="text-xl font-bold text-slate-900">' + formatMoney(precarite) + '</p><p class="text-xs text-slate-500">par mois</p></div>';
                primesDiv.classList.remove('hidden');
            } else if (ct === 'interim') {
                var ifm = totBrut * 0.10;
                var iccp = (totBrut + ifm) * 0.10;
                primesGrid.innerHTML = '<div class="text-center"><p class="text-xs text-amber-700 font-medium">IFM - Indemnité de fin de mission (10%)</p><p class="text-xl font-bold text-slate-900">' + formatMoney(ifm) + '</p><p class="text-xs text-slate-500">par mois</p></div>' +
                    '<div class="text-center"><p class="text-xs text-amber-700 font-medium">ICCP - Congés payés (10%)</p><p class="text-xl font-bold text-slate-900">' + formatMoney(iccp) + '</p><p class="text-xs text-slate-500">par mois</p></div>';
                primesDiv.classList.remove('hidden');
            } else {
                primesDiv.classList.add('hidden');
            }
        }

        brut.addEventListener('input', calc);
        heures.addEventListener('input', calc);
        contrat.addEventListener('change', calc);
        statut.addEventListener('change', calc);
        calc();
    })();
    </script>

        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                <h2 class="text-xl font-semibold text-slate-900">Comment fonctionnent les heures supplémentaires ?</h2>
                <p>Les heures supplémentaires sont les heures travaillées au-delà de la durée légale de <strong>35 heures par semaine</strong>. Elles donnent lieu à une <strong>majoration de salaire obligatoire</strong> :</p>
                <ul>
                    <li><strong>+25%</strong> pour les 8 premières heures (de la 36e à la 43e heure)</li>
                    <li><strong>+50%</strong> au-delà (à partir de la 44e heure)</li>
                </ul>
                <p>Le contingent annuel d'heures supplémentaires est fixé à <strong>220 heures</strong> par salarié (sauf accord collectif différent).</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Avantage fiscal et social des heures supplémentaires</h2>
                <p>Depuis 2019, les heures supplémentaires bénéficient d'un double avantage :</p>
                <ul>
                    <li><strong>Exonération de cotisations salariales</strong> : réduction de 11,31% sur les cotisations vieillesse et retraite complémentaire. Seules la CSG/CRDS (~9,53%) restent dues.</li>
                    <li><strong>Exonération d'impôt sur le revenu</strong> : les heures supplémentaires sont exonérées d'impôt jusqu'à <strong>7 500 &euro; net par an</strong>.</li>
                </ul>
                <p>Concrètement, le net perçu pour une heure supplémentaire est environ <strong>90%</strong> du brut majoré, contre ~78% pour une heure normale.</p>

                <h2 class="text-xl font-semibold text-slate-900 mt-8">Différences CDI, CDD et Intérim</h2>
                <p>Le calcul des heures supplémentaires est identique quel que soit le contrat. La différence vient des <strong>primes de fin de contrat</strong> :</p>
                <ul>
                    <li><strong>CDI</strong> : pas de prime spécifique liée au contrat.</li>
                    <li><strong>CDD</strong> : prime de précarité de <strong>10%</strong> du salaire brut total (base + HS) versée en fin de contrat.</li>
                    <li><strong>Intérim</strong> : indemnité de fin de mission (IFM) de <strong>10%</strong> + indemnité compensatrice de congés payés (ICCP) de <strong>10%</strong> calculée sur le brut + IFM.</li>
                </ul>
                <p>Pour en savoir plus, consultez notre guide complet sur les <a href="/heures-supplementaires-brut-net/" class="text-brand-600 hover:text-brand-700">heures supplémentaires brut/net</a>.</p>
            </div>
        </section>'''
    html += links_grid("Pages connexes", RELATED_LINKS)
    html += FOOTER
    html += "\n</body></html>"
    write_page("calculateur-heures-supplémentaires", html)

    # Comparateur salaire par pays
    html = page_head(
        "Comparateur Salaire Net par Pays 2026 : France vs Europe",
        "Comparez le salaire net entre pays européens en 2026. France vs Belgique, Suisse, Luxembourg : cotisations sociales, fiscalité et pouvoir d'achat comparés.",
        f"{BASE_URL}/comparateur-salaire-net-par-pays/",
        "comparateur salaire pays, salaire net france belgique suisse, salaire europe comparaison"
    )
    html += HEADER
    html += breadcrumb("Comparateur Salaire Net par Pays")
    html += '''
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 mb-6">Comparateur <span class="text-brand-600">Salaire Net par Pays</span></h1>
                <p class="text-slate-500">Comparez le salaire net pour un même brut dans différents pays francophones européens.</p>
            </div>
        </section>

        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6">Comparaison pour 3 000 € brut mensuel</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="border-b-2 border-slate-200">
                                <th class="py-3 text-left font-semibold text-slate-900">Pays</th>
                                <th class="py-3 text-right font-semibold text-slate-900">Brut</th>
                                <th class="py-3 text-right font-semibold text-slate-900">Cotisations (%)</th>
                                <th class="py-3 text-right font-semibold text-slate-900">Net avant impôt</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="border-b border-slate-100"><td class="py-3">🇫🇷 France</td><td class="py-3 text-right">3 000 €</td><td class="py-3 text-right">~22%</td><td class="py-3 text-right font-medium">~2 340 €</td></tr>
                            <tr class="border-b border-slate-100"><td class="py-3">🇧🇪 Belgique</td><td class="py-3 text-right">3 000 €</td><td class="py-3 text-right">~13,07%</td><td class="py-3 text-right font-medium">~2 608 €</td></tr>
                            <tr class="border-b border-slate-100"><td class="py-3">🇨🇭 Suisse</td><td class="py-3 text-right">3 000 CHF</td><td class="py-3 text-right">~12-15%</td><td class="py-3 text-right font-medium">~2 550 CHF</td></tr>
                            <tr class="border-b border-slate-100"><td class="py-3">🇱🇺 Luxembourg</td><td class="py-3 text-right">3 000 €</td><td class="py-3 text-right">~12,5%</td><td class="py-3 text-right font-medium">~2 625 €</td></tr>
                            <tr><td class="py-3">🇩🇪 Allemagne</td><td class="py-3 text-right">3 000 €</td><td class="py-3 text-right">~20%</td><td class="py-3 text-right font-medium">~2 400 €</td></tr>
                        </tbody>
                    </table>
                </div>
                <p class="text-xs text-slate-400 mt-4">* Estimations indicatives, les taux varient selon la situation personnelle et le canton/région. L'impôt sur le revenu n'est pas inclus.</p>
            </div>
        </section>

        <section class="py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                <h2 class="text-xl font-semibold text-slate-900">Pourquoi les cotisations varient-elles autant ?</h2>
                <p>Chaque pays à son propre système de protection sociale. La France à l'un des taux de cotisations les plus élevés d'Europe, mais en contrepartie offre une couverture sociale très complète (santé, retraite, chômage, famille).</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">France : cotisations élevées, protection forte</h3>
                <p>Avec environ 22% de cotisations salariales, la France offre une couverture maladie universelle, des allocations familiales généreuses, un système de retraite par répartition et une assurance chômage.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Suisse : cotisations basses, coût de la vie élevé</h3>
                <p>Les cotisations sont plus basses, mais l'assurance maladie est obligatoire et entièrement à la charge du salarié (300-500 CHF/mois en moyenne). Le coût de la vie est aussi nettement plus élevé.</p>

                <h3 class="text-lg font-semibold text-slate-900 mt-6">Belgique : cotisations basses, impôts élevés</h3>
                <p>Les cotisations sociales salariales sont plus basses qu'en France (~13%), mais l'impôt sur le revenu est parmi les plus élevés d'Europe (jusqu'à 50%), ce qui réduit fortement le net après impôt.</p>

                <p class="mt-6">Pour calculer votre salaire net en France précisément, utilisez notre <a href="/" class="text-brand-600 hover:text-brand-700">calculateur brut/net</a>.</p>
            </div>
        </section>'''
    html += links_grid("Pages connexes", RELATED_LINKS)
    html += FOOTER
    html += "\n</body></html>"
    write_page("comparateur-salaire-net-par-pays", html)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Génération des pages Phase 2 ===\n")

    print("1. Pages par statut professionnel...")
    gen_status_pages()

    print("\n2. Pages par période...")
    gen_period_pages()

    print("\n3. Pages de contenu éducatif...")
    gen_content_pages()

    print("\n4. Pages outils complémentaires...")
    gen_tool_pages()

    print("\n=== Terminé ! ===")


if __name__ == "__main__":
    main()
