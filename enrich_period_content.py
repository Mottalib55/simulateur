#!/usr/bin/env python3
"""Add enrichments to period and content pages"""
import re

with open('generate-pages.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Enriching period and content pages...")

# Find and replace gen_period_pages rendering
old_period_render = '''    for p in pages:
        html = page_head(p["title"], p["desc"], f'{BASE_URL}/{p["slug"]}/', p["kw"])
        html += HEADER
        html += breadcrumb(p["h1"].replace('<span class="text-brand-600">', '').replace('</span>', ''))
        html += f\'\'\'
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 mb-6">{p["h1"]}</h1>
            </div>
        </section>\'\'\'
        html += calculator_widget(2500, "non-cadre", "brut")
        html += f\'\'\'
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>\'\'\'
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\\n</body></html>"
        write_page(p["slug"], html)'''

new_period_render = '''    # Add enrichments
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
        html += f\'\'\'
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 mb-6">{p["h1"]}</h1>
            </div>
        </section>\'\'\'
        html += calculator_widget(2500, "non-cadre", "brut")
        html += f\'\'\'
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>\'\'\'
        if "table" in p and p["table"]:
            html += f\'\'\'
        <section class="py-12 px-4 bg-slate-50">
            <div class="mx-auto max-w-4xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6">Tableau de conversion brut → net</h2>
                {p["table"]}
            </div>
        </section>\'\'\'
        if "examples" in p and p["examples"]:
            html += f\'\'\'
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl">
                {p["examples"]}
            </div>
        </section>\'\'\'
        if "faqs" in p and p["faqs"]:
            html += p["faqs"]
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\\n</body></html>"
        write_page(p["slug"], html)'''

content = content.replace(old_period_render, new_period_render)
print("✓ Modified gen_period_pages() rendering")

# Now do gen_content_pages
old_content_render = '''    for p in pages:
        html = page_head(p["title"], p["desc"], f'{BASE_URL}/{p["slug"]}/', p["kw"])
        html += HEADER
        html += breadcrumb(p["title"].split(" :")[0].split(" 2026")[0])
        html += f\'\'\'
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 mb-6">{p["title"].split(" :")[0]}</h1>
            </div>
        </section>\'\'\'
        html += calculator_widget(2500, "non-cadre", "brut")
        html += f\'\'\'
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>\'\'\'
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\\n</body></html>"
        write_page(p["slug"], html)'''

new_content_render = '''    # Add FAQs to content pages
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
        html += f\'\'\'
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 mb-6">{p["title"].split(" :")[0]}</h1>
            </div>
        </section>\'\'\'
        html += calculator_widget(2500, "non-cadre", "brut")
        html += f\'\'\'
        <section class="bg-white border-t border-slate-200 py-12 px-4">
            <div class="mx-auto max-w-4xl prose prose-slate">
                {p["content"]}
            </div>
        </section>\'\'\'
        if "faqs" in p and p["faqs"]:
            html += p["faqs"]
        html += links_grid("Pages connexes", RELATED_LINKS)
        html += FOOTER
        html += "\\n</body></html>"
        write_page(p["slug"], html)'''

content = content.replace(old_content_render, new_content_render)
print("✓ Modified gen_content_pages() rendering")

# Write back
with open('generate-pages.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Period and content pages enriched!")
