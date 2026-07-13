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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/img/logo.svg">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:locale" content="fr_FR">
    <meta property="og:site_name" content="SalaireBrutNet">
    <meta name="robots" content="index, follow">
    <meta name="keywords" content="{keywords}">
    <link rel="stylesheet" href="/css/fonts.css">
    <link rel="stylesheet" href="/css/style.css">
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
</head>'''


HEADER = '''
<body class="bg-slate-50 text-slate-600 antialiased selection:bg-brand-100 selection:text-brand-900 flex flex-col min-h-screen">
    <header class="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/90 backdrop-blur-md">
        <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
            <a href="/" class="flex items-center gap-2">
                <img src="/img/logo.svg" alt="SalaireBrutNet" class="h-8 w-8">
                <span class="text-base font-semibold tracking-tight text-slate-900">SalaireBrutNet</span>
            </a>
            <nav class="hidden md:flex gap-8">
                <a href="/" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Calculateur</a>
                <a href="/simulateur-impot-sur-le-revenu/" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Simulateur Impôts</a>
                <a href="/mission/" class="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Notre Mission</a>
            </nav>
        </div>
    </header>
    <main class="flex-grow">
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
            <div class="flex gap-4">
                <a href="/" class="text-xs text-slate-500 hover:text-slate-900">Calculateur</a>
                <a href="/mentions-legales/" class="text-xs text-slate-500 hover:text-slate-900">Mentions légales</a>
                <a href="/mission/" class="text-xs text-slate-500 hover:text-slate-900">Notre Mission</a>
                <a href="/simulateur-impot-sur-le-revenu/" class="text-xs text-slate-500 hover:text-slate-900">Simulateur Impôts</a>
            </div>
        </div>
    </footer>
    <script src="/js/brut-net.js"></script>
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
