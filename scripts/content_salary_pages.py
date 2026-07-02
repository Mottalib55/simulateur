#!/usr/bin/env python3
"""
Module de generation de contenu contextuel unique pour les pages salaire.

Genere ~900-1000 mots de contenu unique par page en fonction du montant
et de la direction (brut-en-net / net-en-brut).

7 tranches salariales x 5 variantes de structure x 2 directions = 70 blocs.
La variante est selectionnee par hash deterministe du montant.
"""


# ── Hash deterministe ─────────────────────────────────────────────────────────

def _djb2_hash(s):
    """Hash DJB2 deterministe pour selectionner la variante."""
    h = 5381
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF
    return h


def select_variant(montant):
    """Retourne un index de variante 0-4 deterministe pour le montant."""
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
    """Determine la tranche salariale pour un montant brut mensuel."""
    if montant <= 1400:
        return "smic"
    elif montant <= 1900:
        return "modeste"
    elif montant <= 2600:
        return "median"
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
        "median": "autour de la mediane",
        "confortable": "confortable",
        "cadre_sup": "cadre superieur",
        "haut_revenu": "haut revenu",
        "tres_haut": "tres haut revenu",
    }
    return labels.get(tranche, "")


# ── Donnees de reference par tranche ──────────────────────────────────────────

_TRANCHE_DATA = {
    "smic": {
        "percentile": "les 20 % les plus bas",
        "vs_median": "nettement inferieur au salaire median francais (2 524 euros brut mensuel en 2024 selon l'INSEE)",
        "metiers": [
            "employe de commerce ou de grande distribution",
            "agent d'entretien ou de nettoyage",
            "aide a domicile ou auxiliaire de vie",
            "serveur en restauration ou equipier en restauration rapide",
            "preparateur de commandes en logistique",
            "caissier ou hote d'accueil",
            "ouvrier non qualifie dans l'industrie",
        ],
        "secteurs": "commerce, restauration, services a la personne, logistique, agriculture",
        "experience": "debutant ou peu qualifie, souvent en CDD ou temps partiel",
        "loyer_pct": 35,
        "alim_pct": 20,
        "transport_pct": 12,
        "epargne_pct": 3,
        "loisirs_pct": 5,
        "charges_pct": 25,
        "aides": [
            "la prime d'activite (jusqu'a 595 euros par mois pour une personne seule)",
            "les aides au logement APL (jusqu'a 300 euros selon la zone)",
            "la reduction Fillon qui diminue les cotisations patronales de votre employeur",
            "le cheque energie pour reduire votre facture energetique (jusqu'a 277 euros par an)",
            "la complementaire sante solidaire (CSS) pour une mutuelle gratuite ou a 1 euro par jour",
        ],
        "evolution": "viser une qualification (CAP, BEP, titre professionnel) pour acceder a des postes mieux remuneres, envisager la VAE (Validation des Acquis de l'Experience)",
        "tranche_suivante": "modeste (1 500 a 1 900 euros brut)",
    },
    "modeste": {
        "percentile": "les 30 % inferieurs",
        "vs_median": "legerement inferieur au salaire median francais",
        "metiers": [
            "secretaire ou assistant administratif",
            "vendeur qualifie en boutique specialisee",
            "aide-soignant en debut de carriere",
            "technicien de maintenance de premier niveau",
            "conducteur livreur",
            "ouvrier qualifie dans le batiment ou l'industrie",
            "agent de securite qualifie",
        ],
        "secteurs": "administration, sante, BTP, industrie, commerce specialise",
        "experience": "2 a 5 ans d'experience ou diplome de niveau CAP/BEP/Bac",
        "loyer_pct": 33,
        "alim_pct": 18,
        "transport_pct": 10,
        "epargne_pct": 5,
        "loisirs_pct": 7,
        "charges_pct": 27,
        "aides": [
            "la prime d'activite (montant reduit mais toujours accessible pour un celibataire)",
            "l'aide personnalisee au logement (APL) si le loyer est eleve par rapport aux revenus",
            "la participation et l'interessement si votre entreprise en propose",
            "les titres-restaurant (jusqu'a 7,18 euros par jour exoneres en 2026)",
            "le remboursement transport a 75 % obligatoire par l'employeur",
        ],
        "evolution": "obtenir une certification ou un diplome supplementaire, demander une formation via le CPF, negocier une evolution interne",
        "tranche_suivante": "mediane (2 000 a 2 600 euros brut)",
    },
    "median": {
        "percentile": "autour de la mediane (50e percentile)",
        "vs_median": "au niveau du salaire median francais, ce qui signifie que la moitie des salaries francais gagnent moins",
        "metiers": [
            "technicien superieur ou agent de maitrise",
            "comptable ou gestionnaire de paie",
            "infirmier diplome d'Etat",
            "developpeur junior en informatique",
            "charge de clientele en banque ou assurance",
            "responsable de rayon en grande distribution",
            "educateur specialise",
        ],
        "secteurs": "sante, informatique, banque-assurance, industrie, fonction publique",
        "experience": "3 a 8 ans d'experience ou diplome Bac+2 a Bac+3",
        "loyer_pct": 30,
        "alim_pct": 16,
        "transport_pct": 8,
        "epargne_pct": 10,
        "loisirs_pct": 8,
        "charges_pct": 28,
        "aides": [
            "l'optimisation du prelevement a la source via le taux individualise pour les couples",
            "l'epargne salariale (PEE) avec abondement employeur defiscalise",
            "les titres-restaurant et la mutuelle d'entreprise obligatoire",
            "les deductions fiscales pour frais reels si vos deplacements professionnels sont importants",
            "le Plan d'Epargne Retraite (PER) pour deduire vos versements du revenu imposable",
        ],
        "evolution": "passer cadre via une promotion interne, obtenir un diplome Bac+5 en formation continue, changer de secteur vers un domaine plus remunerateur",
        "tranche_suivante": "confortable (2 700 a 3 500 euros brut)",
    },
    "confortable": {
        "percentile": "les 30 % superieurs",
        "vs_median": "superieur au salaire median francais, plaçant le salarie dans la tranche haute des remunerations",
        "metiers": [
            "cadre en entreprise ou responsable d'equipe",
            "ingenieur confirme en industrie ou informatique",
            "chef de projet digital ou marketing",
            "pharmacien salarie",
            "professeur agrege ou certifie avec anciennete",
            "responsable comptable ou financier",
            "consultant en cabinet de conseil",
        ],
        "secteurs": "industrie, conseil, sante, numerique, finance, education nationale",
        "experience": "5 a 15 ans d'experience ou diplome Bac+5 (ecole d'ingenieur, master, ecole de commerce)",
        "loyer_pct": 27,
        "alim_pct": 14,
        "transport_pct": 7,
        "epargne_pct": 15,
        "loisirs_pct": 10,
        "charges_pct": 27,
        "aides": [
            "le Plan d'Epargne Retraite (PER) pour deduire jusqu'a 10 % de vos revenus nets imposables",
            "l'investissement locatif Pinel ou Denormandie pour reduire votre impot sur le revenu",
            "l'epargne salariale (PEE, PERCO) avec abondement employeur jusqu'a 3 fois vos versements",
            "la negociation d'avantages en nature (voiture de fonction, telephone, ordinateur)",
            "les cheques CESU prefinances pour les services a la personne (exoneres jusqu'a 2 421 euros par an)",
        ],
        "evolution": "negocier un passage cadre superieur, developper une expertise rare sur le marche, viser un poste de direction dans une PME ou une ETI",
        "tranche_suivante": "cadre superieur (3 600 a 5 000 euros brut)",
    },
    "cadre_sup": {
        "percentile": "les 15 % superieurs",
        "vs_median": "nettement superieur au salaire median, situant le salarie parmi les cadres les mieux remuneres",
        "metiers": [
            "directeur de departement ou de business unit",
            "architecte logiciel ou lead developer senior",
            "medecin salarie en clinique ou en hopital",
            "directeur des ressources humaines",
            "avocat collaborateur confirme",
            "responsable grands comptes en B2B",
            "directeur commercial regional",
        ],
        "secteurs": "grandes entreprises, ESN, sante, cabinets d'avocats, industrie pharmaceutique, finance",
        "experience": "10 a 20 ans d'experience, souvent MBA ou diplome grande ecole, management d'equipe",
        "loyer_pct": 25,
        "alim_pct": 12,
        "transport_pct": 5,
        "epargne_pct": 20,
        "loisirs_pct": 12,
        "charges_pct": 26,
        "aides": [
            "le package de remuneration globale incluant bonus, stock-options et actions gratuites",
            "l'assurance-vie multisupport pour diversifier votre epargne avec une fiscalite avantageuse apres 8 ans",
            "le PER pour reduire votre TMI (Taux Marginal d'Imposition) qui est probablement a 30 %",
            "la negociation de la part variable (bonus) et des avantages non monetaires",
            "le FCPI ou FIP pour investir dans les PME avec reduction d'impot de 25 %",
        ],
        "evolution": "viser un poste de direction generale ou de comite executif, creer sa propre entreprise, devenir consultant independant a forte valeur ajoutee",
        "tranche_suivante": "haut revenu (5 100 a 7 000 euros brut)",
    },
    "haut_revenu": {
        "percentile": "les 5 % superieurs",
        "vs_median": "plus du double du salaire median, plaçant le salarie dans la categorie des hauts revenus en France",
        "metiers": [
            "directeur general adjoint d'une ETI",
            "partner junior en cabinet de conseil ou d'audit",
            "chirurgien salarie ou medecin specialiste hospitalier",
            "directeur financier (DAF) d'une grande entreprise",
            "expert en cybersecurite ou en intelligence artificielle",
            "directeur de la strategie ou du developpement",
            "trader junior en salle de marche",
        ],
        "secteurs": "finance de marche, conseil en strategie, technologie, sante specialisee, luxe, energie",
        "experience": "15 a 25 ans d'experience, expertise pointue ou management de haut niveau, reseau professionnel etendu",
        "loyer_pct": 22,
        "alim_pct": 10,
        "transport_pct": 5,
        "epargne_pct": 25,
        "loisirs_pct": 12,
        "charges_pct": 26,
        "aides": [
            "la defiscalisation immobiliere (LMNP, Malraux, monuments historiques) pour des economies substantielles",
            "le Plan d'Epargne Retraite avec deduction au TMI de 41 % pour un levier fiscal maximal",
            "la gestion de patrimoine via une SCI pour optimiser la transmission et les revenus fonciers",
            "les dons aux oeuvres et mecenat avec reduction d'impot de 66 % a 75 %",
            "le plafonnement des niches fiscales a 10 000 euros par an (hors investissements outre-mer et Sofica)",
        ],
        "evolution": "viser un poste de CEO ou de president, rejoindre un conseil d'administration, developper un portefeuille d'investissements generant des revenus passifs",
        "tranche_suivante": "tres haut revenu (7 100 a 10 000 euros brut)",
    },
    "tres_haut": {
        "percentile": "le top 1 % des salaires en France",
        "vs_median": "quatre a cinq fois superieur au salaire median, plaçant le salarie dans l'elite des remunerations françaises",
        "metiers": [
            "president-directeur general (PDG) d'une ETI ou filiale de grand groupe",
            "partner senior dans un cabinet de strategie (McKinsey, BCG, Bain)",
            "directeur general d'une grande entreprise cotee",
            "medecin chef de service en CHU ou clinique privee",
            "avocat associe dans un cabinet international",
            "directeur d'investissement en private equity",
            "chief technology officer (CTO) d'une scale-up",
        ],
        "secteurs": "direction generale, finance d'entreprise, conseil en strategie, medecine liberale hospitaliere, droit des affaires, capital-investissement",
        "experience": "20 ans ou plus d'experience, parcours d'excellence (grandes ecoles, MBA), responsabilite P&L significative",
        "loyer_pct": 18,
        "alim_pct": 8,
        "transport_pct": 4,
        "epargne_pct": 35,
        "loisirs_pct": 10,
        "charges_pct": 25,
        "aides": [
            "la creation d'une holding patrimoniale pour optimiser la fiscalite des dividendes et plus-values",
            "le mecanisme de l'apport-cession (article 150-0 B ter du CGI) pour reporter l'imposition des plus-values",
            "la gestion de fortune avec une allocation d'actifs diversifiee (immobilier, private equity, assurance-vie luxembourgeoise)",
            "l'expatriation fiscale encadree vers des pays a convention fiscale favorable (Portugal, Suisse)",
            "le pacte Dutreil pour preparer la transmission d'entreprise avec une exoneration de 75 % des droits",
        ],
        "evolution": "sieger dans plusieurs conseils d'administration, developper un patrimoine genérant des revenus passifs superieurs au salaire, transmettre de maniere optimisee",
        "tranche_suivante": None,
    },
}


# ── Formattage ────────────────────────────────────────────────────────────────

def _fmt(val):
    """Format un nombre en style francais : 1 500."""
    return f"{round(val):,}".replace(",", "\u202f").replace(".", ",")


# ── Sections de contenu ──────────────────────────────────────────────────────

def _section_positionnement(montant, tranche, direction):
    """Section 1 : Ce que represente ce salaire en France."""
    d = _TRANCHE_DATA[tranche]
    label = _get_tranche_label(tranche)

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "pos_bn", [
            f"Avec un salaire brut mensuel de {_fmt(montant)}\u202f\u20ac, votre remuneration se situe dans "
            f"la categorie \u00ab\u202f{label}\u202f\u00bb en France. ",
            f"Un salaire de {_fmt(montant)}\u202f\u20ac brut par mois vous place dans la categorie "
            f"\u00ab\u202f{label}\u202f\u00bb sur le marche du travail français. ",
            f"Percevoir {_fmt(montant)}\u202f\u20ac brut chaque mois correspond a la tranche "
            f"\u00ab\u202f{label}\u202f\u00bb des remunerations en France. ",
            f"A hauteur de {_fmt(montant)}\u202f\u20ac brut mensuel, vous vous inscrivez dans la categorie "
            f"\u00ab\u202f{label}\u202f\u00bb des salaires français. ",
        ])
    else:
        intro = _phrase_variant(montant, "pos_nb", [
            f"Pour atteindre un salaire net de {_fmt(montant)}\u202f\u20ac par mois, le brut necessaire vous place "
            f"dans la categorie \u00ab\u202f{label}\u202f\u00bb du marche français. ",
            f"Viser {_fmt(montant)}\u202f\u20ac net mensuel implique un salaire brut situe dans la tranche "
            f"\u00ab\u202f{label}\u202f\u00bb des remunerations en France. ",
            f"Un objectif de {_fmt(montant)}\u202f\u20ac net par mois requiert un brut correspondant "
            f"a la categorie \u00ab\u202f{label}\u202f\u00bb du marche de l'emploi français. ",
            f"Toucher {_fmt(montant)}\u202f\u20ac net mensuellement necessite un brut qui vous positionne "
            f"dans la categorie \u00ab\u202f{label}\u202f\u00bb en France. ",
        ])

    body = _phrase_variant(montant, "pos_body", [
        f"Ce niveau de remuneration est {d['vs_median']}. "
        f"Statistiquement, ce montant vous situe parmi {d['percentile']} des salaries du secteur prive en France. ",
        f"Cette remuneration est {d['vs_median']}. "
        f"En termes de distribution salariale, vous vous situez parmi {d['percentile']} des salaries du prive. ",
        f"Ce montant est {d['vs_median']}. "
        f"D'apres les statistiques de l'emploi, ce salaire vous positionne parmi {d['percentile']} des salaries du secteur prive. ",
    ])

    if tranche == "smic":
        body += (
            "Le SMIC brut mensuel en 2026 s'eleve a 1\u202f801,80\u202f\u20ac pour 35 heures hebdomadaires, "
            "soit 1\u202f426,30\u202f\u20ac net avant impot. Un salaire dans cette tranche correspond souvent "
            "a un temps partiel ou a un debut de carriere sans qualification specifique. "
            "Selon les donnees de la DARES, environ 17 % des salaries du prive sont remuneres au voisinage du SMIC."
        )
    elif tranche == "modeste":
        body += (
            "Ce salaire represente environ 75 a 90 % du salaire median. "
            "Selon l'INSEE, pres de 30 % des salaries français perçoivent une remuneration dans cette fourchette. "
            "Il correspond frequemment a des postes qualifies mais non-cadres, avec une anciennete de quelques annees."
        )
    elif tranche == "median":
        body += (
            "Vous vous situez dans la norme salariale française. "
            "Le salaire median signifie que 50 % des salaries gagnent moins et 50 % gagnent plus. "
            "Selon l'INSEE, le salaire brut median dans le secteur prive s'etablit autour de 2\u202f524\u202f\u20ac mensuels en equivalent temps plein. "
            "Ce niveau correspond souvent a un premier poste de cadre ou a un technicien superieur experimente."
        )
    elif tranche == "confortable":
        body += (
            "Ce salaire depasse largement la mediane et vous place dans la partie haute de la distribution salariale. "
            "Selon les statistiques de l'INSEE, seulement 30 % des salaries du prive atteignent ce niveau de remuneration. "
            "A ce stade, l'impot sur le revenu commence a peser significativement, avec un taux marginal d'imposition (TMI) generalement a 30 %."
        )
    elif tranche == "cadre_sup":
        body += (
            "Ce niveau de salaire est caracteristique des cadres superieurs et des profils hautement qualifies. "
            "D'apres l'APEC, le salaire median des cadres en France s'etablit autour de 52\u202f000\u202f\u20ac brut annuels, "
            "soit environ 4\u202f333\u202f\u20ac brut mensuels. Votre remuneration se situe donc dans la fourchette haute des cadres. "
            "Le plafond de la Securite sociale (3\u202f864\u202f\u20ac en 2026) est depasse, ce qui impacte le calcul de certaines cotisations."
        )
    elif tranche == "haut_revenu":
        body += (
            "A ce niveau, vous faites partie des 5 % de salaries les mieux payes en France. "
            "Votre TMI (Taux Marginal d'Imposition) est probablement de 41 %, ce qui rend chaque euro supplementaire "
            "fortement impose. La difference entre brut et net est encore plus marquee a cause du depassement "
            "du plafond de la Securite sociale sur la totalite du salaire. "
            "Les cotisations AGIRC-ARRCO en tranche 2 (au-dela du PSS) representent un prelevement supplementaire significatif."
        )
    else:
        body += (
            "A ce stade, votre remuneration depasse quatre fois le salaire median français. "
            "Vous etes dans le top 1 % des remunerations salariales du secteur prive. "
            "Votre TMI est tres probablement a 41 % voire 45 % pour la fraction depassant 180\u202f294\u202f\u20ac annuels. "
            "La gestion patrimoniale et l'optimisation fiscale deviennent des enjeux majeurs a ce niveau de revenu."
        )

    # Add fiscal detail paragraph
    if direction == "brut-en-net":
        fiscal = _phrase_variant(montant, "pos_fisc_bn", [
            f"En termes de cotisations, un salaire brut de {_fmt(montant)}\u202f\u20ac genere environ "
            f"{_fmt(round(montant * 0.22))}\u202f\u20ac a {_fmt(round(montant * 0.25))}\u202f\u20ac de prelevements "
            "salariaux selon que vous etes non-cadre ou cadre. Ces cotisations financent votre protection sociale\u202f: "
            "retraite de base et complementaire (AGIRC-ARRCO), assurance maladie, chomage et prevoyance. "
            "La CSG (Contribution Sociale Generalisee) a elle seule represente 9,2 % de 98,25 % du salaire brut, "
            "dont 6,8 % sont deductibles de votre revenu imposable.",
            f"Les cotisations salariales prelevees sur {_fmt(montant)}\u202f\u20ac brut representent entre "
            f"{_fmt(round(montant * 0.22))}\u202f\u20ac et {_fmt(round(montant * 0.25))}\u202f\u20ac selon votre statut. "
            "Elles couvrent la retraite de base, la complementaire AGIRC-ARRCO, l'assurance maladie et la prevoyance. "
            "La CSG, prelevee a 9,2 % sur 98,25 % du brut, constitue le poste le plus important, "
            "avec une part deductible de 6,8 % qui reduit votre base imposable.",
            f"Sur un brut mensuel de {_fmt(montant)}\u202f\u20ac, les prelevements salariaux oscillent entre "
            f"{_fmt(round(montant * 0.22))}\u202f\u20ac (non-cadre) et {_fmt(round(montant * 0.25))}\u202f\u20ac (cadre). "
            "Ces cotisations alimentent votre protection sociale\u202f: retraite, maladie, chomage et prevoyance. "
            "La CSG-CRDS, calculee sur 98,25 % du salaire brut, represente a elle seule pres de 10 % du brut.",
        ])
    else:
        fiscal = _phrase_variant(montant, "pos_fisc_nb", [
            f"Pour percevoir {_fmt(montant)}\u202f\u20ac net chaque mois, le salaire brut necessaire integre "
            "l'ensemble des cotisations salariales obligatoires\u202f: la part salariale pour la retraite de base "
            "(vieillesse plafonnee a 6,90 % et deplafonnee a 0,40 %), la retraite complementaire AGIRC-ARRCO "
            "(3,15 % en tranche 1), la CSG-CRDS (9,7 % sur 98,25 % du brut) et la CEG (0,86 % en tranche 1). "
            "Pour un cadre, il faut ajouter la CET de 0,14 %, ce qui explique qu'un brut legerement superieur "
            "est necessaire pour atteindre le meme montant net.",
            f"Atteindre {_fmt(montant)}\u202f\u20ac net par mois necessite un brut integrant toutes les cotisations "
            "obligatoires\u202f: vieillesse plafonnee (6,90 %) et deplafonnee (0,40 %), complementaire AGIRC-ARRCO "
            "(3,15 % sur la tranche 1), CSG-CRDS (9,7 % sur 98,25 % du brut) et CEG (0,86 %). "
            "Le statut cadre ajoute une CET de 0,14 %, augmentant legerement le brut requis.",
            f"Le brut necessaire pour obtenir {_fmt(montant)}\u202f\u20ac net inclut l'ensemble des prelevements "
            "salariaux\u202f: retraite de base (6,90 % + 0,40 %), AGIRC-ARRCO (3,15 % en T1), "
            "CSG-CRDS (9,7 % sur 98,25 % du brut) et CEG (0,86 % en T1). "
            "Un cadre doit negocier un brut legerement superieur en raison de la CET additionnelle de 0,14 %.",
        ])

    h2 = _phrase_variant(montant, "pos_h2", [
        f'Ce que represente un salaire de {_fmt(montant)}\u202f\u20ac en France',
        f'Salaire de {_fmt(montant)}\u202f\u20ac\u202f: positionnement en France',
        f'{_fmt(montant)}\u202f\u20ac par mois\u202f: ou se situe ce salaire\u202f?',
    ])

    return (
        f'<h2>{h2}</h2>\n'
        f'<p>{intro}{body}</p>\n<p>{fiscal}</p>'
    )


def _section_metiers(montant, tranche, direction):
    """Section 2 : Metiers et profils types."""
    d = _TRANCHE_DATA[tranche]

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "met_bn", [
            f"Un salaire brut de {_fmt(montant)}\u202f\u20ac par mois est typiquement associe "
            f"a des postes dans les secteurs suivants\u202f: {d['secteurs']}. ",
            f"Avec {_fmt(montant)}\u202f\u20ac brut mensuel, vous exercez probablement dans l'un de ces "
            f"secteurs\u202f: {d['secteurs']}. ",
            f"Les emplois remuneres {_fmt(montant)}\u202f\u20ac brut par mois se concentrent principalement "
            f"dans\u202f: {d['secteurs']}. ",
        ])
    else:
        intro = _phrase_variant(montant, "met_nb", [
            f"Pour negocier un salaire net de {_fmt(montant)}\u202f\u20ac par mois, vous visez "
            f"des postes que l'on retrouve principalement dans\u202f: {d['secteurs']}. ",
            f"Atteindre {_fmt(montant)}\u202f\u20ac net mensuel passe par des postes concentres "
            f"dans les secteurs suivants\u202f: {d['secteurs']}. ",
            f"Un salaire net de {_fmt(montant)}\u202f\u20ac par mois est accessible dans ces "
            f"domaines d'activite\u202f: {d['secteurs']}. ",
        ])

    metiers_list = ", ".join(d["metiers"][:5])
    metiers_extra = ", ".join(d["metiers"][5:])

    body = (
        f"Les metiers les plus courants a ce niveau incluent\u202f: {metiers_list}. "
    )
    if metiers_extra:
        body += f"On retrouve egalement des profils de {metiers_extra}. "

    body += (
        f"Le profil type correspond a un salarie avec {d['experience']}. "
    )

    if direction == "brut-en-net":
        body += (
            "Lorsque vous recevez une offre d'emploi affichant ce montant en brut, "
            "il est essentiel de comprendre combien vous percevrez reellement sur votre compte bancaire. "
            "Les cotisations salariales, qui representent environ 22 a 25 % du brut selon votre statut, "
            "constituent la principale difference entre le salaire brut annonce et le net perçu."
        )
    else:
        body += (
            "Lors d'une negociation salariale, connaitre le brut correspondant a votre objectif net "
            "vous donne un avantage strategique. Vous pouvez ainsi formuler votre demande en brut, "
            "qui est la reference pour les recruteurs, tout en sachant exactement ce que vous toucherez. "
            "N'oubliez pas que le brut necessaire pour un meme net est legerement plus eleve pour un cadre "
            "en raison de la cotisation CET supplementaire de 0,14 %."
        )

    # Add regional salary variation paragraph
    if tranche in ("smic", "modeste"):
        regional = (
            "A noter que les ecarts de remuneration varient considerablement selon les regions. "
            "En Ile-de-France, les salaires sont en moyenne 20 % plus eleves que dans le reste de la France "
            "pour des postes equivalents, mais le cout de la vie — notamment le logement — "
            "absorbe souvent cette difference. Les regions comme PACA, Auvergne-Rhone-Alpes et Occitanie "
            "offrent un compromis interessant entre niveau de salaire et qualite de vie."
        )
    elif tranche in ("median", "confortable"):
        regional = (
            "Les disparites regionales sont significatives a ce niveau de salaire. "
            "Un meme poste peut etre remunere 15 a 25 % de plus en region parisienne qu'en province, "
            "mais le differentiel de cout de la vie reduit cet avantage. Des metropoles comme Lyon, Nantes, "
            "Bordeaux ou Toulouse attirent de plus en plus d'entreprises et proposent des salaires competitifs "
            "avec une meilleure qualite de vie. Le teletravail generalise depuis 2020 a aussi modifie "
            "la donne en permettant d'acceder a des salaires parisiens depuis la province."
        )
    else:
        regional = (
            "A ce niveau de remuneration, les postes sont concentres dans les grandes metropoles "
            "et les sieges sociaux des grands groupes. Paris et sa region concentrent plus de 40 % "
            "des emplois cadres superieurs en France. Cependant, des poles d'excellence existent "
            "en province\u202f: la finance a Lyon, l'aeronautique a Toulouse, le numerique a Sophia Antipolis, "
            "l'industrie pharmaceutique a Strasbourg. L'implantation croissante de bureaux decentralises "
            "et le travail hybride offrent de nouvelles opportunites geographiques a ces niveaux de salaire."
        )

    h2 = _phrase_variant(montant, "met_h2", [
        f'Metiers et profils types pour {_fmt(montant)}\u202f\u20ac',
        f'Quels metiers pour {_fmt(montant)}\u202f\u20ac brut par mois\u202f?',
        f'Profils et secteurs associes a {_fmt(montant)}\u202f\u20ac',
    ])

    return (
        f'<h2>{h2}</h2>\n'
        f'<p>{intro}{body}</p>\n<p>{regional}</p>'
    )


def _section_budget(montant, tranche, direction):
    """Section 3 : Budget mensuel type."""
    d = _TRANCHE_DATA[tranche]

    # Estimer le net approximatif
    if direction == "brut-en-net":
        net_approx = round(montant * 0.78)
        intro_budget = f"Avec environ {_fmt(net_approx)}\u202f\u20ac net par mois (estimation non-cadre avant impot)"
    else:
        net_approx = montant
        intro_budget = f"Avec {_fmt(net_approx)}\u202f\u20ac net par mois"

    loyer = round(net_approx * d["loyer_pct"] / 100)
    alim = round(net_approx * d["alim_pct"] / 100)
    transport = round(net_approx * d["transport_pct"] / 100)
    epargne = round(net_approx * d["epargne_pct"] / 100)
    loisirs = round(net_approx * d["loisirs_pct"] / 100)
    charges = round(net_approx * d["charges_pct"] / 100)

    body = _phrase_variant(montant, "bud_body", [
        f"{intro_budget}, voici une repartition budgetaire type adaptee a ce niveau de revenus. "
        f"Le logement represente le poste le plus important avec environ {d['loyer_pct']}\u202f% du budget, "
        f"soit {_fmt(loyer)}\u202f\u20ac par mois. Ce montant correspond ",
        f"{intro_budget}, la repartition de vos depenses suit un schema classique pour cette tranche. "
        f"Le poste logement absorbe environ {d['loyer_pct']}\u202f% de vos revenus, "
        f"soit {_fmt(loyer)}\u202f\u20ac mensuels. Ce budget logement correspond ",
        f"{intro_budget}, voici comment se repartit un budget type a ce niveau de salaire. "
        f"Le logement, premier poste de depense, represente {d['loyer_pct']}\u202f% du revenu net, "
        f"soit environ {_fmt(loyer)}\u202f\u20ac par mois. Cette enveloppe correspond ",
    ])

    if tranche in ("smic", "modeste"):
        body += (
            "a un studio ou un T2 en province, ou a une chambre en region parisienne. "
            "La regle des 33 % de taux d'effort est difficile a respecter dans les grandes metropoles a ce niveau de salaire."
        )
    elif tranche in ("median", "confortable"):
        body += (
            "a un T2 ou T3 en province, ou a un studio/T2 en petite couronne parisienne. "
            "Ce budget permet de vivre correctement en adaptant le lieu de residence au cout de la vie local."
        )
    else:
        body += (
            "a un logement confortable dans la plupart des grandes villes françaises, "
            "y compris un appartement decent en region parisienne."
        )

    body += (
        f" L'alimentation represente environ {d['alim_pct']}\u202f% ({_fmt(alim)}\u202f\u20ac), "
        f"le transport {d['transport_pct']}\u202f% ({_fmt(transport)}\u202f\u20ac), "
        f"les loisirs et sorties {d['loisirs_pct']}\u202f% ({_fmt(loisirs)}\u202f\u20ac), "
        f"et les charges courantes (energie, telephone, internet, assurances) {d['charges_pct']}\u202f% ({_fmt(charges)}\u202f\u20ac). "
        f"La capacite d'epargne estimee est de {d['epargne_pct']}\u202f% du revenu net, soit environ {_fmt(epargne)}\u202f\u20ac par mois"
    )

    if tranche in ("smic", "modeste"):
        body += (
            ". Cette epargne reste fragile et il est recommande de constituer en priorite un fonds d'urgence "
            "de 3 mois de depenses sur un Livret A (taux de 2,4 % en 2026, plafond de 22\u202f950\u202f\u20ac). "
            "Le Livret d'Epargne Populaire (LEP), reserve aux revenus modestes, offre un taux plus avantageux de 3,5 %."
        )
    elif tranche in ("median", "confortable"):
        body += (
            ". Cette capacite d'epargne permet de constituer un apport immobilier ou de preparer des projets "
            "a moyen terme. Repartissez entre Livret A pour l'epargne de precaution, "
            "PEA (Plan d'Epargne en Actions) pour l'investissement long terme, "
            "et eventuellement une assurance-vie en fonds euros et unites de compte."
        )
    else:
        body += (
            ". A ce niveau d'epargne, une strategie patrimoniale diversifiee s'impose\u202f: "
            "assurance-vie multisupport, PEA, investissement immobilier (direct ou via SCPI), "
            "et potentiellement private equity ou fonds structures. "
            "Un conseil en gestion de patrimoine peut s'averer rentable pour optimiser l'allocation de vos actifs."
        )

    h2 = _phrase_variant(montant, "bud_h2", [
        f'Budget mensuel type avec {_fmt(montant)}\u202f\u20ac',
        f'Comment gerer un budget de {_fmt(net_approx)}\u202f\u20ac net par mois',
        f'Repartition budgetaire pour {_fmt(montant)}\u202f\u20ac',
    ])

    return f'<h2>{h2}</h2>\n<p>{body}</p>'


def _section_optimisation(montant, tranche, direction):
    """Section 4 : Conseils d'optimisation."""
    d = _TRANCHE_DATA[tranche]

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "opt_bn", [
            f"Avec un salaire brut de {_fmt(montant)}\u202f\u20ac, plusieurs leviers permettent "
            "d'optimiser votre remuneration nette et votre fiscalite. ",
            f"A {_fmt(montant)}\u202f\u20ac brut mensuel, des dispositifs existent pour augmenter "
            "votre pouvoir d'achat reel sans changer de poste. ",
            f"Pour un salaire brut de {_fmt(montant)}\u202f\u20ac, voici les strategies "
            "d'optimisation fiscale et sociale les plus pertinentes. ",
        ])
    else:
        intro = _phrase_variant(montant, "opt_nb", [
            f"En ciblant un net de {_fmt(montant)}\u202f\u20ac par mois, il est utile de connaitre "
            "les dispositifs qui peuvent ameliorer votre pouvoir d'achat reel au-dela du simple salaire. ",
            f"Avec un objectif de {_fmt(montant)}\u202f\u20ac net mensuel, plusieurs leviers permettent "
            "d'accroitre votre revenu disponible effectif. ",
            f"Si vous visez {_fmt(montant)}\u202f\u20ac net par mois, des mecanismes fiscaux et sociaux "
            "peuvent renforcer significativement votre pouvoir d'achat. ",
        ])

    conseils = d["aides"]
    body = "Voici les principaux dispositifs et conseils adaptes a votre tranche de revenus\u202f: "

    for i, conseil in enumerate(conseils):
        body += f"{conseil}"
        if i < len(conseils) - 1:
            body += "\u202f; "
        else:
            body += ". "

    if tranche in ("smic", "modeste"):
        body += (
            "Pensez egalement a verifier votre eligibilite sur le site mesdroitssociaux.gouv.fr qui centralise "
            "toutes les aides disponibles. Selon une etude de la DREES, pres de 30 % des beneficiaires potentiels "
            "ne reclament pas les aides auxquelles ils ont droit, soit un manque a gagner de plusieurs centaines "
            "d'euros par mois."
        )
    elif tranche in ("median", "confortable"):
        body += (
            "Pensez aussi a optimiser votre declaration d'impots\u202f: le choix entre deduction forfaitaire "
            "de 10 % et frais reels peut faire une difference significative si vous avez des frais "
            "de deplacement importants. La deduction des frais reels est avantageuse des que vos frais "
            "professionnels depassent 10 % de votre salaire net imposable."
        )
    else:
        body += (
            "A ce niveau de revenus, une strategie fiscale et patrimoniale structuree est indispensable. "
            "Le plafonnement global des niches fiscales a 10\u202f000\u202f\u20ac par an limite les possibilites "
            "de reduction d'impot, mais certains dispositifs (investissement outre-mer, Sofica) beneficient "
            "d'un plafond supplementaire de 18\u202f000\u202f\u20ac. "
            "Consultez un conseiller en gestion de patrimoine agree (CGP ou CGPI) pour une strategie sur mesure."
        )

    h2 = _phrase_variant(montant, "opt_h2", [
        f"Conseils d'optimisation pour {_fmt(montant)}\u202f\u20ac",
        f"Comment optimiser un salaire de {_fmt(montant)}\u202f\u20ac",
        f"Maximiser son pouvoir d'achat avec {_fmt(montant)}\u202f\u20ac",
    ])

    return f'<h2>{h2}</h2>\n<p>{intro}{body}</p>'


def _section_evolution(montant, tranche, direction):
    """Section 5 : Perspectives d'evolution."""
    d = _TRANCHE_DATA[tranche]

    if direction == "brut-en-net":
        intro = _phrase_variant(montant, "evo_bn", [
            f"Si vous percevez actuellement {_fmt(montant)}\u202f\u20ac brut par mois, "
            "voici comment envisager une progression salariale. ",
            f"Avec {_fmt(montant)}\u202f\u20ac brut mensuel, des perspectives d'evolution existent "
            "pour faire progresser votre remuneration. ",
            f"A {_fmt(montant)}\u202f\u20ac brut par mois, comment accelerer "
            "votre progression salariale\u202f? Voici les pistes concretes. ",
        ])
    else:
        intro = _phrase_variant(montant, "evo_nb", [
            f"Si votre objectif est d'atteindre {_fmt(montant)}\u202f\u20ac net par mois, "
            "voici les pistes pour y parvenir ou pour progresser au-dela. ",
            f"Viser {_fmt(montant)}\u202f\u20ac net mensuel est un objectif atteignable "
            "avec les bonnes strategies d'evolution professionnelle. ",
            f"Pour atteindre ou depasser {_fmt(montant)}\u202f\u20ac net par mois, "
            "plusieurs leviers de progression s'offrent a vous. ",
        ])

    body = f"Pour evoluer, la strategie recommandee est de {d['evolution']}. "

    if d["tranche_suivante"]:
        body += (
            f"La tranche salariale suivante est la tranche {d['tranche_suivante']}. "
            "Pour y acceder, plusieurs leviers sont a votre disposition\u202f: "
        )
    else:
        body += (
            "A ce niveau de remuneration, l'evolution passe moins par le salaire fixe que par "
            "la construction d'un patrimoine productif et l'acces a des formes de remuneration alternatives. "
        )

    if tranche == "smic":
        body += (
            "la formation professionnelle via le CPF (Compte Personnel de Formation, jusqu'a 500\u202f\u20ac par an "
            "credites automatiquement) est un levier puissant. Les secteurs en tension comme le numerique, "
            "la sante ou le BTP offrent des perspectives d'augmentation rapide apres une reconversion. "
            "En moyenne, un changement d'employeur permet une augmentation de 10 a 15 % contre 2 a 4 % "
            "pour une augmentation annuelle en interne."
        )
    elif tranche == "modeste":
        body += (
            "la montee en competences est cle. Les certifications professionnelles (titre RNCP, CQP) "
            "permettent souvent un bond salarial de 15 a 20 %. Le passage au statut cadre, accessible "
            "via une promotion interne ou un changement d'entreprise, ouvre l'acces a des grilles salariales "
            "superieures et a des avantages complementaires (mutuelle renforcee, prevoyance cadre, retraite supplementaire)."
        )
    elif tranche == "median":
        body += (
            "a ce stade, l'enjeu est de developper une expertise distinctive ou de prendre des responsabilites "
            "manageriales. Un MBA en formation continue ou un mastere specialise peut accelerer la progression. "
            "La mobilite geographique vers des bassins d'emploi dynamiques (Ile-de-France, Lyon, Toulouse) "
            "ou la mobilite sectorielle vers des industries plus remuneratrices (tech, finance, pharma) "
            "sont des strategies efficaces."
        )
    elif tranche == "confortable":
        body += (
            "les augmentations significatives passent souvent par la mobilite externe ou l'acces a des postes "
            "de direction. La negociation du package global (fixe + variable + avantages) devient aussi "
            "importante que le salaire fixe seul. Les stock-options et actions gratuites, exonerees de cotisations "
            "salariales sous certaines conditions, peuvent representer un complement de remuneration significatif."
        )
    elif tranche == "cadre_sup":
        body += (
            "a ce niveau, la progression passe par le reseau professionnel, la visibilite dans votre secteur "
            "et l'acces a des postes de gouvernance. Les chasseurs de tetes deviennent vos principaux interlocuteurs. "
            "La remuneration se negocie en package global\u202f: fixe + bonus (20 a 50 % du fixe) + LTI (Long Term Incentives) "
            "+ avantages (voiture, logement, retraite chapeau). Un bilan de competences ou un coaching de dirigeant "
            "peut aider a structurer votre parcours vers le top management."
        )
    elif tranche == "haut_revenu":
        body += (
            "la progression vers la tranche superieure repose sur l'acces a des postes de direction generale "
            "ou a des roles d'associe dans les cabinets de conseil et d'audit. Le mandat social (president, DG) "
            "offre une remuneration differente du salariat avec des possibilites d'optimisation specifiques. "
            "La creation ou la reprise d'entreprise est aussi une voie pour depasser le plafond salarial "
            "et acceder a la creation de valeur patrimoniale."
        )
    else:
        body += (
            "les revenus du travail atteignent un plateau naturel. La croissance de votre patrimoine global "
            "passe desormais par les revenus du capital\u202f: dividendes, plus-values, revenus fonciers, "
            "interets. La structuration via une holding permet de reinvestir les benefices avec une fiscalite "
            "allegee (regime mere-fille, integration fiscale). L'entrepreneuriat et l'investissement en private equity "
            "sont les voies privilegiees pour une creation de valeur exponentielle."
        )

    h2 = _phrase_variant(montant, "evo_h2", [
        f"Perspectives d'evolution salariale depuis {_fmt(montant)}\u202f\u20ac",
        f"Comment evoluer au-dela de {_fmt(montant)}\u202f\u20ac",
        f"Progresser depuis un salaire de {_fmt(montant)}\u202f\u20ac",
    ])

    return f'<h2>{h2}</h2>\n<p>{intro}{body}</p>'


# ── Variantes de structure ────────────────────────────────────────────────────

def _build_variant_0(montant, tranche, direction):
    """Variante 0 : budget > metiers > optimisation > positionnement > evolution."""
    sections = [
        _section_budget(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_1(montant, tranche, direction):
    """Variante 1 : metiers > positionnement > budget > evolution > optimisation."""
    sections = [
        _section_metiers(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_2(montant, tranche, direction):
    """Variante 2 : positionnement > budget > evolution > metiers > optimisation."""
    sections = [
        _section_positionnement(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
        _section_optimisation(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_3(montant, tranche, direction):
    """Variante 3 : optimisation > positionnement > metiers > budget > evolution."""
    sections = [
        _section_optimisation(montant, tranche, direction),
        _section_positionnement(montant, tranche, direction),
        _section_metiers(montant, tranche, direction),
        _section_budget(montant, tranche, direction),
        _section_evolution(montant, tranche, direction),
    ]
    return "\n".join(sections)


def _build_variant_4(montant, tranche, direction):
    """Variante 4 : evolution > optimisation > positionnement > budget > metiers."""
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
        str: contenu HTML (5 sections h2) a injecter dans {{DESCRIPTION_CONTEXTUELLE}}
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

    # Check that adjacent amounts get different variants
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
