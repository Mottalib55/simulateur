#!/usr/bin/env python3
"""
Module partagé de calcul salaire brut ↔ net.
Utilisé par generate.py et generate-pages.py.
"""

PSS_MENSUEL = 3864
SMIC_MENSUEL_BRUT = 1801.80


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
    impôt = 0
    prev = 0
    for limit, taux in tranches:
        if net_imposable_annuel <= prev:
            break
        base = min(net_imposable_annuel, limit) - prev
        impôt += base * taux
        prev = limit
    return round(impôt)


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


def fmt(val):
    """Format number French style: 1 500"""
    return f"{round(val):,}".replace(",", " ").replace(".", ",")


def fmt2(val):
    """Format number with 2 decimals French style"""
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")
