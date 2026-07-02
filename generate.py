#!/usr/bin/env python3
"""
Génère les pages programmatiques brut→net et net→brut
ainsi que le sitemap.xml mis à jour.

Usage : python generate.py
"""

import os
import sys
import math
from datetime import date

# Add scripts/ to path for content module import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from content_salary_pages import generate_contextual_content

# ── Configuration ──────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://salairebrutonet.com"
MONTANT_MIN = 1000
MONTANT_MAX = 10000
MONTANT_STEP = 100

# Paliers intermédiaires de 50€ entre 1000 et 5000
MONTANT_50_MIN = 1000
MONTANT_50_MAX = 5000
MONTANT_50_STEP = 50

PSS_MENSUEL = 3864
SMIC_MENSUEL_BRUT = 1801.80

MONTANTS_POPULAIRES = [1000, 1200, 1500, 1800, 2000, 2500, 3000, 3500, 4000, 5000]

# ── Fonctions de calcul (miroir de js/brut-net.js) ─────────────────────────────

def calculer_cotisations_salariales(brut_mensuel, statut):
    is_cadre = statut == "cadre"
    t1 = min(brut_mensuel, PSS_MENSUEL)
    t2 = max(0, brut_mensuel - PSS_MENSUEL)
    assiette_csg = brut_mensuel * 0.9825

    cotisations = {
        "Vieillesse plafonnée": t1 * 0.069,
        "Vieillesse déplafonnée": brut_mensuel * 0.004,
        "AGIRC-ARRCO T1": t1 * 0.0315,
        "AGIRC-ARRCO T2": t2 * 0.0864,
        "CEG T1": t1 * 0.0086,
        "CEG T2": t2 * 0.0108,
        "CSG déductible": assiette_csg * 0.068,
        "CSG non déductible": assiette_csg * 0.024,
        "CRDS": assiette_csg * 0.005,
    }
    if is_cadre:
        cotisations["CET (cadre)"] = brut_mensuel * 0.0014

    total = sum(cotisations.values())
    return cotisations, total


def calculer_cotisations_patronales(brut_mensuel):
    t1 = min(brut_mensuel, PSS_MENSUEL)
    t2 = max(0, brut_mensuel - PSS_MENSUEL)
    seuil_alloc = SMIC_MENSUEL_BRUT * 3.5
    taux_alloc = 0.0345 if brut_mensuel <= seuil_alloc else 0.0525

    cotisations = {
        "Maladie": brut_mensuel * 0.07,
        "Vieillesse plafonnée": t1 * 0.0855,
        "Vieillesse déplafonnée": brut_mensuel * 0.0202,
        "Allocations familiales": brut_mensuel * taux_alloc,
        "Chômage": t1 * 0.0405,
        "AGIRC-ARRCO T1": t1 * 0.0472,
        "AGIRC-ARRCO T2": t2 * 0.1295,
        "AT/MP (taux moyen)": brut_mensuel * 0.01,
        "CEG T1": t1 * 0.0129,
        "CEG T2": t2 * 0.0162,
        "CET": brut_mensuel * 0.0021,
    }
    total = sum(cotisations.values())
    return cotisations, total


def estimer_impot_revenu(net_imposable_annuel):
    tranches = [
        (11497, 0),
        (29315, 0.11),
        (83823, 0.30),
        (180294, 0.41),
        (float("inf"), 0.45),
    ]
    impot = 0
    prev = 0
    for limit, taux in tranches:
        if net_imposable_annuel <= prev:
            break
        base = min(net_imposable_annuel, limit) - prev
        impot += base * taux
        prev = limit
    return round(impot)


def calculer_brut_vers_net(brut_mensuel, statut):
    cotis_sal, total_sal = calculer_cotisations_salariales(brut_mensuel, statut)
    cotis_pat, total_pat = calculer_cotisations_patronales(brut_mensuel)

    net_avant_impot = brut_mensuel - total_sal

    csg_non_ded = cotis_sal.get("CSG non déductible", 0)
    crds = cotis_sal.get("CRDS", 0)
    net_imposable_mensuel = brut_mensuel - total_sal + csg_non_ded + crds
    net_imposable_annuel = net_imposable_mensuel * 12

    abattement = min(max(net_imposable_annuel * 0.1, 495), 14171)
    net_imposable_apres_abattement = net_imposable_annuel - abattement

    impot_annuel = estimer_impot_revenu(net_imposable_apres_abattement)
    impot_mensuel = round(impot_annuel / 12)

    net_apres_impot = net_avant_impot - impot_mensuel
    cout_employeur = brut_mensuel + total_pat

    taux_cotisations = round((total_sal / brut_mensuel) * 1000) / 10 if brut_mensuel > 0 else 0

    return {
        "brut_mensuel": brut_mensuel,
        "brut_annuel": brut_mensuel * 12,
        "net_avant_impot": round(net_avant_impot, 2),
        "net_apres_impot": round(net_apres_impot, 2),
        "impot_mensuel": impot_mensuel,
        "cout_employeur": round(cout_employeur, 2),
        "total_salarial": round(total_sal, 2),
        "total_patronal": round(total_pat, 2),
        "taux_cotisations": taux_cotisations,
        "detail_salariales": cotis_sal,
    }


def calculer_net_vers_brut(net_cible, statut):
    brut_estime = net_cible * 1.3
    for _ in range(50):
        result = calculer_brut_vers_net(brut_estime, statut)
        diff = result["net_avant_impot"] - net_cible
        if abs(diff) < 0.01:
            break
        brut_estime -= diff * 0.7
    return calculer_brut_vers_net(brut_estime, statut)


# ── Formatage ──────────────────────────────────────────────────────────────────

def fmt(val):
    """Format number French style: 1 500"""
    return f"{round(val):,}".replace(",", " ").replace(".", ",")


def fmt2(val):
    """Format number with 2 decimals French style"""
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")


# ── Génération HTML ────────────────────────────────────────────────────────────

def build_cotisations_table_html(cotisations, total):
    """Build an HTML table for cotisations."""
    rows = ""
    for label, montant in cotisations.items():
        if montant < 0.01:
            continue
        rows += f"""<tr class="border-b border-slate-50">
            <td class="py-1.5 text-slate-600 text-sm">{label}</td>
            <td class="py-1.5 text-right text-sm font-medium text-slate-900">{fmt2(montant)} €</td>
        </tr>\n"""
    rows += f"""<tr class="border-t border-slate-200 font-semibold">
        <td class="py-1.5 text-slate-900 text-sm">Total</td>
        <td class="py-1.5 text-right text-sm text-slate-900">{fmt2(total)} €</td>
    </tr>"""
    return f"""<table class="w-full text-sm">
        <thead><tr class="border-b border-slate-100">
            <th class="pb-2 text-left font-medium text-slate-500">Cotisation</th>
            <th class="pb-2 text-right font-medium text-slate-500">Montant</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table>"""


def build_liens_proches(montant, direction="brut-en-net"):
    """Build HTML for nearby amount links (X00 steps only)."""
    liens = []
    all_m = get_main_montants()
    idx = all_m.index(montant) if montant in all_m else -1
    offsets_idx = [-2, -1, 1, 2]
    for oi in offsets_idx:
        ni = idx + oi
        if 0 <= ni < len(all_m):
            m = all_m[ni]
            slug = f"/{m}-euros-{direction}/"
            label = f"{fmt(m)} €"
            sub_label = direction.replace("-", " ")
            liens.append(
                f'<a href="{slug}" class="block rounded-xl border border-slate-200 bg-white p-3 text-center hover:border-brand-300 hover:shadow-sm transition-all">'
                f'<span class="block text-lg font-bold text-slate-900">{label}</span>'
                f'<span class="block text-xs text-slate-500">{sub_label}</span></a>'
            )
    return "\n".join(liens)


def build_liens_populaires(direction="brut-en-net"):
    """Build HTML for popular amount links."""
    liens = []
    for m in MONTANTS_POPULAIRES:
        slug = f"/{m}-euros-{direction}/"
        label = f"{fmt(m)} €"
        sub_label = direction.replace("-", " ")
        liens.append(
            f'<a href="{slug}" class="block rounded-xl border border-slate-200 bg-white p-3 text-center hover:border-brand-300 hover:shadow-sm transition-all">'
            f'<span class="block text-lg font-bold text-slate-900">{label}</span>'
            f'<span class="block text-xs text-slate-500">{sub_label}</span></a>'
        )
    return "\n".join(liens)


def build_description_brut_net(montant, nc, c):
    """Build contextual description for brut→net pages."""
    brut_annuel = montant * 12
    net_annuel_nc = round(nc["net_avant_impot"] * 12)

    # Contextual comparisons
    if montant < 1800:
        context = f"Ce salaire se situe en dessous du salaire médian français (environ 2 100 € brut mensuel)."
    elif montant <= 2500:
        context = f"Ce salaire se situe autour du salaire médian français."
    elif montant <= 4000:
        context = f"Ce salaire est supérieur au salaire médian français et se situe dans la tranche haute des rémunérations."
    else:
        context = f"Ce salaire est nettement supérieur au salaire médian français et correspond à un profil senior ou cadre supérieur."

    base = f"""<h2 class="text-xl font-semibold text-slate-900">{fmt(montant)} € brut en net : tout savoir</h2>
<p>Avec un salaire de <strong>{fmt(montant)} € brut mensuel</strong>, vous toucherez environ <strong>{fmt(nc['net_avant_impot'])} € net par mois</strong> si vous êtes non-cadre, ou <strong>{fmt(c['net_avant_impot'])} € net</strong> si vous êtes cadre. {context}</p>
<p>Sur une base annuelle, cela représente <strong>{fmt(brut_annuel)} € brut</strong> soit environ <strong>{fmt(net_annuel_nc)} € net annuel</strong> avant prélèvement à la source pour un non-cadre.</p>
<p>Le coût total pour votre employeur est d'environ <strong>{fmt(nc['cout_employeur'])} € par mois</strong>, soit {fmt(round(nc['cout_employeur'] * 12))} € par an, en incluant les cotisations patronales.</p>
<p>Après prélèvement à la source (estimation pour un célibataire sans enfant), votre salaire net mensuel serait d'environ <strong>{fmt(nc['net_apres_impot'])} €</strong> (non-cadre) ou <strong>{fmt(c['net_apres_impot'])} €</strong> (cadre).</p>"""
    contextual = generate_contextual_content(montant, "brut-en-net")
    return base + "\n" + contextual


def build_description_net_brut(montant, nc, c):
    """Build contextual description for net→brut pages."""
    base = f"""<h2 class="text-xl font-semibold text-slate-900">{fmt(montant)} € net en brut : tout savoir</h2>
<p>Si vous souhaitez toucher <strong>{fmt(montant)} € net par mois</strong>, vous devez négocier un salaire brut d'environ <strong>{fmt(nc['brut_mensuel'])} € brut mensuel</strong> en tant que non-cadre, ou <strong>{fmt(c['brut_mensuel'])} € brut</strong> en tant que cadre.</p>
<p>La différence entre les deux statuts s'explique par la cotisation CET (Contribution d'Équilibre Technique) supplémentaire de 0,14% pour les cadres, qui nécessite un brut légèrement plus élevé pour atteindre le même net.</p>
<p>Sur une base annuelle, cela correspond à un salaire brut de <strong>{fmt(nc['brut_annuel'])} €</strong> (non-cadre) ou <strong>{fmt(c['brut_annuel'])} €</strong> (cadre).</p>
<p>Le coût total pour l'employeur serait d'environ <strong>{fmt(nc['cout_employeur'])} € par mois</strong> (non-cadre), soit le brut majoré d'environ 45% de cotisations patronales.</p>"""
    contextual = generate_contextual_content(montant, "net-en-brut")
    return base + "\n" + contextual


# ── Génération des pages ───────────────────────────────────────────────────────

def get_main_montants():
    """Get main montants: 100€ steps only (1000-10000)."""
    return list(range(MONTANT_MIN, MONTANT_MAX + 1, MONTANT_STEP))


def get_redirect_montants():
    """Get X50 montants that should be redirect pages (1050, 1150, ..., 4950)."""
    return [m for m in range(MONTANT_50_MIN + MONTANT_50_STEP, MONTANT_50_MAX + 1, MONTANT_50_STEP) if m % 100 != 0]


def get_all_montants():
    """Get all montants: 100€ steps (1000-10000) + 50€ steps (1050-4950)."""
    return sorted(set(get_main_montants() + get_redirect_montants()))


def generate_brut_net_pages(template):
    """Generate all brut→net pages (X00 steps only)."""
    montants = get_main_montants()
    for montant in montants:
        nc = calculer_brut_vers_net(montant, "non-cadre")
        c = calculer_brut_vers_net(montant, "cadre")

        # For the FAQ about annual brut
        brut_mensuel_annuel = round(montant / 12, 2)
        result_mensuel_annuel = calculer_brut_vers_net(brut_mensuel_annuel, "non-cadre")

        replacements = {
            "{{MONTANT}}": str(montant),
            "{{MONTANT_FORMATE}}": fmt(montant),
            "{{NET_NON_CADRE_FORMATE}}": fmt(nc["net_avant_impot"]),
            "{{NET_CADRE_FORMATE}}": fmt(c["net_avant_impot"]),
            "{{COUT_EMPLOYEUR_FORMATE}}": fmt(nc["cout_employeur"]),
            "{{COTISATIONS_NC_FORMATE}}": fmt(nc["total_salarial"]),
            "{{COTISATIONS_C_FORMATE}}": fmt(c["total_salarial"]),
            "{{IMPOT_NC_FORMATE}}": fmt(nc["impot_mensuel"]),
            "{{IMPOT_C_FORMATE}}": fmt(c["impot_mensuel"]),
            "{{NET_APRES_IMPOT_NC_FORMATE}}": fmt(nc["net_apres_impot"]),
            "{{NET_APRES_IMPOT_C_FORMATE}}": fmt(c["net_apres_impot"]),
            "{{BRUT_ANNUEL_FORMATE}}": fmt(montant * 12),
            "{{TAUX_COTISATIONS_NC}}": str(nc["taux_cotisations"]),
            "{{TAUX_COTISATIONS_C}}": str(c["taux_cotisations"]),
            "{{TABLE_COTISATIONS_NC}}": build_cotisations_table_html(
                nc["detail_salariales"], nc["total_salarial"]
            ),
            "{{TABLE_COTISATIONS_C}}": build_cotisations_table_html(
                c["detail_salariales"], c["total_salarial"]
            ),
            "{{CANONICAL_URL}}": f"{BASE_URL}/{montant}-euros-brut-en-net/",
            "{{DESCRIPTION_CONTEXTUELLE}}": build_description_brut_net(montant, nc, c),
            "{{LIENS_PROCHES}}": build_liens_proches(montant, "brut-en-net"),
            "{{LIENS_POPULAIRES}}": build_liens_populaires("brut-en-net"),
            "{{BRUT_MENSUEL_ANNUEL_FORMATE}}": fmt(brut_mensuel_annuel),
            "{{NET_MENSUEL_ANNUEL_NC_FORMATE}}": fmt(result_mensuel_annuel["net_avant_impot"]),
            "{{DONUT_NET_PCT}}": str(round(nc["net_avant_impot"] / montant * 100)),
            "{{DONUT_COTIS_PCT}}": str(round(nc["total_salarial"] / montant * 100)),
            "{{DONUT_COTIS_OFFSET}}": str(25 - round(nc["net_avant_impot"] / montant * 100)),
            "{{DONUT_NET_PCT_INT}}": str(round(nc["net_avant_impot"] / montant * 100)),
            "{{DONUT_COTIS_PCT_INT}}": str(round(nc["total_salarial"] / montant * 100)),
        }

        html = template
        for key, value in replacements.items():
            html = html.replace(key, value)

        folder = os.path.join(BASE_DIR, f"{montant}-euros-brut-en-net")
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  ✓ {montant}-euros-brut-en-net/index.html")


def generate_net_brut_pages(template):
    """Generate all net→brut pages (X00 steps only)."""
    montants = get_main_montants()
    for montant in montants:
        nc = calculer_net_vers_brut(montant, "non-cadre")
        c = calculer_net_vers_brut(montant, "cadre")

        replacements = {
            "{{MONTANT}}": str(montant),
            "{{MONTANT_FORMATE}}": fmt(montant),
            "{{BRUT_NON_CADRE_FORMATE}}": fmt(nc["brut_mensuel"]),
            "{{BRUT_CADRE_FORMATE}}": fmt(c["brut_mensuel"]),
            "{{COTISATIONS_NC_FORMATE}}": fmt(nc["total_salarial"]),
            "{{COTISATIONS_C_FORMATE}}": fmt(c["total_salarial"]),
            "{{BRUT_ANNUEL_NC_FORMATE}}": fmt(nc["brut_annuel"]),
            "{{BRUT_ANNUEL_C_FORMATE}}": fmt(c["brut_annuel"]),
            "{{COUT_EMPLOYEUR_NC_FORMATE}}": fmt(nc["cout_employeur"]),
            "{{COUT_EMPLOYEUR_C_FORMATE}}": fmt(c["cout_employeur"]),
            "{{CANONICAL_URL}}": f"{BASE_URL}/{montant}-euros-net-en-brut/",
            "{{DESCRIPTION_CONTEXTUELLE}}": build_description_net_brut(montant, nc, c),
            "{{LIENS_PROCHES}}": build_liens_proches(montant, "net-en-brut"),
            "{{LIENS_POPULAIRES}}": build_liens_populaires("net-en-brut"),
            "{{DONUT_NET_PCT}}": str(round(montant / nc["brut_mensuel"] * 100)),
            "{{DONUT_COTIS_PCT}}": str(round(nc["total_salarial"] / nc["brut_mensuel"] * 100)),
            "{{DONUT_COTIS_OFFSET}}": str(25 - round(montant / nc["brut_mensuel"] * 100)),
            "{{DONUT_NET_PCT_INT}}": str(round(montant / nc["brut_mensuel"] * 100)),
            "{{DONUT_COTIS_PCT_INT}}": str(round(nc["total_salarial"] / nc["brut_mensuel"] * 100)),
        }

        html = template
        for key, value in replacements.items():
            html = html.replace(key, value)

        folder = os.path.join(BASE_DIR, f"{montant}-euros-net-en-brut")
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  ✓ {montant}-euros-net-en-brut/index.html")


# ── Sitemap ────────────────────────────────────────────────────────────────────

def generate_sitemap():
    """Generate sitemap.xml with X00 URLs only (no X50 redirects)."""
    today = date.today().isoformat()
    montants = get_main_montants()

    urls = [
        {"loc": f"{BASE_URL}/", "priority": "1.0", "changefreq": "monthly"},
        {"loc": f"{BASE_URL}/simulateur-impot-sur-le-revenu/", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{BASE_URL}/mission/", "priority": "0.5", "changefreq": "monthly"},
        {"loc": f"{BASE_URL}/mentions-legales/", "priority": "0.3", "changefreq": "yearly"},
    ]

    for m in montants:
        urls.append({"loc": f"{BASE_URL}/{m}-euros-brut-en-net/", "priority": "0.7", "changefreq": "monthly"})
        urls.append({"loc": f"{BASE_URL}/{m}-euros-net-en-brut/", "priority": "0.7", "changefreq": "monthly"})

    # Pages supplémentaires (Phase 2 + pages spéciales)
    extra_pages = [
        # SMIC et année
        ("smic-brut-net-2026", "0.8"),
        ("salaire-brut-net-2026", "0.8"),
        # Par statut
        ("salaire-brut-net-cadre", "0.8"),
        ("salaire-brut-net-non-cadre", "0.8"),
        ("salaire-brut-net-fonction-publique", "0.7"),
        ("salaire-brut-net-auto-entrepreneur", "0.7"),
        ("salaire-brut-net-alternance-apprentissage", "0.7"),
        ("salaire-brut-net-interim", "0.7"),
        ("salaire-brut-net-stage", "0.7"),
        # Par période
        ("salaire-brut-net-mensuel", "0.7"),
        ("salaire-brut-net-annuel", "0.7"),
        ("salaire-brut-net-horaire", "0.7"),
        ("salaire-brut-net-journalier", "0.7"),
        ("taux-horaire-brut-net", "0.7"),
        # Éducatif
        ("difference-salaire-brut-net", "0.7"),
        ("cotisations-sociales-salariales", "0.7"),
        ("salaire-net-imposable", "0.7"),
        ("salaire-net-avant-apres-impot", "0.7"),
        ("lire-fiche-de-paie", "0.7"),
        ("salaire-moyen-france", "0.7"),
        ("negocier-salaire", "0.7"),
        # Outils
        ("cout-employeur", "0.7"),
        ("calculateur-cout-employeur", "0.7"),
        ("calculateur-heures-supplementaires", "0.7"),
        ("prime-brut-en-net", "0.7"),
        ("13eme-mois-brut-net", "0.7"),
        ("heures-supplementaires-brut-net", "0.7"),
        ("avantages-en-nature", "0.7"),
        ("comparateur-salaire-net-par-pays", "0.6"),
        # Nouvelles pages
        ("cadre-vs-non-cadre", "0.8"),
        ("calculateur-temps-partiel", "0.7"),
        ("simulateur-augmentation", "0.7"),
        ("salaire-brut-net-alsace-moselle", "0.7"),
        # Info pages
        ("a-propos", "0.5"),
        ("glossaire", "0.6"),
    ]
    for slug, prio in extra_pages:
        urls.append({"loc": f"{BASE_URL}/{slug}/", "priority": prio, "changefreq": "monthly"})

    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in urls:
        xml_parts.append(f"""    <url>
        <loc>{url['loc']}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>{url['changefreq']}</changefreq>
        <priority>{url['priority']}</priority>
    </url>""")
    xml_parts.append("</urlset>")

    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_parts))

    print(f"  ✓ sitemap.xml ({len(urls)} URLs)")


# ── Redirect pages for X50 ────────────────────────────────────────────────────

REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Redirection — {montant_fmt} € {direction_label}</title>
<link rel="canonical" href="{BASE_URL}/{target}-euros-{direction}/">
<meta http-equiv="refresh" content="0; url=/{target}-euros-{direction}/">
<meta name="robots" content="noindex, follow">
</head>
<body>
<p>Cette page a été déplacée vers <a href="/{target}-euros-{direction}/">{target_fmt} € {direction_label}</a>.</p>
</body>
</html>"""


def generate_redirect_pages():
    """Generate noindex redirect pages for X50 montants → nearest X00."""
    montants_x50 = get_redirect_montants()
    count = 0
    for montant in montants_x50:
        target = ((montant + 50) // 100) * 100  # Round up to nearest X00
        for direction in ["brut-en-net", "net-en-brut"]:
            direction_label = direction.replace("-", " ")
            html = REDIRECT_TEMPLATE.format(
                montant_fmt=fmt(montant),
                direction_label=direction_label,
                BASE_URL=BASE_URL,
                target=target,
                direction=direction,
                target_fmt=fmt(target),
            )
            folder = os.path.join(BASE_DIR, f"{montant}-euros-{direction}")
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
    print(f"  ✓ {count} redirect pages (X50 → X00)")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=== Génération des pages programmatiques ===\n")

    # Read templates
    with open(os.path.join(BASE_DIR, "template-brut-net.html"), "r", encoding="utf-8") as f:
        template_brut_net = f.read()
    with open(os.path.join(BASE_DIR, "template-net-brut.html"), "r", encoding="utf-8") as f:
        template_net_brut = f.read()

    print("Génération pages brut→net (X00)...")
    generate_brut_net_pages(template_brut_net)

    print("\nGénération pages net→brut (X00)...")
    generate_net_brut_pages(template_net_brut)

    print("\nGénération redirects X50...")
    generate_redirect_pages()

    print("\nGénération sitemap.xml...")
    generate_sitemap()

    main_count = len(get_main_montants()) * 2
    redirect_count = len(get_redirect_montants()) * 2
    print(f"\n=== Terminé ! ===")
    print(f"{main_count} pages principales + {redirect_count} redirects + sitemap.xml")


if __name__ == "__main__":
    main()
