const PSS_MENSUEL = 3864;
const PSS_ANNUEL = 46368;
const SMIC_MENSUEL_BRUT = 1801.80;
function calculerCotisationsSalariales(brutMensuel, statut, options) {
options = options || {};
const isCadre = statut === 'cadre';
const isAlsaceMoselle = options.alsaceMoselle || false;
const t1 = Math.min(brutMensuel, PSS_MENSUEL);
const t2 = Math.max(0, brutMensuel - PSS_MENSUEL);
const assietteCsgCrds = brutMensuel * 0.9825;
const cotisations = {
vieillessePlafonnee: { taux: 0.069, montant: t1 * 0.069, label: 'Vieillesse plafonnée', assiette: 'Tranche 1' },
vieillesseDeplafonee: { taux: 0.004, montant: brutMensuel * 0.004, label: 'Vieillesse déplafonnée', assiette: 'Totalité' },
agircArrcoT1: { taux: 0.0315, montant: t1 * 0.0315, label: 'AGIRC-ARRCO T1', assiette: 'Tranche 1' },
agircArrcoT2: { taux: 0.0864, montant: t2 * 0.0864, label: 'AGIRC-ARRCO T2', assiette: 'Tranche 2' },
cegT1: { taux: 0.0086, montant: t1 * 0.0086, label: 'CEG T1', assiette: 'Tranche 1' },
cegT2: { taux: 0.0108, montant: t2 * 0.0108, label: 'CEG T2', assiette: 'Tranche 2' },
csgDeductible: { taux: 0.068, montant: assietteCsgCrds * 0.068, label: 'CSG déductible', assiette: '98,25% du brut' },
csgNonDeductible: { taux: 0.024, montant: assietteCsgCrds * 0.024, label: 'CSG non déductible', assiette: '98,25% du brut' },
crds: { taux: 0.005, montant: assietteCsgCrds * 0.005, label: 'CRDS', assiette: '98,25% du brut' },
};
if (isCadre) {
cotisations.cet = { taux: 0.0014, montant: brutMensuel * 0.0014, label: 'CET (cadre)', assiette: 'Totalité' };
}
if (isAlsaceMoselle) {
cotisations.alsaceMoselle = { taux: 0.013, montant: brutMensuel * 0.013, label: 'Maladie Alsace-Moselle', assiette: 'Totalité' };
}
let total = 0;
for (const key in cotisations) {
total += cotisations[key].montant;
}
return { detail: cotisations, total };
}
function calculerCotisationsPatronales(brutMensuel) {
const t1 = Math.min(brutMensuel, PSS_MENSUEL);
const t2 = Math.max(0, brutMensuel - PSS_MENSUEL);
const seuilAllocFam = SMIC_MENSUEL_BRUT * 3.5;
const tauxAllocFam = brutMensuel <= seuilAllocFam ? 0.0345 : 0.0525;
const cotisations = {
maladie: { taux: 0.07, montant: brutMensuel * 0.07, label: 'Maladie', assiette: 'Totalité' },
vieillessePlafonnee: { taux: 0.0855, montant: t1 * 0.0855, label: 'Vieillesse plafonnée', assiette: 'Tranche 1' },
vieillesseDeplafonee: { taux: 0.0202, montant: brutMensuel * 0.0202, label: 'Vieillesse déplafonnée', assiette: 'Totalité' },
allocFamiliales: { taux: tauxAllocFam, montant: brutMensuel * tauxAllocFam, label: 'Allocations familiales', assiette: 'Totalité' },
chomage: { taux: 0.0405, montant: t1 * 0.0405, label: 'Chômage', assiette: 'Tranche A' },
agircArrcoT1: { taux: 0.0472, montant: t1 * 0.0472, label: 'AGIRC-ARRCO T1', assiette: 'Tranche 1' },
agircArrcoT2: { taux: 0.1295, montant: t2 * 0.1295, label: 'AGIRC-ARRCO T2', assiette: 'Tranche 2' },
atmp: { taux: 0.01, montant: brutMensuel * 0.01, label: 'AT/MP (taux moyen)', assiette: 'Totalité' },
cegT1: { taux: 0.0129, montant: t1 * 0.0129, label: 'CEG T1', assiette: 'Tranche 1' },
cegT2: { taux: 0.0162, montant: t2 * 0.0162, label: 'CEG T2', assiette: 'Tranche 2' },
cet: { taux: 0.0021, montant: brutMensuel * 0.0021, label: 'CET', assiette: 'Totalité' },
};
let total = 0;
for (const key in cotisations) {
total += cotisations[key].montant;
}
return { detail: cotisations, total };
}
function estimerImpotRevenu(netImposableAnnuel, nbParts, partsBase) {
nbParts = nbParts || 1;
partsBase = partsBase || 1;
const tranches = [
{ min: 0, max: 11497, taux: 0 },
{ min: 11497, max: 29315, taux: 0.11 },
{ min: 29315, max: 83823, taux: 0.30 },
{ min: 83823, max: 180294, taux: 0.41 },
{ min: 180294, max: Infinity, taux: 0.45 },
];
var revenuParPart = netImposableAnnuel / nbParts;
var impotParPart = 0;
for (var i = 0; i < tranches.length; i++) {
var tranche = tranches[i];
if (revenuParPart <= tranche.min) break;
var base = Math.min(revenuParPart, tranche.max) - tranche.min;
impotParPart += base * tranche.taux;
}
var impotQF = impotParPart * nbParts;
// Plafonnement du quotient familial : calcul sans QF (avec partsBase seulement)
var demiPartsSupp = nbParts - partsBase;
if (demiPartsSupp > 0) {
var revenuParPartBase = netImposableAnnuel / partsBase;
var impotSansQF = 0;
for (var j = 0; j < tranches.length; j++) {
var tr = tranches[j];
if (revenuParPartBase <= tr.min) break;
var b = Math.min(revenuParPartBase, tr.max) - tr.min;
impotSansQF += b * tr.taux;
}
impotSansQF = impotSansQF * partsBase;
// Plafond : 1 759 EUR par demi-part supplementaire
var plafondReduction = 1759 * (demiPartsSupp / 0.5);
var reductionQF = impotSansQF - impotQF;
if (reductionQF > plafondReduction) {
impotQF = impotSansQF - plafondReduction;
}
}
return Math.max(0, Math.round(impotQF));
}
function calculerNbParts(situation, nbEnfants) {
situation = situation || 'single';
nbEnfants = nbEnfants || 0;
var partsBase = situation === 'couple' ? 2 : 1;
var partsEnfants = 0;
if (nbEnfants <= 2) {
partsEnfants = nbEnfants * 0.5;
} else {
partsEnfants = 1 + (nbEnfants - 2) * 1;
}
return { nbParts: partsBase + partsEnfants, partsBase: partsBase };
}
function calculerBrutVersNet(brutMensuel, statut, tempsTravail, options) {
statut = statut || 'non-cadre';
tempsTravail = tempsTravail != null ? tempsTravail : 1;
options = options || {};
var nbParts = options.nbParts || 1;
var partsBase = options.partsBase || 1;
const brutEffectif = brutMensuel * tempsTravail;
const salariales = calculerCotisationsSalariales(brutEffectif, statut, options);
const patronales = calculerCotisationsPatronales(brutEffectif);
const netAvantImpot = brutEffectif - salariales.total;
const csgNonDed = salariales.detail.csgNonDeductible.montant;
const crds = salariales.detail.crds.montant;
const netImposableMensuel = brutEffectif - salariales.total + csgNonDed + crds;
const netImposableAnnuel = netImposableMensuel * 12;
const abattement = Math.min(Math.max(netImposableAnnuel * 0.1, 495), 14171);
const netImposableApresAbattement = netImposableAnnuel - abattement;
const impotAnnuel = estimerImpotRevenu(netImposableApresAbattement, nbParts, partsBase);
const impotMensuel = Math.round(impotAnnuel / 12);
const netApresImpot = netAvantImpot - impotMensuel;
const coutEmployeur = brutEffectif + patronales.total;
return {
brutMensuel: brutEffectif,
brutAnnuel: brutEffectif * 12,
netAvantImpot: Math.round(netAvantImpot * 100) / 100,
netApresImpot: Math.round(netApresImpot * 100) / 100,
netImposableMensuel: Math.round(netImposableMensuel * 100) / 100,
impotMensuel,
impotAnnuel,
coutEmployeur: Math.round(coutEmployeur * 100) / 100,
detailCotisationsSalariales: salariales.detail,
detailCotisationsPatronales: patronales.detail,
totalSalarial: Math.round(salariales.total * 100) / 100,
totalPatronal: Math.round(patronales.total * 100) / 100,
tauxCotisationsSalariales: Math.round((salariales.total / brutEffectif) * 1000) / 10,
};
}
function calculerNetVersBrut(netMensuelCible, statut, tempsTravail, options) {
statut = statut || 'non-cadre';
tempsTravail = tempsTravail != null ? tempsTravail : 1;
options = options || {};
let brutEstime = netMensuelCible * 1.3;
for (let i = 0; i < 50; i++) {
const resultat = calculerBrutVersNet(brutEstime, statut, tempsTravail, options);
const diff = resultat.netAvantImpot - netMensuelCible;
if (Math.abs(diff) < 0.01) break;
brutEstime -= diff * 0.7;
}
return calculerBrutVersNet(brutEstime, statut, tempsTravail, options);
}
function calculerNetApresImpotVersBrut(netApresImpotCible, statut, tempsTravail, options) {
statut = statut || 'non-cadre';
tempsTravail = tempsTravail != null ? tempsTravail : 1;
options = options || {};
let brutEstime = netApresImpotCible * 1.5;
for (let i = 0; i < 80; i++) {
const resultat = calculerBrutVersNet(brutEstime, statut, tempsTravail, options);
const diff = resultat.netApresImpot - netApresImpotCible;
if (Math.abs(diff) < 0.01) break;
brutEstime -= diff * 0.5;
}
return calculerBrutVersNet(brutEstime, statut, tempsTravail, options);
}
function formatMoney(val) {
if (val == null || isNaN(val)) return '0 €';
return Math.round(val).toLocaleString('fr-FR') + ' €';
}
function formatMoneyPrecis(val) {
if (val == null || isNaN(val)) return '0,00 €';
return val.toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
}
