#!/usr/bin/env python3
"""Replace generic 'Calculateur rapide' widgets with page-specific mini-simulators."""

import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

# Pattern to match the widget block: from <section class="py-12 px-4"> containing "Calculateur rapide"
# through the closing </script> of the widget JS
WIDGET_RE = re.compile(
    r'<section class="py-12 px-4">\s*<div class="mx-auto max-w-3xl">\s*<h2[^>]*>Calculateur rapide</h2>.*?</script>',
    re.DOTALL
)

def replace_widget(page_dir, new_html):
    path = os.path.join(BASE, page_dir, 'index.html')
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return False
    content = open(path, 'r', encoding='utf-8').read()
    if 'Calculateur rapide' not in content:
        print(f"  SKIP (no widget): {page_dir}")
        return False
    m = WIDGET_RE.search(content)
    if not m:
        print(f"  SKIP (regex no match): {page_dir}")
        return False
    new_content = content[:m.start()] + new_html + content[m.end():]
    open(path, 'w', encoding='utf-8').write(new_content)
    print(f"  OK: {page_dir}")
    return True

# ============================================================
# 1. salaire-brut-net-cadre – "Simulateur Cadre"
# ============================================================
W01 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Cadre</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div class="flex items-end">
                            <span class="inline-block rounded-lg bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600 w-full text-center">Statut : Cadre</span>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net mensuel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">CET (0,14%)</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-cet">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Taux cotisations</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-taux">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, 'cadre', 1);
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
            const cet = r.detailCotisationsSalariales.cet;
            document.getElementById('res-cet').textContent = cet ? formatMoneyPrecis(cet.montant) : '0,00 €';
            document.getElementById('res-taux').textContent = r.tauxCotisationsSalariales + ' %';
        }
        inp.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 2. salaire-brut-net-non-cadre – "Simulateur Non-Cadre"
# ============================================================
W02 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Non-Cadre</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div class="flex items-end">
                            <span class="inline-block rounded-lg bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600 w-full text-center">Statut : Non-cadre</span>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net mensuel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Taux cotisations</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-taux">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Écart avec cadre</p>
                            <p class="text-2xl font-bold text-emerald-600" id="res-écart">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const nc = calculerBrutVersNet(v, 'non-cadre', 1);
            const c = calculerBrutVersNet(v, 'cadre', 1);
            document.getElementById('res-net').textContent = formatMoney(nc.netAvantImpot);
            document.getElementById('res-taux').textContent = nc.tauxCotisationsSalariales + ' %';
            const écart = nc.netAvantImpot - c.netAvantImpot;
            document.getElementById('res-écart').textContent = '+' + formatMoney(écart);
        }
        inp.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 3. salaire-brut-net-fonction-publique – "Simulateur Fonction Publique"
# ============================================================
W03 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Fonction Publique</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Traitement brut mensuel</label>
                            <input type="number" id="widget-input" value="2200" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Catégorie</label>
                            <select id="widget-cat" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="A">Catégorie A</option>
                                <option value="B" selected>Catégorie B</option>
                                <option value="C">Catégorie C</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Traitement net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Cotisation pension civile</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-pension">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const cat = document.getElementById('widget-cat');
        function calc() {
            const brut = parseFloat(inp.value) || 0;
            const pensionCivile = brut * 0.1110;
            const rafpAssiette = Math.min(brut * 0.20, brut);
            const rafp = Math.min(rafpAssiette, PSS_MENSUEL * 0.20) * 0.05;
            const csg = brut * 0.9825 * 0.068;
            const csgNd = brut * 0.9825 * 0.024;
            const crds = brut * 0.9825 * 0.005;
            const totalCot = pensionCivile + rafp + csg + csgNd + crds;
            const net = brut - totalCot;
            document.getElementById('res-net').textContent = formatMoney(net);
            document.getElementById('res-pension').textContent = formatMoneyPrecis(pensionCivile);
        }
        inp.addEventListener('input', calc);
        cat.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 4. salaire-brut-net-auto-entrepreneur – "Simulateur Auto-Entrepreneur"
# ============================================================
W04 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Auto-Entrepreneur</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Chiffre d\'affaires mensuel</label>
                            <input type="number" id="widget-input" value="3000" min="0" max="100000" step="100"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Type d\'activité</label>
                            <select id="widget-type" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="0.212">Prestations de services (BIC) – 21,2%</option>
                                <option value="0.211">Libéral (BNC) – 21,1%</option>
                                <option value="0.123">Vente de marchandises – 12,3%</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Revenu net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Cotisations</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-cot">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net imposable</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-imposable">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const typ = document.getElementById('widget-type');
        const abattements = {'0.212': 0.50, '0.211': 0.34, '0.123': 0.71};
        function calc() {
            const ca = parseFloat(inp.value) || 0;
            const taux = parseFloat(typ.value);
            const cot = ca * taux;
            const net = ca - cot;
            const abat = abattements[typ.value] || 0.34;
            const imposable = ca * (1 - abat);
            document.getElementById('res-net').textContent = formatMoney(net);
            document.getElementById('res-cot').textContent = formatMoney(cot);
            document.getElementById('res-imposable').textContent = formatMoney(imposable);
        }
        inp.addEventListener('input', calc);
        typ.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 5. salaire-brut-net-alternance-apprentissage – "Simulateur Alternance"
# ============================================================
W05 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Alternance</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Âge de l\'apprenti</label>
                            <input type="number" id="widget-age" value="20" min="16" max="29" step="1"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Année de contrat</label>
                            <select id="widget-année" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="1" selected>1ère année</option>
                                <option value="2">2ème année</option>
                                <option value="3">3ème année</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Salaire brut</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-brut">–</p>
                        </div>
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Salaire net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Impôt</p>
                            <p class="text-lg font-bold text-emerald-700" id="res-impôt">Exonéré</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const age = document.getElementById('widget-age');
        const année = document.getElementById('widget-année');
        /* Grille apprentissage 2026 (% du SMIC) */
        const grille = {
            '16-17': [0.27, 0.39, 0.55],
            '18-20': [0.43, 0.51, 0.67],
            '21-25': [0.53, 0.61, 0.78],
            '26+':   [1.00, 1.00, 1.00]
        };
        function trancheAge(a) {
            if (a < 18) return '16-17';
            if (a <= 20) return '18-20';
            if (a <= 25) return '21-25';
            return '26+';
        }
        function calc() {
            const a = parseInt(age.value) || 20;
            const y = parseInt(année.value) - 1;
            const pct = grille[trancheAge(a)][y] || 0.43;
            const brut = SMIC_MENSUEL_BRUT * pct;
            /* Apprenti exonéré de cotisations sous le SMIC */
            const net = brut <= SMIC_MENSUEL_BRUT ? brut : brut - (brut - SMIC_MENSUEL_BRUT) * 0.22;
            document.getElementById('res-brut').textContent = formatMoney(brut);
            document.getElementById('res-net').textContent = formatMoney(net);
            document.getElementById('res-impôt').textContent = 'Exonéré';
        }
        age.addEventListener('input', calc);
        année.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 6. salaire-brut-net-interim – "Simulateur Intérim"
# ============================================================
W06 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Intérim</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mission</label>
                            <input type="number" id="widget-input" value="2000" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net mission</p>
                            <p class="text-xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">IFM net (10%)</p>
                            <p class="text-xl font-bold text-slate-900" id="res-ifm">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">ICCP net (10%)</p>
                            <p class="text-xl font-bold text-slate-900" id="res-iccp">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Total fin mission</p>
                            <p class="text-xl font-bold text-emerald-700" id="res-total">–</p>
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
            const brut = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(brut, sel.value, 1);
            const tauxNet = r.netAvantImpot / brut || 0;
            const ifmBrut = brut * 0.10;
            const iccpBrut = (brut + ifmBrut) * 0.10;
            const ifmNet = ifmBrut * tauxNet;
            const iccpNet = iccpBrut * tauxNet;
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('res-ifm').textContent = formatMoney(ifmNet);
            document.getElementById('res-iccp').textContent = formatMoney(iccpNet);
            document.getElementById('res-total').textContent = formatMoney(r.netAvantImpot + ifmNet + iccpNet);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 7. salaire-brut-net-stage – "Simulateur Stage"
# ============================================================
W07 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Stage</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Gratification mensuelle brute</label>
                            <input type="number" id="widget-input" value="700" min="0" max="5000" step="10"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Heures / mois</label>
                            <input type="number" id="widget-heures" value="154" min="1" max="200" step="1"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Gratification nette</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Statut</p>
                            <p class="text-lg font-bold text-slate-900" id="res-statut">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const heu = document.getElementById('widget-heures');
        function calc() {
            const brut = parseFloat(inp.value) || 0;
            const heures = parseFloat(heu.value) || 154;
            const seuil = 4.35 * heures;
            var net, statut;
            if (brut <= seuil) {
                net = brut;
                statut = 'Exonéré de cotisations';
            } else {
                var excedent = brut - seuil;
                var cotis = excedent * 0.22;
                net = brut - cotis;
                statut = 'Cotisations sur ' + formatMoney(excedent);
            }
            document.getElementById('res-net').textContent = formatMoney(net);
            document.getElementById('res-statut').textContent = statut;
        }
        inp.addEventListener('input', calc);
        heu.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 8. salaire-brut-net-mensuel – "Calculateur Mensuel"
# ============================================================
W08 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Mensuel</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
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
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net mensuel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Cotisations</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-cot">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Taux cotisations</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-taux">–</p>
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
        const tmp = document.getElementById('widget-temps');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, parseInt(tmp.value)/100);
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('res-cot').textContent = formatMoney(r.totalSalarial);
            document.getElementById('res-taux').textContent = r.tauxCotisationsSalariales + ' %';
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        tmp.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 9. salaire-brut-net-annuel – "Calculateur Annuel"
# ============================================================
W09 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Annuel</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut annuel</label>
                            <input type="number" id="widget-input" value="30000" min="0" max="300000" step="500"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net annuel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-annuel">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net mensuel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-mensuel">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Impôt annuel estimé</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-impôt">–</p>
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
            const annuel = parseFloat(inp.value) || 0;
            const mensuel = annuel / 12;
            const r = calculerBrutVersNet(mensuel, sel.value, 1);
            document.getElementById('res-annuel').textContent = formatMoney(r.netAvantImpot * 12);
            document.getElementById('res-mensuel').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('res-impôt').textContent = formatMoney(r.impotAnnuel);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 10. salaire-brut-net-horaire – "Calculateur Horaire"
# ============================================================
W10 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Horaire</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Taux horaire brut</label>
                            <input type="number" id="widget-input" value="16.50" min="0" max="200" step="0.10"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Heures / semaine</label>
                            <input type="number" id="widget-heures" value="35" min="1" max="48" step="1"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Taux horaire net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-horaire">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Salaire mensuel net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-mensuel">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const heu = document.getElementById('widget-heures');
        function calc() {
            const taux = parseFloat(inp.value) || 0;
            const heures = parseFloat(heu.value) || 35;
            const brutMensuel = taux * heures * 52 / 12;
            const r = calculerBrutVersNet(brutMensuel, 'non-cadre', 1);
            const tauxNet = brutMensuel > 0 ? (r.netAvantImpot / brutMensuel) * taux : 0;
            document.getElementById('res-horaire').textContent = formatMoneyPrecis(tauxNet);
            document.getElementById('res-mensuel').textContent = formatMoney(r.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        heu.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 11. salaire-brut-net-journalier – "Calculateur Journalier"
# ============================================================
W11 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Journalier</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut journalier</label>
                            <input type="number" id="widget-input" value="115" min="0" max="1000" step="1"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Jours / mois</label>
                            <input type="number" id="widget-jours" value="21.67" min="1" max="31" step="0.01"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net journalier</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-jour">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Salaire mensuel net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-mensuel">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const jrs = document.getElementById('widget-jours');
        function calc() {
            const jour = parseFloat(inp.value) || 0;
            const jours = parseFloat(jrs.value) || 21.67;
            const brutMensuel = jour * jours;
            const r = calculerBrutVersNet(brutMensuel, 'non-cadre', 1);
            const netJour = jours > 0 ? r.netAvantImpot / jours : 0;
            document.getElementById('res-jour').textContent = formatMoneyPrecis(netJour);
            document.getElementById('res-mensuel').textContent = formatMoney(r.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        jrs.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 12. taux-horaire-brut-net – "Convertisseur Taux Horaire"
# ============================================================
W12 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Convertisseur Taux Horaire</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Taux horaire brut</label>
                            <input type="number" id="widget-input" value="16.50" min="0" max="200" step="0.10"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Taux horaire net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-horaire">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Mensuel brut</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-brut">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Mensuel net</p>
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
            const taux = parseFloat(inp.value) || 0;
            const brutMensuel = taux * 151.67;
            const r = calculerBrutVersNet(brutMensuel, sel.value, 1);
            const tauxNet = brutMensuel > 0 ? (r.netAvantImpot / brutMensuel) * taux : 0;
            document.getElementById('res-horaire').textContent = formatMoneyPrecis(tauxNet);
            document.getElementById('res-brut').textContent = formatMoney(brutMensuel);
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 13. différence-salaire-brut-net – "Visualiser la Différence"
# ============================================================
W13 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Visualiser la Différence</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-4">
                        <div class="flex items-center gap-2 mb-2">
                            <span class="text-sm font-medium text-slate-700">Brut</span>
                            <span class="text-sm font-bold text-slate-900" id="res-brut">–</span>
                        </div>
                        <div class="w-full bg-slate-100 rounded-full h-8 relative overflow-hidden">
                            <div class="h-full rounded-full bg-brand-500 transition-all" id="bar-net" style="width:78%"></div>
                            <div class="absolute inset-0 flex items-center justify-center text-sm font-bold text-white" id="bar-label">–</div>
                        </div>
                        <div class="flex justify-between mt-1">
                            <span class="text-xs text-slate-500">Net : <span id="res-net2">–</span></span>
                            <span class="text-xs text-slate-500">Cotisations : <span id="res-cot2">–</span></span>
                        </div>
                    </div>
                    <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                        <p class="text-sm text-brand-600 font-medium">Pourcentage retenu</p>
                        <p class="text-3xl font-bold text-slate-900" id="res-pct">–</p>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            const pctNet = v > 0 ? (r.netAvantImpot / v * 100) : 0;
            document.getElementById('res-brut').textContent = formatMoney(v);
            document.getElementById('res-net2').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('res-cot2').textContent = formatMoney(r.totalSalarial);
            document.getElementById('bar-net').style.width = pctNet.toFixed(1) + '%';
            document.getElementById('bar-label').textContent = formatMoney(r.netAvantImpot) + ' net';
            document.getElementById('res-pct').textContent = (100 - pctNet).toFixed(1) + ' %';
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 14. cotisations-sociales-salariales – "Détail des Cotisations"
# ============================================================
W14 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Détail des Cotisations</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm" id="table-cotis">
                            <thead><tr class="border-b-2 border-slate-300">
                                <th class="py-2 text-left font-semibold">Cotisation</th>
                                <th class="py-2 text-right font-semibold">Taux</th>
                                <th class="py-2 text-right font-semibold">Montant</th>
                            </tr></thead>
                            <tbody></tbody>
                            <tfoot><tr class="border-t-2 border-slate-300 font-bold">
                                <td class="py-2">Total</td>
                                <td class="py-2 text-right" id="res-taux-total">–</td>
                                <td class="py-2 text-right" id="res-total">–</td>
                            </tr></tfoot>
                        </table>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            const tbody = document.querySelector('#table-cotis tbody');
            tbody.innerHTML = '';
            const d = r.detailCotisationsSalariales;
            for (const key in d) {
                const c = d[key];
                const tr = document.createElement('tr');
                tr.className = 'border-b border-slate-100';
                tr.innerHTML = '<td class="py-2">' + c.label + '</td><td class="py-2 text-right">' + (c.taux * 100).toFixed(2) + ' %</td><td class="py-2 text-right">' + formatMoneyPrecis(c.montant) + '</td>';
                tbody.appendChild(tr);
            }
            document.getElementById('res-taux-total').textContent = r.tauxCotisationsSalariales + ' %';
            document.getElementById('res-total').textContent = formatMoney(r.totalSalarial);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 15. salaire-net-imposable – "Comparateur Net / Net Imposable"
# ============================================================
W15 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Comparateur Net / Net Imposable</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net à payer</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-amber-50 border border-amber-200 p-4 text-center">
                            <p class="text-sm text-amber-600 font-medium">Net imposable</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-imposable">–</p>
                        </div>
                    </div>
                    <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                        <p class="text-sm text-slate-500 font-medium">Écart (CSG non déductible + CRDS)</p>
                        <p class="text-xl font-bold text-slate-900" id="res-écart">–</p>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('res-imposable').textContent = formatMoney(r.netImposableMensuel);
            const écart = r.netImposableMensuel - r.netAvantImpot;
            document.getElementById('res-écart').textContent = '+' + formatMoneyPrecis(écart);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 16. salaire-net-avant-après-impôt – "Avant et Après Impôt"
# ============================================================
W16 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Avant et Après Impôt</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net avant impôt</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-avant">–</p>
                        </div>
                        <div class="rounded-xl bg-red-50 border border-red-200 p-4 text-center">
                            <p class="text-sm text-red-500 font-medium">Impôt estimé (PAS)</p>
                            <p class="text-2xl font-bold text-red-600" id="res-impôt">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Net après impôt</p>
                            <p class="text-2xl font-bold text-emerald-700" id="res-après">–</p>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('res-avant').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('res-impôt').textContent = '−' + formatMoney(r.impotMensuel);
            document.getElementById('res-après').textContent = formatMoney(r.netApresImpot);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 17. lire-fiche-de-paie – "Simulateur Fiche de Paie"
# ============================================================
W17 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Fiche de Paie</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="space-y-2" id="fiche-paie">
                        <div class="flex justify-between py-2 border-b border-slate-200"><span class="font-semibold text-slate-900">Salaire brut</span><span class="font-bold text-slate-900" id="fp-brut">–</span></div>
                        <div class="flex justify-between py-2 border-b border-slate-100 text-red-600"><span>− Cotisations salariales</span><span id="fp-cotis">–</span></div>
                        <div class="flex justify-between py-2 border-b border-slate-200 bg-brand-50 px-2 rounded"><span class="font-semibold text-brand-700">Net à payer</span><span class="font-bold text-brand-700" id="fp-net">–</span></div>
                        <div class="flex justify-between py-2 border-b border-slate-100"><span class="text-slate-500">Net imposable</span><span id="fp-imposable">–</span></div>
                        <div class="flex justify-between py-2"><span class="text-slate-500">Coût employeur</span><span id="fp-coût">–</span></div>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('fp-brut').textContent = formatMoney(v);
            document.getElementById('fp-cotis').textContent = '−' + formatMoney(r.totalSalarial);
            document.getElementById('fp-net').textContent = formatMoney(r.netAvantImpot);
            document.getElementById('fp-imposable').textContent = formatMoney(r.netImposableMensuel);
            document.getElementById('fp-coût').textContent = formatMoney(r.coutEmployeur);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 18. 13eme-mois-brut-net – "Simulateur 13ème Mois"
# ============================================================
W18 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur 13ème Mois</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire mensuel brut</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">13ème mois net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Impôt estimé sur le 13ème mois</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-impôt">–</p>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            /* 13ème mois = même montant brut, mêmes cotisations */
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
            /* Impôt supplémentaire : comparer 12 mois vs 13 mois */
            const r12 = calculerBrutVersNet(v, sel.value, 1);
            var impot12 = r12.impotAnnuel;
            /* Avec 13ème mois : net imposable annuel sur 13 mois */
            var imposable13 = r12.netImposableMensuel * 13;
            var abat = Math.min(Math.max(imposable13 * 0.1, 495), 14171);
            var impot13 = estimerImpotRevenu(imposable13 - abat);
            document.getElementById('res-impôt').textContent = formatMoney(impot13 - impot12);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 19. heures-supplémentaires-brut-net – "Calculateur Heures Sup"
# ============================================================
W19 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Heures Sup</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Taux horaire brut</label>
                            <input type="number" id="widget-taux" value="16.50" min="0" max="200" step="0.10"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Heures sup / mois</label>
                            <input type="number" id="widget-nb" value="10" min="0" max="100" step="1"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Majoration</label>
                            <select id="widget-maj" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="0.25" selected>25%</option>
                                <option value="0.50">50%</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Brut heures sup</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-brut">–</p>
                        </div>
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net heures sup</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Économie vs heures normales</p>
                            <p class="text-2xl font-bold text-emerald-700" id="res-eco">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const taux = document.getElementById('widget-taux');
        const nb = document.getElementById('widget-nb');
        const maj = document.getElementById('widget-maj');
        function calc() {
            const t = parseFloat(taux.value) || 0;
            const n = parseFloat(nb.value) || 0;
            const m = parseFloat(maj.value) || 0.25;
            const brutHS = t * (1 + m) * n;
            /* Réduction cotisations salariales de 11,31% sur HS */
            const netHS = brutHS * (1 - 0.1131);
            /* Heures normales équivalentes */
            const brutNormal = t * n;
            const rNormal = calculerBrutVersNet(brutNormal, 'non-cadre', 1);
            const netNormal = rNormal.netAvantImpot;
            var eco = netHS - netNormal;
            document.getElementById('res-brut').textContent = formatMoney(brutHS);
            document.getElementById('res-net').textContent = formatMoney(netHS);
            document.getElementById('res-eco').textContent = '+' + formatMoney(eco);
        }
        taux.addEventListener('input', calc);
        nb.addEventListener('input', calc);
        maj.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 20. avantages-en-nature – "Impact Avantage en Nature"
# ============================================================
W20 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Impact Avantage en Nature</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut de base</label>
                            <input type="number" id="widget-base" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Avantage en nature</label>
                            <input type="number" id="widget-avantage" value="200" min="0" max="5000" step="10"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net avec avantage</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-avec">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net sans avantage</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-sans">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Surcoût cotisations</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-surcout">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const base = document.getElementById('widget-base');
        const avantage = document.getElementById('widget-avantage');
        const sel = document.getElementById('widget-statut');
        function calc() {
            const b = parseFloat(base.value) || 0;
            const a = parseFloat(avantage.value) || 0;
            const rAvec = calculerBrutVersNet(b + a, sel.value, 1);
            const rSans = calculerBrutVersNet(b, sel.value, 1);
            document.getElementById('res-avec').textContent = formatMoney(rAvec.netAvantImpot);
            document.getElementById('res-sans').textContent = formatMoney(rSans.netAvantImpot);
            document.getElementById('res-surcout').textContent = '+' + formatMoney(rAvec.totalSalarial - rSans.totalSalarial);
        }
        base.addEventListener('input', calc);
        avantage.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 21. smic-brut-net-2026 – "SMIC 2026 Net"
# ============================================================
W21 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">SMIC 2026 Net</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">SMIC mensuel brut</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-mb">–</p>
                        </div>
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">SMIC mensuel net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-mn">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">SMIC horaire brut</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-hb">–</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">SMIC horaire net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-hn">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">SMIC annuel brut</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-ab">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">SMIC annuel net</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-an">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const r = calculerBrutVersNet(SMIC_MENSUEL_BRUT, 'non-cadre', 1);
        document.getElementById('res-mb').textContent = formatMoneyPrecis(SMIC_MENSUEL_BRUT);
        document.getElementById('res-mn').textContent = formatMoney(r.netAvantImpot);
        var hb = SMIC_MENSUEL_BRUT / 151.67;
        var hn = r.netAvantImpot / 151.67;
        document.getElementById('res-hb').textContent = hb.toFixed(2) + ' \\u20ac';
        document.getElementById('res-hn').textContent = hn.toFixed(2) + ' \\u20ac';
        document.getElementById('res-ab').textContent = formatMoney(SMIC_MENSUEL_BRUT * 12);
        document.getElementById('res-an').textContent = formatMoney(r.netAvantImpot * 12);
    })();
    </script>'''

# ============================================================
# 22. salaire-moyen-france – "Comparez votre Salaire"
# ============================================================
W22 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Comparez votre Salaire</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-slate-700 mb-1">Votre salaire brut mensuel</label>
                        <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                            class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                    </div>
                    <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center mb-4">
                        <p class="text-sm text-brand-600 font-medium">Votre net mensuel</p>
                        <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                    </div>
                    <div class="space-y-3">
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span class="font-medium text-slate-700">Salaire médian : 2 100 € net</span>
                                <span id="lbl-médian" class="text-slate-500">–</span>
                            </div>
                            <div class="w-full bg-slate-100 rounded-full h-4 relative">
                                <div class="h-full rounded-full bg-amber-400" style="width:50%"></div>
                                <div class="absolute h-full top-0 w-0.5 bg-slate-900" id="marker-médian" style="left:50%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span class="font-medium text-slate-700">Salaire moyen : 2 700 € net</span>
                                <span id="lbl-moyen" class="text-slate-500">–</span>
                            </div>
                            <div class="w-full bg-slate-100 rounded-full h-4 relative">
                                <div class="h-full rounded-full bg-brand-400" style="width:50%"></div>
                                <div class="absolute h-full top-0 w-0.5 bg-slate-900" id="marker-moyen" style="left:50%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, 'non-cadre', 1);
            const net = r.netAvantImpot;
            document.getElementById('res-net').textContent = formatMoney(net);
            /* Jauge médian (2100) */
            var pctMedian = Math.min(100, (net / 4200) * 100);
            document.querySelectorAll('#marker-médian')[0].previousElementSibling.style.width = pctMedian + '%';
            document.getElementById('marker-médian').style.left = Math.min(100, (2100 / 4200) * 100) + '%';
            var diffMed = net - 2100;
            document.getElementById('lbl-médian').textContent = (diffMed >= 0 ? '+' : '') + formatMoney(diffMed);
            /* Jauge moyen (2700) */
            var pctMoyen = Math.min(100, (net / 5400) * 100);
            document.querySelectorAll('#marker-moyen')[0].previousElementSibling.style.width = pctMoyen + '%';
            document.getElementById('marker-moyen').style.left = Math.min(100, (2700 / 5400) * 100) + '%';
            var diffMoy = net - 2700;
            document.getElementById('lbl-moyen').textContent = (diffMoy >= 0 ? '+' : '') + formatMoney(diffMoy);
        }
        inp.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# ============================================================
# 23. négocier-salaire – "Simulateur Augmentation"
# ============================================================
W23 = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Augmentation</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut actuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Augmentation (%)</label>
                            <input type="number" id="widget-pct" value="5" min="0" max="100" step="0.5"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Nouveau brut</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-brut">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Gain net mensuel</p>
                            <p class="text-2xl font-bold text-emerald-700" id="res-gain">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Gain net annuel</p>
                            <p class="text-2xl font-bold text-emerald-700" id="res-annuel">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const pct = document.getElementById('widget-pct');
        const sel = document.getElementById('widget-statut');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const p = parseFloat(pct.value) || 0;
            const newBrut = v * (1 + p / 100);
            const rOld = calculerBrutVersNet(v, sel.value, 1);
            const rNew = calculerBrutVersNet(newBrut, sel.value, 1);
            const gain = rNew.netAvantImpot - rOld.netAvantImpot;
            document.getElementById('res-brut').textContent = formatMoney(newBrut);
            document.getElementById('res-gain').textContent = '+' + formatMoney(gain);
            document.getElementById('res-annuel').textContent = '+' + formatMoney(gain * 12);
        }
        inp.addEventListener('input', calc);
        pct.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# ============================================================
# Additional pages from the plan
# ============================================================

# salaire-brut-net-2026 – same as mensuel
W_BRUT_NET_2026 = W08

# salaire-brut-net-alsace-moselle
W_ALSACE = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Alsace-Moselle</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net Alsace-Moselle</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net régime général</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-général">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Surcoût Alsace-Moselle</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-écart">–</p>
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
            const v = parseFloat(inp.value) || 0;
            const rAM = calculerBrutVersNet(v, sel.value, 1, {alsaceMoselle: true});
            const rGen = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('res-net').textContent = formatMoney(rAM.netAvantImpot);
            document.getElementById('res-général').textContent = formatMoney(rGen.netAvantImpot);
            document.getElementById('res-écart').textContent = formatMoney(rGen.netAvantImpot - rAM.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# simulateur-augmentation – same as négocier-salaire
W_AUGMENTATION = W23

# simulateur-impôt-sur-le-revenu
W_IMPOT = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Simulateur Impôt sur le Revenu</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Impôt annuel estimé</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-impôt">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Prélèvement mensuel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-mensuel">–</p>
                        </div>
                        <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-center">
                            <p class="text-sm text-emerald-600 font-medium">Net après impôt</p>
                            <p class="text-2xl font-bold text-emerald-700" id="res-net">–</p>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('res-impôt').textContent = formatMoney(r.impotAnnuel);
            document.getElementById('res-mensuel').textContent = formatMoney(r.impotMensuel);
            document.getElementById('res-net').textContent = formatMoney(r.netApresImpot);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# coût-employeur
W_COUT = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Coût Employeur</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Coût employeur</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-coût">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Cotisations patronales</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-pat">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net salarié</p>
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
            const v = parseFloat(inp.value) || 0;
            const r = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('res-coût').textContent = formatMoney(r.coutEmployeur);
            document.getElementById('res-pat').textContent = formatMoney(r.totalPatronal);
            document.getElementById('res-net').textContent = formatMoney(r.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# calculateur-temps-partiel
W_TEMPS_PARTIEL = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Calculateur Temps Partiel</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut temps plein</label>
                            <input type="number" id="widget-input" value="2500" min="0" max="20000" step="50"
                                class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Temps de travail</label>
                            <select id="widget-temps" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="80" selected>80%</option>
                                <option value="60">60%</option>
                                <option value="50">50%</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
                            <select id="widget-statut" class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none">
                                <option value="non-cadre" selected>Non-cadre</option>
                                <option value="cadre">Cadre</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net temps partiel</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-net">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net temps plein</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-plein">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Différence</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-diff">–</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        const tmp = document.getElementById('widget-temps');
        const sel = document.getElementById('widget-statut');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const t = parseInt(tmp.value) / 100;
            const rPartiel = calculerBrutVersNet(v, sel.value, t);
            const rPlein = calculerBrutVersNet(v, sel.value, 1);
            document.getElementById('res-net').textContent = formatMoney(rPartiel.netAvantImpot);
            document.getElementById('res-plein').textContent = formatMoney(rPlein.netAvantImpot);
            document.getElementById('res-diff').textContent = formatMoney(rPartiel.netAvantImpot - rPlein.netAvantImpot);
        }
        inp.addEventListener('input', calc);
        tmp.addEventListener('change', calc);
        sel.addEventListener('change', calc);
        calc();
    })();
    </script>'''

# cadre-vs-non-cadre
W_CADRE_VS = '''\
<section class="py-12 px-4">
            <div class="mx-auto max-w-3xl">
                <h2 class="text-xl font-bold text-slate-900 mb-6 text-center">Comparateur Cadre vs Non-Cadre</h2>
                <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-slate-700 mb-1">Salaire brut mensuel</label>
                        <input type="number" id="widget-input" value="3000" min="0" max="20000" step="50"
                            class="w-full rounded-lg border border-slate-200 px-3 py-2 text-lg font-bold text-slate-900 focus:border-brand-500 focus:outline-none">
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
                        <div class="rounded-xl bg-brand-50 border border-brand-100 p-4 text-center">
                            <p class="text-sm text-brand-600 font-medium">Net Cadre</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-cadre">–</p>
                        </div>
                        <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                            <p class="text-sm text-slate-500 font-medium">Net Non-Cadre</p>
                            <p class="text-2xl font-bold text-slate-900" id="res-nc">–</p>
                        </div>
                    </div>
                    <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 text-center">
                        <p class="text-sm text-slate-500 font-medium">Différence (non-cadre − cadre)</p>
                        <p class="text-2xl font-bold text-emerald-600" id="res-diff">–</p>
                    </div>
                </div>
            </div>
        </section>
    <script src="/js/brut-net.js"></script>
    <script>
    (function() {
        const inp = document.getElementById('widget-input');
        function calc() {
            const v = parseFloat(inp.value) || 0;
            const rc = calculerBrutVersNet(v, 'cadre', 1);
            const rnc = calculerBrutVersNet(v, 'non-cadre', 1);
            document.getElementById('res-cadre').textContent = formatMoney(rc.netAvantImpot);
            document.getElementById('res-nc').textContent = formatMoney(rnc.netAvantImpot);
            const diff = rnc.netAvantImpot - rc.netAvantImpot;
            document.getElementById('res-diff').textContent = '+' + formatMoney(diff);
        }
        inp.addEventListener('input', calc);
        calc();
    })();
    </script>'''

# différence-salaire-brut-net already done (W13)
# Now map pages to widgets

PAGES = {
    'salaire-brut-net-cadre': W01,
    'salaire-brut-net-non-cadre': W02,
    'salaire-brut-net-fonction-publique': W03,
    'salaire-brut-net-auto-entrepreneur': W04,
    'salaire-brut-net-alternance-apprentissage': W05,
    'salaire-brut-net-interim': W06,
    'salaire-brut-net-stage': W07,
    'salaire-brut-net-mensuel': W08,
    'salaire-brut-net-annuel': W09,
    'salaire-brut-net-horaire': W10,
    'salaire-brut-net-journalier': W11,
    'taux-horaire-brut-net': W12,
    'différence-salaire-brut-net': W13,
    'cotisations-sociales-salariales': W14,
    'salaire-net-imposable': W15,
    'salaire-net-avant-après-impôt': W16,
    'lire-fiche-de-paie': W17,
    '13eme-mois-brut-net': W18,
    'heures-supplémentaires-brut-net': W19,
    'avantages-en-nature': W20,
    'smic-brut-net-2026': W21,
    'salaire-moyen-france': W22,
    'négocier-salaire': W23,
}

# Additional pages that also have the generic widget
EXTRA_PAGES = {
    'salaire-brut-net-2026': W_BRUT_NET_2026,
    'salaire-brut-net-alsace-moselle': W_ALSACE,
    'simulateur-augmentation': W_AUGMENTATION,
    'simulateur-impôt-sur-le-revenu': W_IMPOT,
    'coût-employeur': W_COUT,
    'calculateur-temps-partiel': W_TEMPS_PARTIEL,
    'cadre-vs-non-cadre': W_CADRE_VS,
}

if __name__ == '__main__':
    print("=== Customizing widgets for 23 guide pages ===")
    ok = 0
    for page, widget in PAGES.items():
        if replace_widget(page, widget):
            ok += 1
    print(f"\n=== Done: {ok}/{len(PAGES)} pages updated ===")

    print("\n=== Checking extra pages with generic widget ===")
    ok2 = 0
    for page, widget in EXTRA_PAGES.items():
        if replace_widget(page, widget):
            ok2 += 1
    print(f"\n=== Extra: {ok2}/{len(EXTRA_PAGES)} pages updated ===")
