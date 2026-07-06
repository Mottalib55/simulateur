#!/usr/bin/env python3
"""
Add comprehensive content enrichments to all pages:
- Conversion tables
- FAQ sections  
- Example scenarios
- Extended content
"""
import re

# Read the current file
with open('generate-pages.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Starting content enrichment...")

# Define FAQ data for différent page types
STATUS_FAQS = {
    "cadre": [
        {"q": "Quelle est la différence entre cadre et non-cadre pour le salaire net ?", "a": "Un cadre payé environ 3% de cotisations supplémentaires, notamment la CET à 0,14%. Pour un même brut, le net cadre est légèrement inférieur au net non-cadre."},
        {"q": "Comment est calculée la cotisation CET pour les cadres ?", "a": "La CET (Contribution d'Équilibre Technique) représente 0,14% du salaire brut total. Elle finance l'équilibre du régime de retraite complémentaire AGIRC-ARRCO."},
        {"q": "Un cadre a-t-il une meilleure retraite qu'un non-cadre ?", "a": "Oui, grâce aux cotisations AGIRC-ARRCO majorées sur la tranche 2, les cadres accumulent plus de points de retraite complémentaire, surtout sur les salaires élevés."},
        {"q": "Le statut cadre change-t-il le calcul de l'impôt sur le revenu ?", "a": "Non, l'impôt est calculé sur le net imposable, identique pour cadres et non-cadres à salaire brut égal. Seules les cotisations sociales diffèrent."},
        {"q": "À partir de quel salaire brut est-on concerné par la tranche 2 AGIRC-ARRCO ?", "a": "La tranche 2 s'appliqué au-delà du plafond de la Sécurité sociale, soit 3 864 € brut mensuel en 2026. Le taux passé alors de 3,15% à 8,64%."}
    ],
    "non-cadre": [
        {"q": "Quel est le taux moyen de cotisations pour un non-cadre ?", "a": "En moyenne, les cotisations salariales représentent environ 22% du salaire brut pour un non-cadre, soit un coefficient de conversion brut-net d'environ 0,78."},
        {"q": "Les non-cadres paient-ils la cotisation CET ?", "a": "Non, la CET (0,14%) est réservée aux cadres. C'est la principale différence de cotisation entre cadres et non-cadres."},
        {"q": "Comment calculer rapidement son net à partir du brut en non-cadre ?", "a": "Multipliez votre salaire brut par 0,78 pour obtenir une estimation rapide. Par exemple : 2 000 € brut × 0,78 ≈ 1 560 € net."},
        {"q": "Les primes sont-elles soumises aux mêmes cotisations ?", "a": "Oui, les primes versées sur la fiche de paie sont soumises aux mêmes cotisations sociales que le salaire de base (environ 22%)."},
        {"q": "Y a-t-il des différences de cotisations selon les secteurs d'activité ?", "a": "Les cotisations de base (Sécurité sociale, retraite, CSG/CRDS) sont identiques. Seules certaines cotisations conventionnelles peuvent varier selon la branche professionnelle."}
    ]
}

# Content expansion for cadre page
cadre_expansion = '''
                
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Impact sur les hauts salaires</h3>
                <p>Pour les salaires supérieurs au plafond de la Sécurité sociale (3 864 €/mois), la différence s'accentue avec la tranche 2 de l'AGIRC-ARRCO à 8,64%. Un cadre à 6 000 € brut touchera environ 4 578 € net, contre 4 606 € pour un non-cadre au même brut.</p>
                
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Calcul détaillé exemple 3 500 € brut</h3>
                <p>Pour mieux comprendre, voici le détail des cotisations sur 3 500 € brut mensuel (cadre) :</p>
                <ul class="space-y-1">
                    <li>Vieillesse plafonnée (6,90% sur 3 500) : 241,50 €</li>
                    <li>Vieillesse déplafonnée (0,40%) : 14,00 €</li>
                    <li>AGIRC-ARRCO T1 (3,15% sur 3 500) : 110,25 €</li>
                    <li>CEG T1 (0,86%) : 30,10 €</li>
                    <li>CET cadre (0,14%) : 4,90 €</li>
                    <li>CSG déductible (6,80% sur 98,25%) : 233,50 €</li>
                    <li>CSG non déductible (2,40%) : 82,40 €</li>
                    <li>CRDS (0,50%) : 17,20 €</li>
                    <li><strong>Total cotisations</strong> : environ 733,85 €</li>
                    <li><strong>Net avant impôt</strong> : environ 2 766 €</li>
                </ul>
                
                <h3 class="text-lg font-semibold text-slate-900 mt-6">Forfait social et prévoyance</h3>
                <p>En tant que cadre, votre employeur doit obligatoirement souscrire un contrat de prévoyance complémentaire (décès, invalidité). Une partie de cette cotisation patronale peut être reversée en cotisation salariale, diminuant légèrement votre net final.</p>
            '''

# Inject cadre expansion
content = re.sub(
    r'(les cadres ne paient pas la cotisation CET.*?</li>\n\s+</ul>)',
    r'\1' + cadre_expansion,
    content,
    flags=re.DOTALL
)

print("✓ Added extended content for cadre page")

# Now add the page rendering modifications for all gen_status_pages
# Find and replace the rendering loop
old_status_render = '''    for p in pages:
        html = page_head(p["title"], p["desc"], f'{BASE_URL}/{p["slug"]}/', p["kw"])
        html += HEADER
        html += breadcrumb(p["h1"].replace('<span class="text-brand-600">', '').replace('</span>', ''))
        html += f\'\'\'
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 mb-6">{p["h1"]}</h1>
            </div>
        </section>\'\'\'
        html += calculator_widget(2500, p["statut_default"], "brut")
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

new_status_render = '''    # Add enrichment data
    for p in pages:
        # Add table based on status
        if "cadre" in p["slug"]:
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 3500, 4000, 5000], "cadre")
            p["faqs"] = generate_faq_section(STATUS_FAQS["cadre"])
            p["examples"] = generate_examples([
                {"name": "Sophie, 32 ans", "situation": "Ingénieure logiciel – cadre", "brut": "3 500 €", "net": "2 693 €", "net_apres_impot": "2 438 €"},
                {"name": "Marc, 45 ans", "situation": "Directeur commercial – cadre", "brut": "5 000 €", "net": "3 828 €", "net_apres_impot": "3 344 €"},
                {"name": "Léa, 28 ans", "situation": "Chef de projet marketing – cadre", "brut": "2 800 €", "net": "2 157 €", "net_apres_impot": "1 995 €"},
            ])
        elif "non-cadre" in p["slug"]:
            p["table"] = generate_conversion_table([1500, 2000, 2500, 3000, 3500, 4000, 5000], "non-cadre")
            p["faqs"] = generate_faq_section(STATUS_FAQS["non-cadre"])
            p["examples"] = generate_examples([
                {"name": "Julie, 28 ans", "situation": "Assistante administrative", "brut": "2 200 €", "net": "1 716 €", "net_apres_impot": "1 612 €"},
                {"name": "Thomas, 35 ans", "situation": "Technicien maintenance", "brut": "2 800 €", "net": "2 184 €", "net_apres_impot": "2 023 €"},
                {"name": "Emma, 42 ans", "situation": "Agent logistique", "brut": "2 000 €", "net": "1 560 €", "net_apres_impot": "1 488 €"},
            ])
        else:
            # Default for other status pages
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
        html += f\'\'\'
        <section class="px-4 pb-6">
            <div class="mx-auto max-w-4xl">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 mb-6">{p["h1"]}</h1>
            </div>
        </section>\'\'\'
        html += calculator_widget(2500, p["statut_default"], "brut")
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

content = content.replace(old_status_render, new_status_render)
print("✓ Modified gen_status_pages() rendering")

# Write back
with open('generate-pages.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Content enrichment complete!")
print("✓ File updated: generate-pages.py")
