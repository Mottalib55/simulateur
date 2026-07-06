#!/usr/bin/env python3
"""
Module de generation de contenu contextuel unique pour les pages salaire.

Genere ~900-1000 mots de contenu unique par page en fonction du montant
et de la direction (brut-en-net / net-en-brut).

7 tranches salariales x 5 variantes de structure x 2 directions = 70 blocs.
La variante est sélectionnée par hash déterministe du montant.
"""


# ── Hash déterministe ─────────────────────────────────────────────────────────

def _djb2_hash(s):
    """Hash DJB2 déterministe pour sélectionner la variante."""
    h = 5381
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF
    return h


def select_variant(montant):
    """Retourne un index de variante 0-4 déterministe pour le montant."""
    # Use a combination of hash and arithmetic to reduce adjacent collisions
    h = _djb2_hash(f"salt_{montant}_brutonet")
    # Mix in the montant directly to ensure adjacent values differ
    h = (h ^ (montant * 2654435761)) & 0xFFFFFFFF
    return h % 5


def _phrase_variant(montant, key, options):
    """Select a phrase deterministically among options based on montant and key."""
    h = _djb2_hash(f"v_{montant}_{key}")
    # Mix with Fibonacci hashing to reduce correlations between keys
    h = (h ^ (montant * 2654435761) ^ (_djb2_hash(key) * 1103515245)) & 0xFFFFFFFF
    return options[h % len(options)]


# ── Classification en tranches ────────────────────────────────────────────────

def _get_tranche(montant):
    """Détermine la tranche salariale pour un montant brut mensuel."""
    if montant <= 1400:
        return "smic"
    elif montant <= 1900:
        return "modeste"
    elif montant <= 2600:
        return "médian"
    elif montant <= 3500:
        return "confortable"
    elif montant <= 5000:
        return "cadre_sup"
    elif montant <= 7000:
        return "haut_revenu"
    else:
        return "tres_haut"


def _get_tranche_label(tranche):
    """Retourne le label humain de la tranche."""
    labels = {
        "smic": "proche du SMIC",
        "modeste": "modeste",
        "médian": "autour de la médiane",
        "confortable": "confortable",
        "cadre_sup": "cadre supérieur",
        "haut_revenu": "haut revenu",
        "tres_haut": "très haut revenu",
    }
    return labels.get(tranche, "")


# ── Données de référence par tranche ──────────────────────────────────────────

_TRANCHE_DATA = {
    "smic": {
        "percentile": "les 20 % les plus bas",
        "vs_median": "nettement inférieur au salaire médian français (2 524 euros brut mensuel en 2024 selon l'INSEE)",
        "métiers": [
            "employé de commerce ou de grande distribution",
            "agent d'entretien ou de nettoyage",
            "aide à domicile ou auxiliaire de vie",
            "serveur en restauration ou équipier en restauration rapide",
            "préparateur de commandes en logistique",
            "caissier ou hôte d'accueil",
            "ouvrier non qualifié dans l'industrie",
        ],
        "secteurs": "commerce, restauration, services à la personne, logistique, agriculture",
        "expérience": "débutant ou peu qualifié, souvent en CDD ou temps partiel",
        "loyer_pct": 35,
        "alim_pct": 20,
        "transport_pct": 12,
        "epargne_pct": 3,
        "loisirs_pct": 5,
        "charges_pct": 25,
        "aides": [
            "la prime d'activité (jusqu'à 595 euros par mois pour une personne seule)",
            "les aides au logement APL (jusqu'à 300 euros selon la zone)",
            "la réduction Fillon qui diminue les cotisations patronales de votre employeur",
            "le cheque énergie pour réduire votre facture énergétique (jusqu'à 277 euros par an)",
            "la complémentaire santé solidaire (CSS) pour une mutuelle gratuite ou à 1 euro par jour",
        ],
        "évolution": "viser une qualification (CAP, BEP, titre professionnel) pour accéder à des postes mieux rémunérés, envisager la VAE (Validation des Acquis de l'Expérience)",
        "tranche_suivante": "modeste (1 500 à 1 900 euros brut)",
    },
    "modeste": {
        "percentile": "les 30 % inférieurs",
        "vs_median": "légèrement inférieur au salaire médian français",
        "métiers": [
            "secretaire ou assistant administratif",
            "vendeur qualifié en boutique spécialisée",
            "aide-soignant en debut de carrière",
            "technicien de maintenance de premier niveau",
            "conducteur livreur",
            "ouvrier qualifié dans le bâtiment ou l'industrie",
            "agent de sécurité qualifié",
        ],
        "secteurs": "administration, santé, BTP, industrie, commerce spécialisé",
        "expérience": "2 à 5 ans d'expérience ou diplôme de niveau CAP/BEP/Bac",
        "loyer_pct": 33,
        "alim_pct": 18,
        "transport_pct": 10,
        "epargne_pct": 5,
        "loisirs_pct": 7,
        "charges_pct": 27,
        "aides": [
            "la prime d'activité (montant réduit mais toujours accessible pour un célibataire)",
            "l'aide personnalisee au logement (APL) si le loyer est élevé par rapport aux revenus",
            "la participation et l'intéressement si votre entreprise en propose",
            "les titres-restaurant (jusqu'à 7,18 euros par jour exonérés en 2026)",
            "le remboursement transport à 75 % obligatoire par l'employeur",
        ],
        "évolution": "obtenir une certification ou un diplôme supplémentaire, demander une formation via le CPF, négocier une évolution interne",
        "tranche_suivante": "médiane (2 000 à 2 600 euros brut)",
    },
    "médian": {
        "percentile": "autour de la médiane (50e percentile)",
        "vs_median": "au niveau du salaire médian français, ce qui signifie que la moitie des salariés français gagnent moins",
        "métiers": [
            "technicien supérieur ou agent de maîtrise",
            "comptable ou gestionnaire de paie",
            "infirmier diplôme d'État",
            "développeur junior en informatique",
            "chargé de clientèle en banque ou assurance",
            "responsable de rayon en grande distribution",
            "éducateur spécialisé",
        ],
        "secteurs": "santé, informatique, banque-assurance, industrie, fonction publique",
        "expérience": "3 à 8 ans d'expérience ou diplôme Bac+2 à Bac+3",
        "loyer_pct": 30,
        "alim_pct": 16,
        "transport_pct": 8,
        "epargne_pct": 10,
        "loisirs_pct": 8,
        "charges_pct": 28,
        "aides": [
            "l'optimisation du prélèvement à la source via le taux individualisé pour les couples",
            "l'épargne salariale (PEE) avec abondement employeur défiscalisé",
            "les titres-restaurant et la mutuelle d'entreprise obligatoire",
            "les déductions fiscales pour frais réels si vos déplacements professionnels sont importants",
            "le Plan d'Épargne Retraite (PER) pour déduire vos versements du revenu imposable",
        ],
        "évolution": "passer cadre via une promotion interne, obtenir un diplôme Bac+5 en formation continue, changer de secteur vers un domaine plus rémunérateur",
        "tranche_suivante": "confortable (2 700 à 3 500 euros brut)",
    },
    "confortable": {
        "percentile": "les 30 % supérieurs",
        "vs_median": "supérieur au salaire médian français, plaçant le salarié dans la tranche haute des rémunérations",
        "métiers": [
            "cadre en entreprise ou responsable d'équipe",
            "ingénieur confirmé en industrie ou informatique",
            "chef de projet digital ou marketing",
            "pharmacien salarie",
            "professeur agrégé ou certifié avec ancienneté",
            "responsable comptable ou financier",
            "consultant en cabinet de conseil",
        ],
        "secteurs": "industrie, conseil, santé, numérique, finance, éducation nationale",
        "expérience": "5 à 15 ans d'expérience ou diplôme Bac+5 (école d'ingénieur, master, école de commerce)",
        "loyer_pct": 27,
        "alim_pct": 14,
        "transport_pct": 7,
        "epargne_pct": 15,
        "loisirs_pct": 10,
        "charges_pct": 27,
        "aides": [
            "le Plan d'Épargne Retraite (PER) pour déduire jusqu'à 10 % de vos revenus nets imposables",
            "l'investissement locatif Pinel ou Denormandie pour réduire votre impôt sur le revenu",
            "l'épargne salariale (PEE, PERCO) avec abondement employeur jusqu'à 3 fois vos versements",
            "la négociation d'avantages en nature (voiture de fonction, téléphone, ordinateur)",
            "les chèques CESU préfinancés pour les services à la personne (exonérés jusqu'à 2 421 euros par an)",
        ],
        "évolution": "négocier un passage cadre supérieur, développer une expertise rare sur le marché, viser un poste de direction dans une PME ou une ETI",
        "tranche_suivante": "cadre supérieur (3 600 à 5 000 euros brut)",
    },
    "cadre_sup": {
        "percentile": "les 15 % supérieurs",
        "vs_median": "nettement supérieur au salaire médian, situant le salarié parmi les cadres les mieux rémunérés",
        "métiers": [
            "directeur de departement ou de business unit",
            "architecte logiciel ou lead developer senior",
            "médecin salarié en clinique ou en hopital",
            "directeur des ressources humaines",
            "avocat collaborateur confirmé",
            "responsable grands comptes en B2B",
            "directeur commercial régional",
        ],
        "secteurs": "grandes entreprises, ESN, santé, cabinets d'avocats, industrie pharmaceutique, finance",
        "expérience": "10 à 20 ans d'expérience, souvent MBA ou diplôme grande école, management d'équipe",
        "loyer_pct": 25,
        "alim_pct": 12,
        "transport_pct": 5,
        "epargne_pct": 20,
        "loisirs_pct": 12,
        "charges_pct": 26,
        "aides": [
            "le package de rémunération globale incluant bonus, stock-options et actions gratuites",
            "l'assurance-vie multisupport pour diversifier votre épargne avec une fiscalité avantageuse après 8 ans",
            "le PER pour réduire votre TMI (Taux Marginal d'Imposition) qui est probablement à 30 %",
            "la négociation de la part variable (bonus) et des avantages non monétaires",
            "le FCPI ou FIP pour investir dans les PME avec réduction d'impôt de 25 %",
        ],
        "évolution": "viser un poste de direction générale ou de comité exécutif, créer sa propre entreprise, devenir consultant indépendant à forte valeur ajoutée",
        "tranche_suivante": "haut revenu (5 100 à 7 000 euros brut)",
    },
    "haut_revenu": {
        "percentile": "les 5 % supérieurs",
        "vs_median": "plus du double du salaire médian, plaçant le salarié dans la catégorie des hauts revenus en France",
        "métiers": [
            "directeur général adjoint d'une ETI",
            "partner junior en cabinet de conseil ou d'audit",
            "chirurgien salarié ou médecin spécialiste hospitalier",
            "directeur financier (DAF) d'une grande entreprise",
            "expert en cybersécurité ou en intelligence artificielle",
            "directeur de la stratégie ou du développement",
            "trader junior en salle de marché",
        ],
        "secteurs": "finance de marché, conseil en stratégie, technologie, santé spécialisée, luxe, énergie",
        "expérience": "15 à 25 ans d'expérience, expertise pointue ou management de haut niveau, réseau professionnel étendu",
        "loyer_pct": 22,
        "alim_pct": 10,
        "transport_pct": 5,
        "epargne_pct": 25,
        "loisirs_pct": 12,
        "charges_pct": 26,
        "aides": [
            "la defiscalisation immobilière (LMNP, Malraux, monuments historiques) pour des economies substantielles",
            "le Plan d'Épargne Retraite avec déduction au TMI de 41 % pour un levier fiscal maximal",
            "la gestion de patrimoine via une SCI pour optimiser la transmission et les revenus fonciers",
            "les dons aux oeuvres et mecenat avec réduction d'impôt de 66 % à 75 %",
            "le plafonnement des niches fiscales à 10 000 euros par an (hors investissements outre-mer et Sofica)",
        ],
        "évolution": "viser un poste de CEO ou de président, rejoindre un conseil d'administration, développer un portefeuille d'investissements générant des revenus passifs",
        "tranche_suivante": "très haut revenu (7 100 à 10 000 euros brut)",
    },
    "tres_haut": {
        "percentile": "le top 1 % des salaires en France",
        "vs_median": "quatre à cinq fois supérieur au salaire médian, plaçant le salarié dans l'élite des rémunérations françaises",
        "métiers": [
            "président-directeur général (PDG) d'une ETI ou filiale de grand groupe",
            "partner senior dans un cabinet de stratégie (McKinsey, BCG, Bain)",
            "directeur général d'une grande entreprise cotée",
            "médecin chef de service en CHU ou clinique privée",
            "avocat associé dans un cabinet international",
            "directeur d'investissement en private equity",
            "chief technology officer (CTO) d'une scale-up",
        ],
        "secteurs": "direction générale, finance d'entreprise, conseil en stratégie, médecine libérale hospitalière, droit des affaires, capital-investissement",
        "expérience": "20 ans ou plus d'expérience, parcours d'excellence (grandes écoles, MBA), responsabilité P&L significative",
        "loyer_pct": 18,
        "alim_pct": 8,
        "transport_pct": 4,
        "epargne_pct": 35,
        "loisirs_pct": 10,
        "charges_pct": 25,
        "aides": [
            "la création d'une holding patrimoniale pour optimiser la fiscalité des dividendes et plus-values",
            "le mécanisme de l'apport-cession (article 150-0 B ter du CGI) pour reporter l'imposition des plus-values",
            "la gestion de fortune avec une allocation d'actifs diversifiée (immobilier, private equity, assurance-vie luxembourgeoise)",
            "l'expatriation fiscale encadrée vers des pays à convention fiscale favorable (Portugal, Suisse)",
            "le pacte Dutreil pour préparer la transmission d'entreprise avec une exonération de 75 % des droits",
        ],
        "évolution": "siéger dans plusieurs conseils d'administration, développer un patrimoine générant des revenus passifs supérieurs au salaire, transmettre de manière optimisée",
        "tranche_suivante": None,
    },
}


# ── Formattage ────────────────────────────────────────────────────────────────

def _fmt(val):
    """Format un nombre en style français : 1 500."""
    return f"{round(val):,}".replace(",", "\u202f").replace(".", ",")


# ── Sections de contenu ──────────────────────────────────────────────────────

def _section_positionnement(montant, tranche, direction):
    """Section 1 : Ce que représente ce salaire en France."""
    d = _TRANCHE_DATA[tranche]
    label = _get_tranche_label(tranche)

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "pos_bn", [
            f"Avec un salaire brut mensuel de {_fmt(montant)}\u202f\u20ac, votre rémunération se situe dans "
            f"la catégorie \u00ab\u202f{label}\u202f\u00bb en France. ",
            f"Un salaire de {_fmt(montant)}\u202f\u20ac brut par mois vous place dans la catégorie "
            f"\u00ab\u202f{label}\u202f\u00bb sur le marché du travail français. ",
            f"Percevoir {_fmt(montant)}\u202f\u20ac brut chaque mois correspond à la tranche "
            f"\u00ab\u202f{label}\u202f\u00bb des rémunérations en France. ",
            f"À hauteur de {_fmt(montant)}\u202f\u20ac brut mensuel, vous vous inscrivez dans la catégorie "
            f"\u00ab\u202f{label}\u202f\u00bb des salaires français. ",
        ])
    else:
        intro = _phrase_variant(montant, "pos_nb", [
            f"Pour atteindre un salaire net de {_fmt(montant)}\u202f\u20ac par mois, le brut nécessaire vous place "
            f"dans la catégorie \u00ab\u202f{label}\u202f\u00bb du marché français. ",
            f"Viser {_fmt(montant)}\u202f\u20ac net mensuel implique un salaire brut situé dans la tranche "
            f"\u00ab\u202f{label}\u202f\u00bb des rémunérations en France. ",
            f"Un objectif de {_fmt(montant)}\u202f\u20ac net par mois requiert un brut correspondant "
            f"a la catégorie \u00ab\u202f{label}\u202f\u00bb du marché de l'emploi français. ",
            f"Toucher {_fmt(montant)}\u202f\u20ac net mensuellement nécessite un brut qui vous positionne "
            f"dans la catégorie \u00ab\u202f{label}\u202f\u00bb en France. ",
        ])

    body = _phrase_variant(montant, "pos_body", [
        f"Ce niveau de rémunération est {d['vs_median']}. "
        f"Statistiquement, ce montant vous situe parmi {d['percentile']} des salariés du secteur privé en France. ",
        f"Cette rémunération est {d['vs_median']}. "
        f"En termes de distribution salariale, vous vous situez parmi {d['percentile']} des salariés du privé. ",
        f"Ce montant est {d['vs_median']}. "
        f"D'après les statistiques de l'emploi, ce salaire vous positionne parmi {d['percentile']} des salariés du secteur privé. ",
    ])

    if tranche == "smic":
        body += (
            "Le SMIC brut mensuel en 2026 s'élève à 1\u202f801,80\u202f\u20ac pour 35 heures hebdomadaires, "
            "soit 1\u202f426,30\u202f\u20ac net avant impôt. Un salaire dans cette tranche correspond souvent "
            "a un temps partiel ou à un debut de carrière sans qualification spécifique. "
            "Selon les données de la DARES, environ 17 % des salariés du privé sont rémunérés au voisinage du SMIC."
        )
    elif tranche == "modeste":
        body += (
            "Ce salaire représente environ 75 à 90 % du salaire médian. "
            "Selon l'INSEE, près de 30 % des salariés français perçoivent une rémunération dans cette fourchette. "
            "Il correspond fréquemment à des postes qualifiés mais non-cadres, avec une ancienneté de quelques années."
        )
    elif tranche == "médian":
        body += (
            "Vous vous situez dans la norme salariale française. "
            "Le salaire médian signifie que 50 % des salariés gagnent moins et 50 % gagnent plus. "
            "Selon l'INSEE, le salaire brut médian dans le secteur privé s'établit autour de 2\u202f524\u202f\u20ac mensuels en équivalent temps plein. "
            "Ce niveau correspond souvent à un premier poste de cadre ou à un technicien supérieur experimente."
        )
    elif tranche == "confortable":
        body += (
            "Ce salaire dépasse largement la médiane et vous place dans la partie haute de la distribution salariale. "
            "Selon les statistiques de l'INSEE, seulement 30 % des salariés du privé atteignent ce niveau de rémunération. "
            "À ce stade, l'impôt sur le revenu commence à peser significativement, avec un taux marginal d'imposition (TMI) généralement à 30 %."
        )
    elif tranche == "cadre_sup":
        body += (
            "Ce niveau de salaire est caractéristique des cadres supérieurs et des profils hautement qualifiés. "
            "D'après l'APEC, le salaire médian des cadres en France s'établit autour de 52\u202f000\u202f\u20ac brut annuels, "
            "soit environ 4\u202f333\u202f\u20ac brut mensuels. Votre rémunération se situe donc dans la fourchette haute des cadres. "
            "Le plafond de la Sécurité sociale (3\u202f864\u202f\u20ac en 2026) est dépassé, ce qui impacte le calcul de certaines cotisations."
        )
    elif tranche == "haut_revenu":
        body += (
            "À ce niveau, vous faites partie des 5 % de salariés les mieux payés en France. "
            "Votre TMI (Taux Marginal d'Imposition) est probablement de 41 %, ce qui rend chaque euro supplémentaire "
            "fortement imposé. La différence entre brut et net est encore plus marquée à cause du dépassement "
            "du plafond de la Sécurité sociale sur la totalité du salaire. "
            "Les cotisations AGIRC-ARRCO en tranche 2 (au-delà du PSS) représentent un prélèvement supplémentaire significatif."
        )
    else:
        body += (
            "À ce stade, votre rémunération dépasse quatre fois le salaire médian français. "
            "Vous êtes dans le top 1 % des rémunérations salariales du secteur privé. "
            "Votre TMI est très probablement à 41 % voire 45 % pour la fraction dépassant 180\u202f294\u202f\u20ac annuels. "
            "La gestion patrimoniale et l'optimisation fiscale deviennent des enjeux majeurs à ce niveau de revenu."
        )

    # Add fiscal detail paragraph
    if direction == "brut-en-net":
        fiscal = _phrase_variant(montant, "pos_fisc_bn", [
            f"En termes de cotisations, un salaire brut de {_fmt(montant)}\u202f\u20ac génère environ "
            f"{_fmt(round(montant * 0.22))}\u202f\u20ac a {_fmt(round(montant * 0.25))}\u202f\u20ac de prélèvements "
            "salariaux selon que vous êtes non-cadre ou cadre. Ces cotisations financent votre protection sociale\u202f: "
            "retraite de base et complémentaire (AGIRC-ARRCO), assurance maladie, chômage et prévoyance. "
            "La CSG (Contribution Sociale Généralisée) à elle seule représente 9,2 % de 98,25 % du salaire brut, "
            "dont 6,8 % sont déductibles de votre revenu imposable.",
            f"Les cotisations salariales prélevées sur {_fmt(montant)}\u202f\u20ac brut représentent entre "
            f"{_fmt(round(montant * 0.22))}\u202f\u20ac et {_fmt(round(montant * 0.25))}\u202f\u20ac selon votre statut. "
            "Elles couvrent la retraite de base, la complémentaire AGIRC-ARRCO, l'assurance maladie et la prévoyance. "
            "La CSG, prélevée à 9,2 % sur 98,25 % du brut, constitue le poste le plus important, "
            "avec une part déductible de 6,8 % qui réduit votre base imposable.",
            f"Sur un brut mensuel de {_fmt(montant)}\u202f\u20ac, les prélèvements salariaux oscillent entre "
            f"{_fmt(round(montant * 0.22))}\u202f\u20ac (non-cadre) et {_fmt(round(montant * 0.25))}\u202f\u20ac (cadre). "
            "Ces cotisations alimentent votre protection sociale\u202f: retraite, maladie, chômage et prévoyance. "
            "La CSG-CRDS, calculée sur 98,25 % du salaire brut, représente à elle seule près de 10 % du brut.",
        ])
    else:
        fiscal = _phrase_variant(montant, "pos_fisc_nb", [
            f"Pour percevoir {_fmt(montant)}\u202f\u20ac net chaque mois, le salaire brut nécessaire intègre "
            "l'ensemble des cotisations salariales obligatoires\u202f: la part salariale pour la retraite de base "
            "(vieillesse plafonnée à 6,90 % et déplafonnée à 0,40 %), la retraite complémentaire AGIRC-ARRCO "
            "(3,15 % en tranche 1), la CSG-CRDS (9,7 % sur 98,25 % du brut) et la CEG (0,86 % en tranche 1). "
            "Pour un cadre, il faut ajouter la CET de 0,14 %, ce qui explique qu'un brut légèrement supérieur "
            "est nécessaire pour atteindre le même montant net.",
            f"Atteindre {_fmt(montant)}\u202f\u20ac net par mois nécessite un brut integrant toutes les cotisations "
            "obligatoires\u202f: vieillesse plafonnée (6,90 %) et déplafonnée (0,40 %), complémentaire AGIRC-ARRCO "
            "(3,15 % sur la tranche 1), CSG-CRDS (9,7 % sur 98,25 % du brut) et CEG (0,86 %). "
            "Le statut cadre ajoute une CET de 0,14 %, augmentant légèrement le brut requis.",
            f"Le brut nécessaire pour obtenir {_fmt(montant)}\u202f\u20ac net inclut l'ensemble des prélèvements "
            "salariaux\u202f: retraite de base (6,90 % + 0,40 %), AGIRC-ARRCO (3,15 % en T1), "
            "CSG-CRDS (9,7 % sur 98,25 % du brut) et CEG (0,86 % en T1). "
            "Un cadre doit négocier un brut légèrement supérieur en raison de la CET additionnelle de 0,14 %.",
        ])

    h2 = _phrase_variant(montant, "pos_h2", [
        f'Ce que représente un salaire de {_fmt(montant)}\u202f\u20ac en France',
        f'Salaire de {_fmt(montant)}\u202f\u20ac\u202f: positionnement en France',
        f'{_fmt(montant)}\u202f\u20ac par mois\u202f: où se situe ce salaire\u202f?',
    ])

    return (
        f'<h2>{h2}</h2>\n'
        f'<p>{intro}{body}</p>\n<p>{fiscal}</p>'
    )


def _section_metiers(montant, tranche, direction):
    """Section 2 : Métiers et profils types."""
    d = _TRANCHE_DATA[tranche]

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "met_bn", [
            f"Un salaire brut de {_fmt(montant)}\u202f\u20ac par mois est typiquement associé "
            f"a des postes dans les secteurs suivants\u202f: {d['secteurs']}. ",
            f"Avec {_fmt(montant)}\u202f\u20ac brut mensuel, vous exercez probablement dans l'un de ces "
            f"secteurs\u202f: {d['secteurs']}. ",
            f"Les emplois rémunérés {_fmt(montant)}\u202f\u20ac brut par mois se concentrent principalement "
            f"dans\u202f: {d['secteurs']}. ",
        ])
    else:
        intro = _phrase_variant(montant, "met_nb", [
            f"Pour négocier un salaire net de {_fmt(montant)}\u202f\u20ac par mois, vous visez "
            f"des postes que l'on retrouve principalement dans\u202f: {d['secteurs']}. ",
            f"Atteindre {_fmt(montant)}\u202f\u20ac net mensuel passe par des postes concentres "
            f"dans les secteurs suivants\u202f: {d['secteurs']}. ",
            f"Un salaire net de {_fmt(montant)}\u202f\u20ac par mois est accessible dans ces "
            f"domaines d'activité\u202f: {d['secteurs']}. ",
        ])

    metiers_list = ", ".join(d["métiers"][:5])
    metiers_extra = ", ".join(d["métiers"][5:])

    body = (
        f"Les métiers les plus courants à ce niveau incluent\u202f: {metiers_list}. "
    )
    if metiers_extra:
        body += f"On retrouve également des profils de {metiers_extra}. "

    body += (
        f"Le profil type correspond à un salarié avec {d['expérience']}. "
    )

    if direction == "brut-en-net":
        body += (
            "Lorsque vous recevez une offre d'emploi affichant ce montant en brut, "
            "il est essentiel de comprendre combien vous percevrez réellement sur votre compte bancaire. "
            "Les cotisations salariales, qui représentent environ 22 à 25 % du brut selon votre statut, "
            "constituent la principale différence entre le salaire brut annoncé et le net perçu."
        )
    else:
        body += (
            "Lors d'une négociation salariale, connaître le brut correspondant à votre objectif net "
            "vous donne un avantage stratégique. Vous pouvez ainsi formuler votre demande en brut, "
            "qui est la référence pour les recruteurs, tout en sachant exactement ce que vous toucherez. "
            "N'oubliez pas que le brut nécessaire pour un même net est légèrement plus élevé pour un cadre "
            "en raison de la cotisation CET supplémentaire de 0,14 %."
        )

    # Add régional salary variation paragraph
    if tranche in ("smic", "modeste"):
        régional = (
            "À noter que les écarts de rémunération varient considérablement selon les régions. "
            "En Ile-de-France, les salaires sont en moyenne 20 % plus élevés que dans le reste de la France "
            "pour des postes équivalents, mais le coût de la vie — notamment le logement — "
            "absorbe souvent cette différence. Les régions comme PACA, Auvergne-Rhone-Alpes et Occitanie "
            "offrent un compromis intéressant entre niveau de salaire et qualité de vie."
        )
    elif tranche in ("médian", "confortable"):
        régional = (
            "Les disparités régionales sont significatives à ce niveau de salaire. "
            "Un même poste peut être rémunéré 15 à 25 % de plus en région parisienne qu'en province, "
            "mais le différentiel de coût de la vie réduit cet avantage. Des métropoles comme Lyon, Nantes, "
            "Bordeaux ou Toulouse attirent de plus en plus d'entreprises et proposent des salaires compétitifs "
            "avec une meilleure qualité de vie. Le télétravail généralisé depuis 2020 a aussi modifié "
            "la donne en permettant d'accéder à des salaires parisiens depuis la province."
        )
    else:
        régional = (
            "À ce niveau de rémunération, les postes sont concentres dans les grandes métropoles "
            "et les sieges sociaux des grands groupes. Paris et sa région concentrent plus de 40 % "
            "des emplois cadres supérieurs en France. Cependant, des poles d'excellence existent "
            "en province\u202f: la finance à Lyon, l'aéronautique à Toulouse, le numérique à Sophia Antipolis, "
            "l'industrie pharmaceutique à Strasbourg. L'implantation croissante de bureaux décentralisés "
            "et le travail hybride offrent de nouvelles opportunités géographiques à ces niveaux de salaire."
        )

    h2 = _phrase_variant(montant, "met_h2", [
        f'Métiers et profils types pour {_fmt(montant)}\u202f\u20ac',
        f'Quels métiers pour {_fmt(montant)}\u202f\u20ac brut par mois\u202f?',
        f'Profils et secteurs associés à {_fmt(montant)}\u202f\u20ac',
    ])

    return (
        f'<h2>{h2}</h2>\n'
        f'<p>{intro}{body}</p>\n<p>{régional}</p>'
    )


def _section_budget(montant, tranche, direction):
    """Section 3 : Budget mensuel type."""
    d = _TRANCHE_DATA[tranche]

    # Estimer le net approximatif
    if direction == "brut-en-net":
        net_approx = round(montant * 0.78)
        intro_budget = f"Avec environ {_fmt(net_approx)}\u202f\u20ac net par mois (estimation non-cadre avant impôt)"
    else:
        net_approx = montant
        intro_budget = f"Avec {_fmt(net_approx)}\u202f\u20ac net par mois"

    loyer = round(net_approx * d["loyer_pct"] / 100)
    alim = round(net_approx * d["alim_pct"] / 100)
    transport = round(net_approx * d["transport_pct"] / 100)
    épargne = round(net_approx * d["epargne_pct"] / 100)
    loisirs = round(net_approx * d["loisirs_pct"] / 100)
    charges = round(net_approx * d["charges_pct"] / 100)

    body = _phrase_variant(montant, "bud_body", [
        f"{intro_budget}, voici une répartition budgétaire type adaptée à ce niveau de revenus. "
        f"Le logement représente le poste le plus important avec environ {d['loyer_pct']}\u202f% du budget, "
        f"soit {_fmt(loyer)}\u202f\u20ac par mois. Ce montant correspond ",
        f"{intro_budget}, la répartition de vos dépenses suit un schéma classique pour cette tranche. "
        f"Le poste logement absorbe environ {d['loyer_pct']}\u202f% de vos revenus, "
        f"soit {_fmt(loyer)}\u202f\u20ac mensuels. Ce budget logement correspond ",
        f"{intro_budget}, voici comment se répartit un budget type à ce niveau de salaire. "
        f"Le logement, premier poste de dépense, représente {d['loyer_pct']}\u202f% du revenu net, "
        f"soit environ {_fmt(loyer)}\u202f\u20ac par mois. Cette enveloppe correspond ",
    ])

    if tranche in ("smic", "modeste"):
        body += (
            "a un studio ou un T2 en province, ou à une chambre en région parisienne. "
            "La règle des 33 % de taux d'effort est difficile à respecter dans les grandes métropoles à ce niveau de salaire."
        )
    elif tranche in ("médian", "confortable"):
        body += (
            "a un T2 ou T3 en province, ou à un studio/T2 en petite couronne parisienne. "
            "Ce budget permet de vivre correctement en adaptant le lieu de résidence au coût de la vie local."
        )
    else:
        body += (
            "a un logement confortable dans la plupart des grandes villes françaises, "
            "y compris un appartement décent en région parisienne."
        )

    body += (
        f" L'alimentation représente environ {d['alim_pct']}\u202f% ({_fmt(alim)}\u202f\u20ac), "
        f"le transport {d['transport_pct']}\u202f% ({_fmt(transport)}\u202f\u20ac), "
        f"les loisirs et sorties {d['loisirs_pct']}\u202f% ({_fmt(loisirs)}\u202f\u20ac), "
        f"et les charges courantes (énergie, téléphone, internet, assurances) {d['charges_pct']}\u202f% ({_fmt(charges)}\u202f\u20ac). "
        f"La capacité d'épargne estimée est de {d['epargne_pct']}\u202f% du revenu net, soit environ {_fmt(épargne)}\u202f\u20ac par mois"
    )

    if tranche in ("smic", "modeste"):
        body += (
            ". Cette épargne reste fragile et il est recommandé de constituer en priorité un fonds d'urgence "
            "de 3 mois de dépenses sur un Livret A (taux de 2,4 % en 2026, plafond de 22\u202f950\u202f\u20ac). "
            "Le Livret d'Épargne Populaire (LEP), reserve aux revenus modestes, offre un taux plus avantageux de 3,5 %."
        )
    elif tranche in ("médian", "confortable"):
        body += (
            ". Cette capacité d'épargne permet de constituer un apport immobilier ou de préparer des projets "
            "a moyen terme. Répartissez entre Livret A pour l'épargne de précaution, "
            "PEA (Plan d'Épargne en Actions) pour l'investissement long terme, "
            "et éventuellement une assurance-vie en fonds euros et unités de compte."
        )
    else:
        body += (
            ". À ce niveau d'épargne, une stratégie patrimoniale diversifiée s'impose\u202f: "
            "assurance-vie multisupport, PEA, investissement immobilier (direct ou via SCPI), "
            "et potentiellement private equity ou fonds structurés. "
            "Un conseil en gestion de patrimoine peut s'avérer rentable pour optimiser l'allocation de vos actifs."
        )

    h2 = _phrase_variant(montant, "bud_h2", [
        f'Budget mensuel type avec {_fmt(montant)}\u202f\u20ac',
        f'Comment gerer un budget de {_fmt(net_approx)}\u202f\u20ac net par mois',
        f'Répartition budgétaire pour {_fmt(montant)}\u202f\u20ac',
    ])

    return f'<h2>{h2}</h2>\n<p>{body}</p>'


def _section_optimisation(montant, tranche, direction):
    """Section 4 : Conseils d'optimisation."""
    d = _TRANCHE_DATA[tranche]

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "opt_bn", [
            f"Avec un salaire brut de {_fmt(montant)}\u202f\u20ac, plusieurs leviers permettent "
            "d'optimiser votre rémunération nette et votre fiscalité. ",
            f"A {_fmt(montant)}\u202f\u20ac brut mensuel, des dispositifs existent pour augmenter "
            "votre pouvoir d'achat réel sans changer de poste. ",
            f"Pour un salaire brut de {_fmt(montant)}\u202f\u20ac, voici les stratégies "
            "d'optimisation fiscale et sociale les plus pertinentes. ",
        ])
    else:
        intro = _phrase_variant(montant, "opt_nb", [
            f"En ciblant un net de {_fmt(montant)}\u202f\u20ac par mois, il est utile de connaître "
            "les dispositifs qui peuvent améliorer votre pouvoir d'achat réel au-delà du simple salaire. ",
            f"Avec un objectif de {_fmt(montant)}\u202f\u20ac net mensuel, plusieurs leviers permettent "
            "d'accroître votre revenu disponible effectif. ",
            f"Si vous visez {_fmt(montant)}\u202f\u20ac net par mois, des mécanismes fiscaux et sociaux "
            "peuvent renforcer significativement votre pouvoir d'achat. ",
        ])

    conseils = d["aides"]
    body = "Voici les principaux dispositifs et conseils adaptés à votre tranche de revenus\u202f: "

    for i, conseil in enumerate(conseils):
        body += f"{conseil}"
        if i < len(conseils) - 1:
            body += "\u202f; "
        else:
            body += ". "

    if tranche in ("smic", "modeste"):
        body += (
            "Pensez également à vérifier votre éligibilité sur le site mesdroitssociaux.gouv.fr qui centralise "
            "toutes les aides disponibles. Selon une étude de la DREES, près de 30 % des bénéficiaires potentiels "
            "ne réclament pas les aides auxquelles ils ont droit, soit un manque à gagner de plusieurs centaines "
            "d'euros par mois."
        )
    elif tranche in ("médian", "confortable"):
        body += (
            "Pensez aussi à optimiser votre déclaration d'impôts\u202f: le choix entre déduction forfaitaire "
            "de 10 % et frais réels peut faire une différence significative si vous avez des frais "
            "de déplacement importants. La déduction des frais réels est avantageuse dès que vos frais "
            "professionnels dépassent 10 % de votre salaire net imposable."
        )
    else:
        body += (
            "À ce niveau de revenus, une stratégie fiscale et patrimoniale structurée est indispensable. "
            "Le plafonnement global des niches fiscales à 10\u202f000\u202f\u20ac par an limite les possibilités "
            "de réduction d'impôt, mais certains dispositifs (investissement outre-mer, Sofica) bénéficient "
            "d'un plafond supplémentaire de 18\u202f000\u202f\u20ac. "
            "Consultez un conseiller en gestion de patrimoine agréé (CGP ou CGPI) pour une stratégie sur mesure."
        )

    h2 = _phrase_variant(montant, "opt_h2", [
        f"Conseils d'optimisation pour {_fmt(montant)}\u202f\u20ac",
        f"Comment optimiser un salaire de {_fmt(montant)}\u202f\u20ac",
        f"Maximiser son pouvoir d'achat avec {_fmt(montant)}\u202f\u20ac",
    ])

    return f'<h2>{h2}</h2>\n<p>{intro}{body}</p>'


def _section_evolution(montant, tranche, direction):
    """Section 5 : Perspectives d'évolution."""
    d = _TRANCHE_DATA[tranche]

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "evo_bn", [
            f"Si vous percevez actuellement {_fmt(montant)}\u202f\u20ac brut par mois, "
            "voici comment envisager une progression salariale. ",
            f"Avec {_fmt(montant)}\u202f\u20ac brut mensuel, des perspectives d'évolution existent "
            "pour faire progresser votre rémunération. ",
            f"A {_fmt(montant)}\u202f\u20ac brut par mois, comment accélérer "
            "votre progression salariale\u202f? Voici les pistes concrètes. ",
        ])
    else:
        intro = _phrase_variant(montant, "evo_nb", [
            f"Si votre objectif est d'atteindre {_fmt(montant)}\u202f\u20ac net par mois, "
            "voici les pistes pour y parvenir ou pour progresser au-delà. ",
            f"Viser {_fmt(montant)}\u202f\u20ac net mensuel est un objectif atteignable "
            "avec les bonnes stratégies d'évolution professionnelle. ",
            f"Pour atteindre ou dépasser {_fmt(montant)}\u202f\u20ac net par mois, "
            "plusieurs leviers de progression s'offrent à vous. ",
        ])

    body = f"Pour évoluer, la stratégie recommandée est de {d['évolution']}. "

    if d["tranche_suivante"]:
        body += (
            f"La tranche salariale suivante est la tranche {d['tranche_suivante']}. "
            "Pour y accéder, plusieurs leviers sont à votre disposition\u202f: "
        )
    else:
        body += (
            "À ce niveau de rémunération, l'évolution passe moins par le salaire fixe que par "
            "la construction d'un patrimoine productif et l'accès à des formes de rémunération alternatives. "
        )

    if tranche == "smic":
        body += (
            "la formation professionnelle via le CPF (Compte Personnel de Formation, jusqu'à 500\u202f\u20ac par an "
            "credites automatiquement) est un levier puissant. Les secteurs en tension comme le numérique, "
            "la santé ou le BTP offrent des perspectives d'augmentation rapide après une reconversion. "
            "En moyenne, un changement d'employeur permet une augmentation de 10 à 15 % contre 2 à 4 % "
            "pour une augmentation annuelle en interne."
        )
    elif tranche == "modeste":
        body += (
            "la montée en compétences est clé. Les certifications professionnelles (titre RNCP, CQP) "
            "permettent souvent un bond salarial de 15 à 20 %. Le passage au statut cadre, accessible "
            "via une promotion interne ou un changement d'entreprise, ouvre l'accès à des grilles salariales "
            "supérieures et à des avantages complémentaires (mutuelle renforcée, prévoyance cadre, retraite supplémentaire)."
        )
    elif tranche == "médian":
        body += (
            "a ce stade, l'enjeu est de développer une expertise distinctive ou de prendre des responsabilités "
            "managériales. Un MBA en formation continue ou un mastere spécialisé peut accélérer la progression. "
            "La mobilité géographique vers des bassins d'emploi dynamiques (Ile-de-France, Lyon, Toulouse) "
            "ou la mobilité sectorielle vers des industries plus rémunératrices (tech, finance, pharma) "
            "sont des stratégies efficaces."
        )
    elif tranche == "confortable":
        body += (
            "les augmentations significatives passent souvent par la mobilité externe ou l'accès à des postes "
            "de direction. La négociation du package global (fixe + variable + avantages) devient aussi "
            "importante que le salaire fixe seul. Les stock-options et actions gratuites, exonérées de cotisations "
            "salariales sous certaines conditions, peuvent représenter un complément de rémunération significatif."
        )
    elif tranche == "cadre_sup":
        body += (
            "a ce niveau, la progression passe par le réseau professionnel, la visibilité dans votre secteur "
            "et l'accès à des postes de gouvernance. Les chasseurs de têtes deviennent vos principaux interlocuteurs. "
            "La rémunération se négocie en package global\u202f: fixe + bonus (20 à 50 % du fixe) + LTI (Long Term Incentives) "
            "+ avantages (voiture, logement, retraite chapeau). Un bilan de compétences ou un coaching de dirigeant "
            "peut aider à structurer votre parcours vers le top management."
        )
    elif tranche == "haut_revenu":
        body += (
            "la progression vers la tranche supérieure repose sur l'accès à des postes de direction générale "
            "ou à des roles d'associé dans les cabinets de conseil et d'audit. Le mandat social (président, DG) "
            "offre une rémunération différente du salariat avec des possibilités d'optimisation spécifiques. "
            "La création ou la reprise d'entreprise est aussi une voie pour dépasser le plafond salarial "
            "et accéder à la création de valeur patrimoniale."
        )
    else:
        body += (
            "les revenus du travail atteignent un plateau naturel. La croissance de votre patrimoine global "
            "passé désormais par les revenus du capital\u202f: dividendes, plus-values, revenus fonciers, "
            "intérêts. La structuration via une holding permet de réinvestir les bénéfices avec une fiscalité "
            "allégée (régime mère-fille, intégration fiscale). L'entrepreneuriat et l'investissement en private equity "
            "sont les voies privilégiées pour une création de valeur exponentielle."
        )

    h2 = _phrase_variant(montant, "evo_h2", [
        f"Perspectives d'évolution salariale depuis {_fmt(montant)}\u202f\u20ac",
        f"Comment évoluer au-delà de {_fmt(montant)}\u202f\u20ac",
        f"Progresser depuis un salaire de {_fmt(montant)}\u202f\u20ac",
    ])

    return f'<h2>{h2}</h2>\n<p>{intro}{body}</p>'


# ── Variantes de structure ────────────────────────────────────────────────────

def _build_variant_0(montant, tranche, direction):
    """Variante 0 : budget > métiers > optimisation > positionnement > évolution."""
    sections = [
        _section_budget(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_1(montant, tranche, direction):
    """Variante 1 : métiers > positionnement > budget > évolution > optimisation."""
    sections = [
        _section_metiers(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_2(montant, tranche, direction):
    """Variante 2 : positionnement > budget > évolution > métiers > optimisation."""
    sections = [
        _section_positionnement(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_3(montant, tranche, direction):
    """Variante 3 : optimisation > positionnement > métiers > budget > évolution."""
    sections = [
        _section_optimisation(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_4(montant, tranche, direction):
    """Variante 4 : évolution > optimisation > positionnement > budget > métiers."""
    sections = [
        _section_evolution(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
    ]
    return "\n".join(sections)


_VARIANT_BUILDERS = [
    _build_variant_0,
    _build_variant_1,
    _build_variant_2,
    _build_variant_3,
    _build_variant_4,
]


# ── API publique ──────────────────────────────────────────────────────────────

def generate_contextual_content(montant, direction):
    """
    Genere le contenu HTML contextuel unique pour une page salaire.

    Args:
        montant: int, le montant en euros (ex: 2500)
        direction: str, "brut-en-net" ou "net-en-brut"

    Returns:
        str: contenu HTML (5 sections h2) à injecter dans {{DESCRIPTION_CONTEXTUELLE}}
    """
    tranche = _get_tranche(montant)
    variant_idx = select_variant(montant)
    builder = _VARIANT_BUILDERS[variant_idx]
    return builder(montant, tranche, direction)


# ── Test standalone ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    test_montants = [1000, 1200, 1500, 1800, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 8000, 10000]

    for m in test_montants:
        for d in ["brut-en-net", "net-en-brut"]:
            content = generate_contextual_content(m, d)
            # Count words roughly
            word_count = len(content.split())
            tranche = _get_tranche(m)
            variant = select_variant(m)
            print(f"{m}e {d}: {word_count} mots, tranche={tranche}, variante={variant}")

    # Check that adjacent amounts get différent variants
    print("\n--- Verification des variantes adjacentes ---")
    prev_variant = None
    consecutive_same = 0
    for m in range(1000, 10100, 100):
        v = select_variant(m)
        t = _get_tranche(m)
        if v == prev_variant:
            consecutive_same += 1
        else:
            consecutive_same = 0
        if consecutive_same >= 2:
            print(f"  ATTENTION: {m-200}, {m-100}, {m} ont tous la variante {v}")
        prev_variant = v

    print("\nDone.")
