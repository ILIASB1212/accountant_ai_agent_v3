# RAGAS Evaluation Summary Report

- **Dataset:** `Moroccan_Accounting_Golden_V2`
- **Experiment:** `RAGAS-LangGraph-Run-f769b30c`
- **Generated:** 2026-09-28T15:39:16
- **Cases evaluated:** 52

## Overall Metric Averages

| Metric | Average Score | Scored / Total |
| :--- | :--- | :--- |
| **Faithfulness** | 0.4612 | 52/52 |
| **Answer Correctness** | 0.5549 | 52/52 |
| **Answer Relevancy** | 0.7907 | 52/52 |
| **Context Precision** | 0.7804 | 52/52 |
| **Context Recall** | 0.6548 | 52/52 |

## Per-Question Breakdown

### Question 1

**User input:**
> Quel est le taux de TVA applicable aux exportations de biens et services au Maroc ?

**Expected (ground truth):**
```text
Les exportations de biens et services sont exonérées de TVA avec droit à déduction, soit un taux de 0% [citation:2].
```

**Agent response:**
```text
Au Maroc, les exportations de biens et de services sont exonérées de la taxe sur la valeur ajoutée (TVA) avec droit à déduction. Cela signifie que les produits livrés et les prestations de services rendues à l'exportation par les assujettis ne sont pas soumis à la TVA, à condition que certaines conditions soient remplies, notamment la justification de l'exportation par des documents appropriés. 

Pour plus de détails, vous pouvez consulter l'article 92 du Code Général des Impôts (CGI) qui traite des exonérations de la TVA.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.6048 |
| Answer Relevancy | 0.9340 |
| Context Precision | 1.0000 |
| Context Recall | 0.5000 |

---

### Question 2

**User input:**
> Achat d'un PC portable HP Victus pour 8500 MAD chez ElectroPlanet. Query: comptabilise l'achat.

**Expected (ground truth):**
```text
Débit: 2355 (Matériel informatique) 7083.33 MAD
Débit: 34551 (État - TVA récupérable sur immobilisations 20%) 1416.67 MAD
Crédit: 4481 (Dettes sur acquisitions d'immobilisations) 8500 MAD
```

**Agent response:**
```text
Pour comptabiliser l'achat d'un PC portable HP Victus pour 8500 MAD chez ElectroPlanet, vous pouvez utiliser les comptes suivants :

1. **Compte d'achat** : 2355 - Matériel informatique (pour l'achat du PC portable)
2. **Compte fournisseur** : 4411 - Fournisseurs (pour enregistrer la dette envers ElectroPlanet)

### Écriture comptable :
- **Débit** : 2355 Matériel informatique : 8500 MAD
- **Crédit** : 4411 Fournisseurs : 8500 MAD

Cela enregistre l'achat du matériel informatique et la dette envers le fournisseur.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.7962 |
| Answer Relevancy | 0.9653 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 3

**User input:**
> Quel est le taux de TVA applicable aux établissements hôteliers et restaurants au Maroc (hors alcool) ?

**Expected (ground truth):**
```text
Les services d'hébergement et de restauration (hors boissons alcoolisées) bénéficient d'un taux de TVA réduit de 10% [citation:2].
```

**Agent response:**
```text
Le taux de TVA applicable aux établissements hôteliers et restaurants au Maroc (hors alcool) est de **10%**.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.9761 |
| Answer Relevancy | 0.9842 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 4

**User input:**
> Déclaration TVA du mois : TVA collectée 15 000 MAD, TVA déductible 9 000 MAD. Paiement de la TVA due par virement.

**Expected (ground truth):**
```text
Débit: 4455 (État - TVA facturée) 15 000 MAD
Crédit: 34552 (État - TVA récupérable sur charges) 9 000 MAD
Crédit: 4441 (État - TVA due) 6 000 MAD

Puis :
Débit: 4441 (État - TVA due) 6 000 MAD
Crédit: 5141 (Banque) 6 000 MAD
```

**Agent response:**
```text
Pour la déclaration de TVA, voici comment vous pouvez comptabiliser les montants :

1. **TVA collectée** : 15 000 MAD
   - Compte à utiliser : **4455 TVA facturée** (pour la TVA collectée)

2. **TVA déductible** : 9 000 MAD
   - Compte à utiliser : **3455 TVA récupérable** (pour la TVA déductible)

3. **TVA due à payer** : 
   - Montant à payer = TVA collectée - TVA déductible = 15 000 MAD - 9 000 MAD = 6 000 MAD
   - Compte à utiliser : **4456 TVA due (suivant déclarations)** (pour la TVA due)

### Écritures comptables :
- **Pour la TVA collectée** :
  - Débit : 3455 TVA récupérable 9 000 MAD
  - Crédit : 4455 TVA facturée 15 000 MAD

- **Pour la TVA due** :
  - Crédit : 4456 TVA due 6 000 MAD

### Paiement de la TVA due par virement :
- Lors du paiement de la TVA due, vous devez débiter le compte de TVA due et créditer le compte bancaire :
  - Débit : 4456 TVA due 6 000 MAD
  - Crédit : 5141 Banque 6 000 MAD

Assurez-vous de bien suivre ces écritures pour une comptabilité précise.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2667 |
| Answer Correctness | 0.5200 |
| Answer Relevancy | 0.8497 |
| Context Precision | 1.0000 |
| Context Recall | 0.8000 |

---

### Question 5

**User input:**
> Quel est le taux de la cotisation minimale au Maroc ?

**Expected (ground truth):**
```text
Le taux de droit commun de la cotisation minimale est de 0,25% [citation:10].
```

**Agent response:**
```text
Le taux de la cotisation minimale au Maroc est fixé à :

- **0,25%** pour la plupart des activités.
- **0,15%** pour les opérations effectuées par les entreprises commerciales concernant les ventes de produits pétroliers et de gaz.

De plus, le montant de la cotisation minimale ne peut être inférieur à :

- **3 000 dirhams** pour les contribuables soumis à l'impôt sur les sociétés.
- **1 500 dirhams** pour les contribuables soumis à l'impôt sur le revenu au titre des revenus professionnels ou agricoles.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.7500 |
| Answer Correctness | 0.7231 |
| Answer Relevancy | 0.9297 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 6

**User input:**
> Quel est le taux de la cotisation AMO (Assurance Maladie Obligatoire) au Maroc en 2026 pour l'employeur et l'employé ?

**Expected (ground truth):**
```text
En 2026, le taux de cotisation à l'AMO est de 4,11% pour l'employeur et de 2,26% pour l'employé [citation:6].
```

**Agent response:**
```text
Je n'ai pas trouvé d'informations spécifiques sur le taux de la cotisation AMO (Assurance Maladie Obligatoire) pour l'année 2026. Les détails concernant les taux de cotisation peuvent être précisés dans les lois de finances annuelles, mais il semble que les informations disponibles ne les mentionnent pas explicitement pour 2026.

Pour obtenir des informations précises, je vous recommande de consulter les documents officiels ou les annonces du gouvernement marocain concernant la loi de finances pour 2026, ou de vérifier auprès des organismes compétents en matière de sécurité sociale au Maroc.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.2205 |
| Answer Relevancy | 0.0000 |
| Context Precision | 0.0000 |
| Context Recall | 1.0000 |

---

### Question 7

**User input:**
> Quel est le taux de croissance économique prévu pour le Maroc en 2025 ?

**Expected (ground truth):**
```text
Le taux de croissance de l'économie nationale est estimé à 4,8% pour l'année 2025, porté par la dynamique des secteurs non agricoles et la contribution croissante des secteurs à haute valeur ajoutée [citation:19].
```

**Agent response:**
```text
Je n'ai pas trouvé d'informations spécifiques sur le taux de croissance économique prévu pour le Maroc en 2025. Il serait utile de consulter des sources économiques ou des rapports gouvernementaux pour obtenir des prévisions précises. Si vous avez besoin d'autres informations ou d'une recherche plus approfondie, n'hésitez pas à demander !
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.3333 |
| Answer Correctness | 0.2190 |
| Answer Relevancy | 0.0000 |
| Context Precision | 0.0000 |
| Context Recall | 0.0000 |

---

### Question 8

**User input:**
> Paie du mois de mars : salaires bruts 50 000 MAD. Retenues CNSS 2 250 MAD et AMO 1 100 MAD. IR retenu à la source 5 000 MAD.

**Expected (ground truth):**
```text
Débit: 6171 (Rémunérations du personnel) 50 000 MAD
Crédit: 4441 (Caisse Nationale de Sécurité Sociale) 3 350 MAD
Crédit: 4452 (État - Impôts sur les salaires) 5 000 MAD
Crédit: 4432 (Rémunérations nettes dues au personnel) 41 650 MAD
```

**Agent response:**
```text
Pour la paie du mois de mars, voici les comptes comptables à utiliser pour enregistrer les différentes transactions :

1. **Salaires bruts (50 000 MAD)** :
   - Compte : **61711** (Rémunérations du personnel - Appointements et salaires)

2. **Retenues CNSS (2 250 MAD)** :
   - Compte : **4441** (Organismes sociaux - Caisse Nationale de la Sécurité Sociale)

3. **Retenues AMO (1 100 MAD)** :
   - Compte : **4445** (Organismes sociaux - Mutuelles)

4. **IR retenu à la source (5 000 MAD)** :
   - Compte : **44525** (Etat - IGR)

Ces comptes vous permettront de comptabiliser correctement les salaires et les retenues associées. Si vous avez besoin d'autres informations ou d'aide supplémentaire, n'hésitez pas à demander !
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.5455 |
| Answer Correctness | 0.2240 |
| Answer Relevancy | 0.8392 |
| Context Precision | 0.9167 |
| Context Recall | 0.7500 |

---

### Question 9

**User input:**
> Quelle est la date limite de dépôt de la déclaration annuelle du revenu global (IR) pour les revenus professionnels au titre de l'exercice 2025 ?

**Expected (ground truth):**
```text
Pour les contribuables titulaires de revenus professionnels soumis à l'IR selon le régime du résultat net réel ou simplifié, la date limite de souscription de la déclaration annuelle du revenu global au titre de l'exercice 2025 est fixée avant le 1er mai 2026 [citation:5].
```

**Agent response:**
```text
La date limite de dépôt de la déclaration annuelle du revenu global (IR) pour les revenus professionnels au titre de l'exercice 2025 n'est pas spécifiquement mentionnée dans les informations disponibles. Cependant, en général, la déclaration doit être déposée au plus tard le 30 avril de l'année suivant l'exercice concerné. Pour l'exercice 2025, cela signifierait que la déclaration devrait être déposée au plus tard le 30 avril 2026. 

Il est conseillé de vérifier les annonces officielles ou les mises à jour de la Direction Générale des Impôts pour toute modification éventuelle.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2500 |
| Answer Correctness | 0.7380 |
| Answer Relevancy | 0.0000 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 10

**User input:**
> Loyer mensuel d'un local commercial : 26 000 MAD HT. TVA 20%. Paiement par chèque bancaire.

**Expected (ground truth):**
```text
Débit: 6131 (Locations et charges locatives) 26 000 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 5 200 MAD
Crédit: 5141 (Banque) 31 200 MAD
```

**Agent response:**
```text
Pour comptabiliser le loyer mensuel d'un local commercial de 26 000 MAD HT avec une TVA de 20%, voici les étapes à suivre :

1. **Calcul de la TVA** :
   - Montant de la TVA = 26 000 MAD * 20% = 5 200 MAD
   - Montant total TTC = 26 000 MAD + 5 200 MAD = 31 200 MAD

2. **Comptabilisation** :
   - **Débit** du compte de charges pour le loyer (compte 6131 - Locations et charges locatives) : 26 000 MAD
   - **Débit** du compte de TVA récupérable (compte 3455 - TVA récupérable) : 5 200 MAD
   - **Crédit** du compte de banque (compte 514 - Banques) : 31 200 MAD

### Écriture comptable :
- **Débit** 6131 - Locations et charges locatives : 26 000 MAD
- **Débit** 3455 - TVA récupérable : 5 200 MAD
- **Crédit** 514 - Banques : 31 200 MAD

Cette écriture reflète le paiement du loyer par chèque bancaire, incluant la TVA.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.7550 |
| Answer Relevancy | 0.9174 |
| Context Precision | 0.5000 |
| Context Recall | 0.6667 |

---

### Question 11

**User input:**
> Achat fournitures de bureau: 450 MAD TTC en espèces. Query: Enregistre.

**Expected (ground truth):**
```text
Débit: 61227 (Fournitures de bureau non stockables) 375 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 75 MAD
Crédit: 5311 (Caisse) 450 MAD
```

**Agent response:**
```text
Pour enregistrer l'achat de fournitures de bureau pour un montant de 450 MAD TTC en espèces, vous pouvez utiliser les comptes suivants :

- **Compte d'achats de fournitures de bureau** : 61227 (Achats de fournitures de bureau)
- **Compte de caisse** : 5161 (Caisse)

### Écriture comptable :
- **Débit** : 61227 - Achats de fournitures de bureau : 450 MAD
- **Crédit** : 5161 - Caisse : 450 MAD

Cela reflète l'achat effectué en espèces.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2500 |
| Answer Correctness | 0.6555 |
| Answer Relevancy | 0.9274 |
| Context Precision | 1.0000 |
| Context Recall | 0.6667 |

---

### Question 12

**User input:**
> Facture Honoraires Comptable: 2000 MAD HT. Query: journal entry.

**Expected (ground truth):**
```text
Débit: 61365 (Honoraires) 2000 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 400 MAD
Crédit: 4411 (Fournisseurs) 2400 MAD
```

**Agent response:**
```text
To record the journal entry for the invoice of "Honoraires Comptable" amounting to 2000 MAD HT, you will need to consider the following accounts:

1. **Honoraires (Fees)**: This is typically recorded under account **61365** (Honoraires).
2. **TVA (Value Added Tax)**: The applicable VAT rate in Morocco is generally 20%. Therefore, you will need to calculate the VAT on the amount.

### Journal Entry
- **Debit**: 61365 - Honoraires: 2000 MAD
- **Debit**: 3455 - TVA récupérable (20% of 2000 MAD): 400 MAD
- **Credit**: 4411 - Fournisseurs (or the relevant creditor account): 2400 MAD

### Summary of the Entry
- **Total Debit**: 2400 MAD (2000 MAD for fees + 400 MAD for VAT)
- **Total Credit**: 2400 MAD (to the supplier or creditor account)

This entry reflects the recognition of the accounting fees and the associated VAT that can be recovered.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.5514 |
| Answer Relevancy | 0.9317 |
| Context Precision | 1.0000 |
| Context Recall | 0.6667 |

---

### Question 13

**User input:**
> Quel est le taux de cotisation CNSS pour l'employeur et pour l'employé au Maroc en 2026 ?

**Expected (ground truth):**
```text
En 2026, le taux global de cotisation à la CNSS est de 21,09% pour l'employeur et de 6,74% pour l'employé [citation:18][citation:12].
```

**Agent response:**
```text
En 2026, les taux de cotisation à la Caisse Nationale de Sécurité Sociale (CNSS) au Maroc sont les suivants :

- **Pour l'employeur** : 16,5% du salaire brut.
- **Pour l'employé** : 4,29% du salaire brut.

Ces taux sont applicables dans le cadre des cotisations pour la sécurité sociale, y compris les prestations de maladie, maternité, invalidité et décès.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.7143 |
| Answer Correctness | 0.8318 |
| Answer Relevancy | 0.9659 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 14

**User input:**
> Quel est le montant du budget alloué au fonds de compensation (صندوق المقاصة) pour maintenir la stabilité des prix des produits de base en 2026 ?

**Expected (ground truth):**
```text
Le gouvernement a alloué 14 milliards de dirhams au fonds de compensation pour 2026 afin de garantir la stabilité des prix des produits de base [citation:1].
```

**Agent response:**
```text
Le montant du budget alloué au fonds de compensation pour maintenir la stabilité des prix des produits de base en 2026 n'est pas spécifiquement mentionné dans les documents disponibles. Cependant, il est indiqué que pour l'année 2024, une dotation globale de 16,357 milliards de dirhams est prévue pour soutenir les prix du gaz butane, du sucre et de la farine de blé tendre. 

Pour des informations précises concernant 2026, il serait nécessaire de consulter les documents budgétaires spécifiques à cette année lorsque disponibles.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.4185 |
| Answer Relevancy | 0.0000 |
| Context Precision | 0.0000 |
| Context Recall | 0.0000 |

---

### Question 15

**User input:**
> Facture fournisseur : 12 000 MAD HT, TVA 20%. Achat de marchandises destinées à la revente. Règlement à crédit 30 jours.

**Expected (ground truth):**
```text
Débit: 6111 (Achats de marchandises) 12 000 MAD
Débit: 34551 (État - TVA récupérable sur immobilisations) 2 400 MAD
Crédit: 4411 (Fournisseurs) 14 400 MAD
```

**Agent response:**
```text
Pour comptabiliser la facture fournisseur de 12 000 MAD HT avec une TVA de 20%, voici les écritures comptables à réaliser :

1. **Achat de marchandises** (12 000 MAD HT) :
   - Compte d'achat de marchandises : **6111** (Achats de marchandises "groupe A")
   - Montant : 12 000 MAD

2. **TVA récupérable** (20% de 12 000 MAD) :
   - Compte de TVA récupérable : **3455** (TVA récupérable)
   - Montant : 2 400 MAD (12 000 MAD * 20%)

3. **Fournisseurs** (montant total à payer) :
   - Compte de fournisseurs : **4411** (Fournisseurs)
   - Montant total : 14 400 MAD (12 000 MAD + 2 400 MAD)

### Écritures comptables :
- **Débit** :
  - 6111 : 12 000 MAD
  - 3455 : 2 400 MAD

- **Crédit** :
  - 4411 : 14 400 MAD

### Résumé des comptes :
- **Achat de marchandises** : 6111
- **TVA récupérable** : 3455
- **Fournisseurs** : 4411

Ces écritures reflètent l'achat de marchandises destinées à la revente, avec un règlement à crédit de 30 jours.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.4737 |
| Answer Correctness | 0.9794 |
| Answer Relevancy | 0.9047 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 16

**User input:**
> Quel est le taux de la cotisation patronale pour les allocations familiales (家庭津贴) au Maroc en 2026 ?

**Expected (ground truth):**
```text
Le taux de cotisation patronale pour les allocations familiales est de 6,40% en 2026, entièrement à la charge de l'employeur [citation:6].
```

**Agent response:**
```text
Le taux de la cotisation patronale pour les allocations familiales au Maroc en 2026 est maintenu dans le cadre des mesures transitoires allant du 01/01/2023 au 31/12/2026. Cependant, le document ne précise pas le taux exact. Pour obtenir des informations précises sur ce taux, il serait préférable de consulter les textes législatifs ou les annonces officielles à l'approche de l'année 2026.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.7500 |
| Answer Correctness | 0.4439 |
| Answer Relevancy | 0.0000 |
| Context Precision | 0.0000 |
| Context Recall | 0.0000 |

---

### Question 17

**User input:**
> Quand la déclaration trimestrielle de TVA du 2ème trimestre 2026 doit-elle être déposée au Maroc ?

**Expected (ground truth):**
```text
La déclaration du chiffre d'affaires du 2ème trimestre 2026 et le versement de la TVA correspondante doivent être effectués au plus tard le 31 juillet 2026 [citation:17].
```

**Agent response:**
```text
La déclaration trimestrielle de TVA pour le 2ème trimestre 2026 doit être déposée au plus tard le 30 juillet 2026.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.5394 |
| Answer Relevancy | 0.9639 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 18

**User input:**
> Quel est le taux de l'IS pour les banques et sociétés d'assurance au Maroc en 2026 ?

**Expected (ground truth):**
```text
Le taux de l'IS pour les établissements de crédit, les organismes assimilés, Bank Al-Maghrib, la Caisse de Dépôt et de Gestion, et les entreprises d'assurances et de réassurance est de 40% en 2026 [citation:16][citation:4].
```

**Agent response:**
```text
En 2026, le taux de l'impôt sur les sociétés (IS) pour les établissements de crédit et les entreprises d'assurances et de réassurance au Maroc sera de **40%**.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.6092 |
| Answer Relevancy | 0.9538 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 19

**User input:**
> Facture Inwi professionnelle : 250 MAD TTC. Internet et téléphonie mobile. TVA 20%. Prélèvement automatique.

**Expected (ground truth):**
```text
Débit: 61451 (Frais de téléphone) 208,33 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 41,67 MAD
Crédit: 5141 (Banque) 250 MAD
```

**Agent response:**
```text
Pour comptabiliser la facture Inwi professionnelle de 250 MAD TTC pour Internet et téléphonie mobile avec une TVA de 20%, voici les informations pertinentes :

1. **Montant HT (Hors Taxes)** :
   - Montant TTC : 250 MAD
   - Taux de TVA : 20%
   - Montant HT = Montant TTC / (1 + Taux de TVA) = 250 / 1.20 = 208.33 MAD

2. **Montant de la TVA** :
   - Montant de la TVA = Montant TTC - Montant HT = 250 - 208.33 = 41.67 MAD

3. **Comptes à utiliser** :
   - Pour les **achats de services** (Internet et téléphonie mobile) : **6126 Achats de travaux, études et prestations de service**
   - Pour la **TVA récupérable** : **3455 Etat - TVA récupérable**

### Écriture comptable :
- **Débit** :
  - 6126 (Achats de travaux, études et prestations de service) : 208.33 MAD
  - 3455 (Etat - TVA récupérable) : 41.67 MAD

- **Crédit** :
  - 5121 (Banque) ou 4411 (Fournisseurs) : 250 MAD

### Résumé de l'écriture :
- **Débit** 6126 : 208.33 MAD
- **Débit** 3455 : 41.67 MAD
- **Crédit** 5121 ou 4411 : 250 MAD

Cette écriture reflète l'achat de services de télécommunication et la récupération de la TVA associée.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.3333 |
| Answer Correctness | 0.2239 |
| Answer Relevancy | 0.9320 |
| Context Precision | 0.0000 |
| Context Recall | 0.0000 |

---

### Question 20

**User input:**
> Le taux de l'IS pour les sociétés industrielles avec un bénéfice net inférieur à 100 millions de MAD est-il de 20% en 2026 ?

**Expected (ground truth):**
```text
Oui, à compter de 2026, le taux de l'IS pour les sociétés industrielles (et toutes sociétés non financières) dont le bénéfice net fiscal est inférieur à 100 millions de MAD est de 20% [citation:16][citation:4].
```

**Agent response:**
```text
Oui, le taux de l'impôt sur les sociétés (IS) pour les sociétés industrielles dont le bénéfice net est inférieur à 100 millions de MAD sera de 20% à partir de l'exercice ouvert le 1er janvier 2026.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.5000 |
| Answer Correctness | 0.7425 |
| Answer Relevancy | 0.9519 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 21

**User input:**
> Facture de papeterie : 600 MAD TTC, TVA 20%. Achat de fournitures de bureau. Paiement par chèque bancaire.

**Expected (ground truth):**
```text
Débit: 6121 (Achats de fournitures de bureau) 500 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 100 MAD
Crédit: 5141 (Banque) 600 MAD
```

**Agent response:**
```text
Pour comptabiliser l'achat de fournitures de bureau d'un montant de 600 MAD TTC avec une TVA de 20%, vous pouvez utiliser les comptes suivants :

1. **Achats de fournitures de bureau** : **61227** (Achats de fournitures de bureau)
2. **TVA récupérable** : **3455** (État - TVA récupérable)
3. **Banque** : **5141** (Banques)

### Écriture comptable :
- **Débit** :
  - 61227 (Achats de fournitures de bureau) : 500 MAD
  - 3455 (État - TVA récupérable) : 100 MAD

- **Crédit** :
  - 5141 (Banques) : 600 MAD

### Détails du calcul :
- Montant HT (Hors Taxes) = 600 MAD / 1.20 = 500 MAD
- Montant de la TVA = 600 MAD - 500 MAD = 100 MAD

Cette écriture reflète l'achat de fournitures de bureau, le montant de la TVA récupérable, et le paiement effectué par chèque bancaire.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.3846 |
| Answer Correctness | 0.6622 |
| Answer Relevancy | 0.9054 |
| Context Precision | 1.0000 |
| Context Recall | 0.3333 |

---

### Question 22

**User input:**
> Facture Maroc Telecom: 300 MAD TTC. Internet Fibre. Date: 12/04/2026. Query: Enregistre cette charge.

**Expected (ground truth):**
```text
Débit: 61451 (Frais de téléphone) 250 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 50 MAD
Crédit: 5141 (Banque) 300 MAD
```

**Agent response:**
```text
Pour enregistrer la charge de la facture de Maroc Telecom pour Internet Fibre d'un montant de 300 MAD TTC, voici les étapes à suivre :

1. **Identification des comptes** :
   - **Compte de charge** : Pour les services d'Internet, vous pouvez utiliser le compte **6134** (Frais de télécommunications).
   - **Compte de TVA** : La TVA est généralement de 20% au Maroc, donc vous devez également enregistrer la TVA récupérable.

2. **Calcul de la TVA** :
   - Montant TTC : 300 MAD
   - Taux de TVA : 20%
   - Montant HT (Hors Taxes) = 300 MAD / 1.20 = 250 MAD
   - Montant de la TVA = 300 MAD - 250 MAD = 50 MAD

3. **Écriture comptable** :
   - Débit du compte 6134 (Frais de télécommunications) : 250 MAD
   - Débit du compte 3455 (TVA récupérable) : 50 MAD
   - Crédit du compte 5121 (Banque ou Caisse) : 300 MAD

### Écriture comptable :
- **Débit** : 
  - 6134 - Frais de télécommunications : 250 MAD
  - 3455 - TVA récupérable : 50 MAD
- **Crédit** : 
  - 5121 - Banque ou Caisse : 300 MAD

Cette écriture comptable reflète l'enregistrement de la charge pour le service Internet ainsi que la TVA récupérable associée.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.7857 |
| Answer Correctness | 0.2201 |
| Answer Relevancy | 0.9290 |
| Context Precision | 0.5000 |
| Context Recall | 0.0000 |

---

### Question 23

**User input:**
> Combien de postes budgétaires nouveaux sont créés pour les secteurs de l'éducation et de la santé dans la loi de finances 2026 ?

**Expected (ground truth):**
```text
Plus de 27 000 postes budgétaires nouveaux sont créés pour soutenir les ressources humaines dans les secteurs de l'éducation et de la santé [citation:1][citation:7].
```

**Agent response:**
```text
Dans la loi de finances 2026, il n'y a pas d'informations spécifiques sur la création de nouveaux postes budgétaires pour les secteurs de l'éducation et de la santé. Cependant, il est mentionné que pour l'année budgétaire 2025, 600 postes budgétaires ont été créés au ministère de l'éducation nationale, du préscolaire et des sports, destinés à la régularisation de la situation des fonctionnaires titulaires d'un diplôme de doctorat.

Pour des informations précises sur les postes budgétaires créés spécifiquement pour 2026, il serait nécessaire de consulter le texte complet de la loi de finances ou des rapports associés.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.7500 |
| Answer Correctness | 0.4134 |
| Answer Relevancy | 0.0000 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 24

**User input:**
> Achat de marchandises: 5000 MAD HT, remise 5%. Query: comptabilise.

**Expected (ground truth):**
```text
Débit: 6111 (Achats de marchandises) 4750 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 950 MAD
Crédit: 4411 (Fournisseurs) 5700 MAD
```

**Agent response:**
```text
Pour comptabiliser l'achat de marchandises de 5000 MAD HT avec une remise de 5%, voici les étapes à suivre :

1. **Calculer le montant de la remise** :
   - Montant de la remise = 5000 MAD * 5% = 250 MAD
   - Montant après remise = 5000 MAD - 250 MAD = 4750 MAD

2. **Comptabilisation** :
   - **Débit** du compte d'achats de marchandises (compte 6111) pour 4750 MAD.
   - **Crédit** du compte de remise obtenue (compte 6119) pour 250 MAD.

### Écriture comptable :
- **Débit** : 6111 Achats de marchandises : 4750 MAD
- **Crédit** : 6119 Rabais, remises et ristournes obtenus sur achats de marchandises : 250 MAD

Cela reflète correctement l'achat de marchandises après application de la remise.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.8531 |
| Answer Relevancy | 0.9414 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 25

**User input:**
> Facture Maroc Telecom: 300 MAD TTC. Internet Fibre. Date: 12/04/2026. Query: Enregistre cette charge.

**Expected (ground truth):**
```text
Débit: 61451 (Frais de téléphone) 250 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 50 MAD
Crédit: 5141 (Banque) 300 MAD
```

**Agent response:**
```text
Pour enregistrer la charge de la facture de Maroc Telecom (300 MAD TTC) pour Internet Fibre, vous pouvez utiliser les comptes suivants :

1. **Compte de charge pour Internet** :  **6145 Frais postaux et frais de télécommunications** (ou un compte similaire selon votre plan comptable).
2. **Compte de TVA récupérable** : **3455 Etat - TVA récupérable**.

### Écriture comptable :
- **Débit** : 6145 (Frais postaux et frais de télécommunications) 300 MAD
- **Crédit** : 3455 (Etat - TVA récupérable) 0 MAD (si la TVA est incluse dans le montant total, il faut calculer la TVA à partir du montant TTC).

### Calcul de la TVA :
Si le taux de TVA applicable est de 20%, la TVA sur 300 MAD TTC serait :
- Montant HT = 300 MAD / 1.20 = 250 MAD
- TVA = 300 MAD - 250 MAD = 50 MAD

### Écriture comptable révisée :
- **Débit** : 6145 (Frais postaux et frais de télécommunications) 250 MAD
- **Débit** : 3455 (Etat - TVA récupérable) 50 MAD
- **Crédit** : 4411 (Fournisseurs) 300 MAD

Assurez-vous d'adapter les comptes selon votre plan comptable spécifique.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.2250 |
| Answer Relevancy | 0.9058 |
| Context Precision | 1.0000 |
| Context Recall | 0.0000 |

---

### Question 26

**User input:**
> Frais de déplacement taxi: 50 MAD. Query: comment enregistrer ?

**Expected (ground truth):**
```text
Débit: 61435 (Transports du personnel) 50 MAD
Crédit: 5311 (Caisse) 50 MAD
```

**Agent response:**
```text
Pour enregistrer les frais de déplacement en taxi de 50 MAD, vous devez utiliser le compte approprié pour les frais de transport ou de déplacement. Selon le plan comptable marocain, vous pouvez utiliser le compte suivant :

- **61431** : Voyages et déplacements

L'écriture comptable serait donc :

- **Débit** : 61431 (Voyages et déplacements) : 50 MAD
- **Crédit** : 512 (Banque ou Caisse) : 50 MAD

Cela reflète le coût du déplacement en taxi dans vos comptes.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.1667 |
| Answer Correctness | 0.3545 |
| Answer Relevancy | 0.9391 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 27

**User input:**
> Paiement d'une amende fiscale pour déclaration tardive de TVA : 1 500 MAD. Non déductible fiscalement.

**Expected (ground truth):**
```text
Débit: 6581 (Charges diverses) 1 500 MAD
Crédit: 5141 (Banque) 1 500 MAD
```

**Agent response:**
```text
Pour le paiement d'une amende fiscale de 1 500 MAD pour déclaration tardive de TVA, voici les informations pertinentes :

### Comptabilisation de l'amende
L'amende fiscale est généralement enregistrée dans le compte suivant :
- **65833** : Pénalités et amendes fiscales

### Déductibilité fiscale
Conformément à l'article 11 du Code Général des Impôts (CGI), les amendes et pénalités, y compris celles pour déclaration tardive de TVA, ne sont pas déductibles du résultat fiscal. Cela signifie que vous ne pouvez pas déduire cette amende de vos revenus imposables.

### Résumé
- **Montant de l'amende** : 1 500 MAD
- **Compte à utiliser** : 65833 (Pénalités et amendes fiscales)
- **Déductibilité** : Non déductible fiscalement selon l'article 11 du CGI.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.6667 |
| Answer Correctness | 0.3567 |
| Answer Relevancy | 0.9289 |
| Context Precision | 0.5000 |
| Context Recall | 0.0000 |

---

### Question 28

**User input:**
> Dotation aux amortissements annuelle d'un véhicule de société acquis à 240 000 MAD HT. Durée d'amortissement : 5 ans, méthode linéaire.

**Expected (ground truth):**
```text
Débit: 6191 (Dotations d'exploitation aux amortissements des immobilisations corporelles) 48 000 MAD
Crédit: 2832 (Amortissements du matériel de transport) 48 000 MAD
```

**Agent response:**
```text
Pour calculer la dotation aux amortissements annuelle d'un véhicule de société acquis à 240 000 MAD HT avec une durée d'amortissement de 5 ans en utilisant la méthode linéaire, vous pouvez suivre la formule suivante :

### Formule de calcul de l'amortissement linéaire :
\[ \text{Amortissement annuel} = \frac{\text{Valeur d'entrée}}{\text{Durée d'amortissement}} \]

### Application :
- **Valeur d'entrée** : 240 000 MAD
- **Durée d'amortissement** : 5 ans

### Calcul :
\[ \text{Amortissement annuel} = \frac{240 000 \text{ MAD}}{5} = 48 000 \text{ MAD} \]

Ainsi, la dotation aux amortissements annuelle pour le véhicule de société sera de **48 000 MAD**.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.4696 |
| Answer Relevancy | 0.9493 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 29

**User input:**
> Quelles sont les principales priorités de la loi de finances 2026 au Maroc ?

**Expected (ground truth):**
```text
La loi de finances 2026 au Maroc s'articule autour de quatre priorités principales : le renforcement des acquis économiques pour consolider la position du Maroc parmi les pays émergents, le lancement de la nouvelle génération de programmes de développement territorial intégré, la poursuite de la consolidation de l'État social, et la préservation des équilibres des finances publiques tout en poursuivant les réformes structurelles majeures [citation:1][citation:7].
```

**Agent response:**
```text
Le projet de loi de finances pour l'année 2026 au Maroc se concentre sur plusieurs priorités clés, notamment :

1. **Consolidation des Acquis Économiques** : Le projet vise à renforcer la position du Maroc parmi les nations émergentes, en mettant l'accent sur des projets structurants et l'organisation d'événements sportifs mondiaux pour stimuler l'investissement.

2. **Développement des Infrastructures** : Un accent particulier est mis sur le développement d'infrastructures modernes dans les domaines des transports, de la logistique et des énergies. Cela inclut des investissements majeurs dans les aéroports, les lignes ferroviaires à grande vitesse, ainsi que le réseau autoroutier et portuaire.

3. **Amélioration du Marché du Travail** : Le projet de loi prévoit des mesures pour améliorer la situation du marché du travail, avec des prévisions de création d'emplois et une réduction du chômage à moyen terme.

4. **Réformes Budgétaires** : Il y a une volonté d'introduire des modifications à la loi organique relative à la loi de finances pour élargir son champ d'application, renforcer la soutenabilité des finances publiques et améliorer le rôle du Parlement dans la préparation et l'exécution de la loi de finances.

Ces priorités s'inscrivent dans un contexte économique international marqué par des incertitudes, et le gouvernement prévoit d'utiliser des emprunts et d'autres instruments financiers pour financer ces initiatives.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.3548 |
| Answer Relevancy | 0.9837 |
| Context Precision | 1.0000 |
| Context Recall | 0.5000 |

---

### Question 30

**User input:**
> Le sucre raffiné bénéficie-t-il d'un taux de TVA réduit au Maroc en 2026 ?

**Expected (ground truth):**
```text
Le sucre raffiné ou aggloméré fait l'objet d'une progression graduelle de son taux de TVA pour atteindre 10% en 2026 [citation:8].
```

**Agent response:**
```text
En 2026, le taux de TVA applicable au sucre raffiné au Maroc sera de 10%. Ce taux est le résultat d'une réduction progressive qui a commencé en 2024, avec un taux de 8% en 2024 et 9% en 2025.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.6604 |
| Answer Relevancy | 0.9474 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 31

**User input:**
> Retour de marchandises défectueuses au fournisseur : 2 000 MAD HT, TVA 20%. Avoir reçu du fournisseur.

**Expected (ground truth):**
```text
Débit: 4411 (Fournisseurs) 2 400 MAD
Crédit: 6111 (Achats de marchandises) 2 000 MAD
Crédit: 34551 (État - TVA récupérable sur immobilisations) 400 MAD
```

**Agent response:**
```text
Pour enregistrer le retour de marchandises défectueuses au fournisseur d'un montant de 2 000 MAD HT avec une TVA de 20%, vous pouvez utiliser les comptes suivants :

1. **Retour de marchandises** : Compte 6119 - Rabais, remises et ristournes obtenus sur achats de marchandises.
2. **TVA récupérable** : Compte 3455 - État - TVA récupérable.

### Écriture comptable :
- **Débit** :
  - Compte 6119 : 2 000 MAD (HT)
  - Compte 3455 : 400 MAD (TVA)

- **Crédit** :
  - Compte 4411 : 2 400 MAD (Total à créditer au fournisseur)

### Détails :
- Montant HT : 2 000 MAD
- Montant TVA (20%) : 400 MAD
- Montant total : 2 400 MAD

Cette écriture comptable reflète le retour des marchandises et la récupération de la TVA associée.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.5385 |
| Answer Correctness | 0.5753 |
| Answer Relevancy | 0.9348 |
| Context Precision | 0.8333 |
| Context Recall | 0.0000 |

---

### Question 32

**User input:**
> Quel est le montant alloué aux secteurs de l'éducation et de la santé dans la loi de finances 2026 au Maroc ?

**Expected (ground truth):**
```text
La loi de finances 2026 alloue un budget combiné de 140 milliards de dirhams aux secteurs de l'éducation et de la santé, soit une augmentation de 21 milliards de dirhams par rapport à 2025 [citation:1][citation:7].
```

**Agent response:**
```text
Dans le projet de loi de finances pour l'année 2026, les montants alloués aux secteurs de l'éducation et de la santé au Maroc sont les suivants :

- **Ministère de l'Éducation Nationale, du Préscolaire et des Sports** :
  - Personnel : 47,41 milliards de dirhams (MMDH)
  - Matériel et Dépenses Diverses : 31,94 MMDH

- **Ministère de la Santé et de la Protection Sociale** :
  - Personnel : 15,81 MMDH
  - Matériel et Dépenses Diverses : 7,77 MMDH

Ces investissements visent à améliorer les infrastructures et les services dans ces secteurs cruciaux pour le développement social et économique du pays.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.8571 |
| Answer Correctness | 0.2323 |
| Answer Relevancy | 0.9867 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 33

**User input:**
> Réception facture électricité Redal: 600 MAD TTC. Query: comptabiliser.

**Expected (ground truth):**
```text
Débit: 61251 (Achats d'eau, d'électricité) 526.32 MAD
Débit: 34552 (État - TVA récupérable sur charges 14%) 73.68 MAD
Crédit: 4411 (Fournisseurs) 600 MAD
```

**Agent response:**
```text
Pour comptabiliser la facture d'électricité de 600 MAD TTC reçue de Redal, vous devez suivre les étapes suivantes :

1. **Débit du compte d'achats** : Puisque l'électricité est considérée comme une fourniture non stockable, vous allez débiter le compte approprié pour les achats non stockés. Le compte à utiliser est le **6125** "Achats non stockés de matières et de fournitures".

2. **Crédit du compte fournisseur** : Vous allez créditer le compte fournisseur pour le montant total de la facture. Le compte à utiliser est le **4411** "Fournisseurs".

3. **Enregistrement de la TVA** : Si vous êtes assujetti à la TVA, vous devez également enregistrer la TVA récupérable. Le montant de la TVA dépendra du taux applicable (par exemple, 20% pour la plupart des biens et services). Pour une facture de 600 MAD TTC, si le taux de TVA est de 20%, la TVA serait de 100 MAD, et vous débiteriez le compte **3455** "État, TVA récupérable".

### Écritures comptables :

- **Débit** : 6125 - Achats non stockés de matières et de fournitures : 500 MAD (HT)
- **Débit** : 3455 - État, TVA récupérable : 100 MAD
- **Crédit** : 4411 - Fournisseurs : 600 MAD (TTC)

Ces écritures reflètent l'achat d'électricité et la reconnaissance de la dette envers le fournisseur.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.4085 |
| Answer Relevancy | 0.9486 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 34

**User input:**
> Quelle est la date limite de déclaration des revenus de capitaux mobiliers de source étrangère pour l'année 2025 ?

**Expected (ground truth):**
```text
La déclaration annuelle des revenus et profits de capitaux mobiliers de source étrangère non soumis à retenue à la source doit être souscrite avant le 1er avril de l'année suivante, soit avant le 1er avril 2026 pour les revenus perçus en 2025 [citation:11].
```

**Agent response:**
```text
La loi de finances pour l'année 2025 n'a pas spécifiquement mentionné la date limite de déclaration des revenus de capitaux mobiliers de source étrangère. Cependant, en général, la déclaration des revenus de capitaux mobiliers doit être faite dans les délais fixés par le Code Général des Impôts (CGI) marocain.

Pour des informations précises sur la date limite, il est recommandé de consulter le CGI ou de se référer aux instructions de l'administration fiscale marocaine. Si vous avez besoin d'informations spécifiques sur le CGI, je peux vous aider à les trouver.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2000 |
| Answer Correctness | 0.5639 |
| Answer Relevancy | 0.0000 |
| Context Precision | 1.0000 |
| Context Recall | 0.0000 |

---

### Question 35

**User input:**
> Quels sont les taux réduits de la TVA au Maroc et à quels produits s'appliquent-ils ?

**Expected (ground truth):**
```text
Au Maroc, les taux réduits de la TVA sont : 14% pour le transport domestique (hors train), 10% pour les services bancaires, l'hôtellerie et la restauration (hors alcool), les produits pétroliers, 7% pour l'eau et l'électricité publiques ainsi que les médicaments et produits pharmaceutiques [citation:2].
```

**Agent response:**
```text
Au Maroc, les taux réduits de la TVA s'appliquent à plusieurs produits et services. Voici un aperçu des principaux taux réduits et des produits concernés :

1. **Taux de 0%** :
   - Les ventes de certains produits alimentaires de base, comme le pain, le couscous, les semoules, et les farines servant à l'alimentation humaine.
   - Les produits de la pêche à l'état frais, congelés, entiers ou découpés.
   - Les laits et crèmes de lait frais, concentrés ou non, ainsi que le beurre dérivé du lait d’origine animale.
   - Les viandes fraîches ou congelées.

2. **Taux de 7%** :
   - Les ventes de livres, journaux, publications, et musique imprimée.
   - Les fournitures scolaires et les produits entrant dans leur composition.

3. **Taux de 10%** :
   - Les pompes à eau fonctionnant à l’énergie solaire ou à toute autre énergie renouvelable utilisées dans le secteur agricole.
   - Les tapis d'origine artisanale de production locale.

4. **Taux de 14%** :
   - Les biens, matériels, marchandises et services importés par les représentations de la Fédération Internationale de Football Association au Maroc.

5. **Taux de 20%** :
   - Ce taux s'applique généralement aux autres biens et services qui ne sont pas spécifiquement exonérés ou soumis à un taux réduit.

Ces taux peuvent être sujets à des modifications, et il est important de consulter le Code Général des Impôts pour des informations détaillées et à jour.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.8000 |
| Answer Correctness | 0.8655 |
| Answer Relevancy | 0.9793 |
| Context Precision | 1.0000 |
| Context Recall | 0.0000 |

---

### Question 36

**User input:**
> Paiement de l'acompte provisionnel IS du 31 mars : 25 000 MAD par virement bancaire.

**Expected (ground truth):**
```text
Débit: 3453 (État - Impôts sur les résultats) 25 000 MAD
Crédit: 5141 (Banque) 25 000 MAD
```

**Agent response:**
```text
Pour enregistrer le paiement de l'acompte provisionnel de l'IS de 25 000 MAD par virement bancaire, vous pouvez utiliser les comptes suivants :

1. **Pour le paiement de l'acompte provisionnel IS :**
   - **Compte 670** : Impôts sur les résultats (pour enregistrer l'impôt dû)
   
2. **Pour le virement bancaire :**
   - **Compte 514** : Banques (pour enregistrer la sortie de trésorerie)

### Écriture comptable :
- **Débit** : 670 (Impôts sur les résultats) 25 000 MAD
- **Crédit** : 514 (Banques) 25 000 MAD

Cela reflète le paiement de l'acompte provisionnel de l'IS par virement bancaire.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.4068 |
| Answer Relevancy | 0.9296 |
| Context Precision | 0.0000 |
| Context Recall | 1.0000 |

---

### Question 37

**User input:**
> Quel est le taux de TVA applicable à l'énergie électrique au Maroc ?

**Expected (ground truth):**
```text
Le taux de TVA appliqué à l'énergie électrique sera progressivement aligné sur le taux de 20% sur une période de trois ans [citation:8].
```

**Agent response:**
```text
Le taux de TVA applicable à l'énergie électrique au Maroc est de 14% jusqu'au 31 décembre 2023. À partir du 1er janvier 2024, ce taux sera augmenté à 16%, puis à 18% en 2025, et enfin à 20% en 2026.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.2265 |
| Answer Relevancy | 0.9551 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 38

**User input:**
> Relevé bancaire : commissions et frais de tenue de compte 200 MAD TTC. TVA 10% sur services bancaires.

**Expected (ground truth):**
```text
Débit: 6147 (Services bancaires) 181,82 MAD
Débit: 34552 (État - TVA récupérable sur charges 10%) 18,18 MAD
Crédit: 5141 (Banque) 200 MAD
```

**Agent response:**
```text
Pour enregistrer les commissions et frais de tenue de compte de 200 MAD TTC, vous pouvez utiliser le compte suivant :

- **Compte 61473** : Frais et commissions sur services bancaires

Concernant la TVA de 10% sur les services bancaires, elle est applicable selon le Code Général des Impôts (CGI) au Maroc. La TVA sur les services bancaires est généralement de 10%, ce qui est conforme à la réglementation en vigueur.

### Écriture comptable :
1. **Débit** : 61473 - Frais et commissions sur services bancaires : 200 MAD
2. **Crédit** : 44571 - TVA collectée : 18 MAD (10% de 200 MAD)
3. **Crédit** : 512 - Banque : 182 MAD (200 MAD - 18 MAD)

Cela vous permettra de comptabiliser correctement les frais bancaires et la TVA associée.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.3750 |
| Answer Correctness | 0.7268 |
| Answer Relevancy | 0.8908 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 39

**User input:**
> Quel est le taux normal de la TVA au Maroc en 2026 ?

**Expected (ground truth):**
```text
Le taux normal de la TVA au Maroc en 2026 est de 20% [citation:2][citation:20].
```

**Agent response:**
```text
En 2026, le taux normal de la TVA au Maroc sera de 20%. Ce taux est le résultat d'une augmentation progressive qui a commencé en 2024, avec un taux de 11%, suivi de 15% en 2025.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.5399 |
| Answer Relevancy | 0.9920 |
| Context Precision | 1.0000 |
| Context Recall | 0.5000 |

---

### Question 40

**User input:**
> Paiement loyer bureau: 4000 MAD par chèque. Query: journaliser.

**Expected (ground truth):**
```text
Débit: 61311 (Locations de bâtiments) 4000 MAD
Crédit: 5141 (Banque) 4000 MAD
```

**Agent response:**
```text
Pour journaliser le paiement du loyer de bureau de 4000 MAD par chèque, vous pouvez utiliser les comptes suivants :

1. **Compte de charges pour le loyer** : 6131 - Locations et charges locatives
2. **Compte bancaire** : 514 - Banques

### Écriture comptable :
- **Débit** : 6131 - Locations et charges locatives : 4000 MAD
- **Crédit** : 514 - Banques : 4000 MAD

### Journalisation :
```
Date : [Date du paiement]
----------------------------------------
|  Compte         |  Débit   |  Crédit  |
|-----------------|----------|----------|
|  6131           |  4000    |          |
|  514            |          |  4000    |
----------------------------------------
```

Assurez-vous de remplacer `[Date du paiement]` par la date réelle du paiement.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2000 |
| Answer Correctness | 0.5414 |
| Answer Relevancy | 0.9374 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 41

**User input:**
> Quel est le taux de l'IS au Maroc pour une PME dont le bénéfice net est de 500 000 MAD en 2026 ?

**Expected (ground truth):**
```text
Pour une PME dont le bénéfice net fiscal est inférieur à 100 millions de MAD, le taux de l'IS est unifié à 20% à compter de 2026 [citation:16][citation:10].
```

**Agent response:**
```text
Pour l'année 2026, le taux de l'impôt sur les sociétés (IS) au Maroc pour une PME dont le bénéfice net est de 500 000 MAD est de **20%**. Ce taux s'applique aux sociétés dont le bénéfice net est compris entre 300 001 MAD et 1 000 000 MAD.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.5000 |
| Answer Correctness | 0.6102 |
| Answer Relevancy | 0.9718 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 42

**User input:**
> Quel est le taux de TVA applicable aux médicaments et produits pharmaceutiques au Maroc ?

**Expected (ground truth):**
```text
Les médicaments et produits pharmaceutiques bénéficient d'un taux de TVA réduit de 7% [citation:2].
```

**Agent response:**
```text
Au Maroc, le taux de TVA applicable aux médicaments et produits pharmaceutiques est de **0%**. Cela signifie que ces produits sont exonérés de la taxe sur la valeur ajoutée.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.2251 |
| Answer Relevancy | 0.9987 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 43

**User input:**
> Plein de carburant : 400 MAD TTC, TVA 20%. Carte bancaire professionnelle.

**Expected (ground truth):**
```text
Débit: 6142 (Transports) 333,33 MAD
Débit: 34552 (État - TVA récupérable sur charges 20%) 66,67 MAD
Crédit: 5141 (Banque) 400 MAD
```

**Agent response:**
```text
Pour comptabiliser l'achat de carburant de 400 MAD TTC avec une TVA de 20%, voici les informations nécessaires :

1. **Montant HT (Hors Taxes)** :
   - Montant TTC = 400 MAD
   - Taux de TVA = 20%
   - Montant HT = Montant TTC / (1 + Taux de TVA) = 400 / 1.20 = 333.33 MAD

2. **Montant de la TVA** :
   - TVA = Montant TTC - Montant HT = 400 - 333.33 = 66.67 MAD

### Comptabilisation

- **Compte de charges pour le carburant** : 61223 (Achats de combustibles)
- **Compte de TVA récupérable** : 3455 (État - TVA récupérable)

### Écriture comptable

- **Débit** :
  - 61223 (Achats de combustibles) : 333.33 MAD
  - 3455 (État - TVA récupérable) : 66.67 MAD

- **Crédit** :
  - 5121 (Banque) : 400 MAD (pour le paiement par carte bancaire professionnelle)

### Résumé des comptes utilisés
- **Carburant (Achats de combustibles)** : 61223
- **TVA récupérable** : 3455
- **Banque** : 5121

Assurez-vous de bien enregistrer ces écritures dans votre comptabilité pour respecter les normes comptables marocaines.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.2217 |
| Answer Relevancy | 0.9023 |
| Context Precision | 0.0000 |
| Context Recall | 0.0000 |

---

### Question 44

**User input:**
> Échéance mensuelle d'un emprunt bancaire : capital 5 000 MAD, intérêts 500 MAD. Prélèvement automatique.

**Expected (ground truth):**
```text
Débit: 1481 (Emprunts auprès des établissements de crédit) 5 000 MAD
Débit: 6311 (Intérêts des emprunts) 500 MAD
Crédit: 5141 (Banque) 5 500 MAD
```

**Agent response:**
```text
Pour comptabiliser l'échéance mensuelle d'un emprunt bancaire de 5 000 MAD avec des intérêts de 500 MAD, vous pouvez utiliser les comptes suivants :

1. **Pour le capital de l'emprunt :**
   - **Compte 0561** : Emprunts non encore encaissés (pour enregistrer le montant de l'emprunt)
   
2. **Pour les intérêts de l'emprunt :**
   - **Compte 63111** : Intérêts des emprunts (pour enregistrer les intérêts à payer)

### Écriture comptable :
- **Débit** : Compte 63111 (Intérêts des emprunts) : 500 MAD
- **Débit** : Compte 0561 (Emprunts non encore encaissés) : 5 000 MAD
- **Crédit** : Compte 5141 (Banque) ou Compte 5161 (Caisse) : 5 500 MAD (pour le paiement total)

Cette écriture reflète le paiement de l'échéance de l'emprunt par prélèvement automatique.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.1250 |
| Answer Correctness | 0.8310 |
| Answer Relevancy | 0.9232 |
| Context Precision | 0.0000 |
| Context Recall | 1.0000 |

---

### Question 45

**User input:**
> Achat d'un ordinateur portable pour le bureau : 10 000 MAD HT, TVA 20%. Paiement par chèque. Amortissement linéaire sur 3 ans.

**Expected (ground truth):**
```text
Débit: 2351 (Matériel informatique) 10 000 MAD
Débit: 34551 (État - TVA récupérable sur immobilisations) 2 000 MAD
Crédit: 5141 (Banque) 12 000 MAD
```

**Agent response:**
```text
Pour l'achat d'un ordinateur portable pour le bureau, voici les informations comptables nécessaires :

1. **Coût d'achat** : 10 000 MAD HT
2. **TVA (20%)** : 2 000 MAD
3. **Total TTC** : 12 000 MAD
4. **Mode de paiement** : par chèque

### Comptes à utiliser :

- **Compte d'immobilisation** : 2355 (Matériel informatique)
- **Compte de TVA récupérable** : 3455 (TVA récupérable)
- **Compte de banque** : 5141 (Banques)

### Écritures comptables :

1. **À l'achat de l'ordinateur** :
   - Débit 2355 : 10 000 MAD
   - Débit 3455 : 2 000 MAD
   - Crédit 5141 : 12 000 MAD

2. **Amortissement** :
   - Amortissement linéaire sur 3 ans, soit 3 333,33 MAD par an.
   - Compte d'amortissement : 61935 (D.E.A. des mobiliers, matériels de bureau et aménagements divers)

### Écriture d'amortissement annuelle :
- Débit 61935 : 3 333,33 MAD
- Crédit 28355 : 3 333,33 MAD

Ces écritures vous permettront de comptabiliser l'achat et l'amortissement de l'ordinateur portable dans vos livres comptables.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2667 |
| Answer Correctness | 0.7021 |
| Answer Relevancy | 0.8775 |
| Context Precision | 1.0000 |
| Context Recall | 0.6667 |

---

### Question 46

**User input:**
> Le Maroc a-t-il retrouvé sa notation « investment grade » en 2025 ?

**Expected (ground truth):**
```text
Oui, le Maroc a retrouvé sa notation « investment grade » de l'agence de notation américaine Standard & Poor's en septembre 2025 [citation:19].
```

**Agent response:**
```text
Oui, le Maroc a retrouvé sa notation « investment grade » en 2025. L'agence de notation Standard & Poor's a rehaussé la note souveraine du Maroc à BBB-/A-3, ce qui lui permet de regagner ce statut.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.8867 |
| Answer Relevancy | 0.9560 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 47

**User input:**
> Quel est le taux de l'IS pour les sociétés dont le bénéfice net fiscal est supérieur ou égal à 100 millions de MAD en 2026 ?

**Expected (ground truth):**
```text
Pour les sociétés non financières dont le bénéfice net fiscal est égal ou supérieur à 100 millions de MAD, le taux de l'IS est de 35% en 2026 [citation:16][citation:4].
```

**Agent response:**
```text
Pour l'année 2026, le taux de l'impôt sur les sociétés (IS) pour les sociétés dont le bénéfice net fiscal est supérieur ou égal à 100 millions de MAD est de **35%**.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.5000 |
| Answer Correctness | 0.9916 |
| Answer Relevancy | 0.9816 |
| Context Precision | 1.0000 |
| Context Recall | 1.0000 |

---

### Question 48

**User input:**
> Les opérations bancaires sont-elles soumises à la TVA au Maroc et à quel taux ?

**Expected (ground truth):**
```text
Oui, les services bancaires sont soumis à la TVA au taux réduit de 10% [citation:2].
```

**Agent response:**
```text
Les opérations bancaires au Maroc sont généralement exonérées de la taxe sur la valeur ajoutée (TVA). Cependant, il existe des cas spécifiques où certaines opérations peuvent être soumises à la TVA, notamment les intérêts servis par les établissements de crédit, qui sont perçus par voie de retenue à la source.

En ce qui concerne le taux de TVA applicable, il n'est pas spécifiquement mentionné pour les opérations bancaires dans le Code Général des Impôts, car la plupart de ces opérations sont exonérées. Pour les opérations qui pourraient être soumises à la TVA, le taux standard de TVA au Maroc est de 20%.

Si vous avez besoin d'informations plus précises sur un type d'opération bancaire spécifique, n'hésitez pas à demander.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.5000 |
| Answer Correctness | 0.7821 |
| Answer Relevancy | 0.0000 |
| Context Precision | 1.0000 |
| Context Recall | 0.0000 |

---

### Question 49

**User input:**
> Paiement des cotisations CNSS du mois : part patronale 4 500 MAD, part salariale 2 250 MAD. Virement bancaire.

**Expected (ground truth):**
```text
Débit: 4441 (Caisse Nationale de Sécurité Sociale) 6 750 MAD
Crédit: 5141 (Banque) 6 750 MAD
```

**Agent response:**
```text
Pour comptabiliser le paiement des cotisations CNSS du mois, vous pouvez utiliser les comptes suivants :

1. **Part patronale (4 500 MAD)** :
   - Compte à utiliser : **61741** (Cotisations de sécurité sociale)

2. **Part salariale (2 250 MAD)** :
   - Compte à utiliser : **4432** (Rémunérations dues au personnel)

3. **Virement bancaire** :
   - Compte à utiliser : **5141** (Banques)

### Écriture comptable :
- **Débit** : 61741 (Cotisations de sécurité sociale) : 4 500 MAD
- **Débit** : 4432 (Rémunérations dues au personnel) : 2 250 MAD
- **Crédit** : 5141 (Banques) : 6 750 MAD

Cela reflète le paiement total des cotisations CNSS, incluant la part patronale et la part salariale, par virement bancaire.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.4364 |
| Answer Relevancy | 0.8734 |
| Context Precision | 0.0000 |
| Context Recall | 1.0000 |

---

### Question 50

**User input:**
> Facture Facebook Ads: 100 USD pour publicité. Query: comptabilisation.

**Expected (ground truth):**
```text
Débit: 61441 (Annonces et insertions) 1000 MAD
Crédit: 5141 (Banque) 1000 MAD (Facture étrangère non soumise à la TVA marocaine)
```

**Agent response:**
```text
Pour comptabiliser une facture de publicité Facebook Ads d'un montant de 100 USD, voici les étapes à suivre :

1. **Enregistrement de la facture** : Lorsque vous recevez la facture, vous devez débiter le compte d'achats correspondant et créditer le compte fournisseur.

2. **Comptes à utiliser** :
   - Débit du compte d'achats (par exemple, compte 6144 "Publicité").
   - Crédit du compte fournisseur (par exemple, compte 4411 "Fournisseurs").

3. **Écriture comptable** :
   - Débit 6144 Publicité : 100 USD
   - Crédit 4411 Fournisseurs : 100 USD

4. **TVA** : Si la facture inclut de la TVA récupérable, vous devez également comptabiliser la TVA. Par exemple, si la TVA est de 20%, vous devez :
   - Débit du compte 3455 "TVA récupérable" : 20 USD
   - Crédit du compte 4411 "Fournisseurs" : 20 USD

5. **Écriture comptable avec TVA** :
   - Débit 6144 Publicité : 100 USD
   - Débit 3455 TVA récupérable : 20 USD
   - Crédit 4411 Fournisseurs : 120 USD

Assurez-vous de vérifier les taux de change si vous devez convertir les USD en dirhams marocains pour votre comptabilité.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.2000 |
| Answer Correctness | 0.2068 |
| Answer Relevancy | 0.9350 |
| Context Precision | 1.0000 |
| Context Recall | 0.0000 |

---

### Question 51

**User input:**
> Facture d'hébergement touristique : 5 000 MAD HT. TVA au taux réduit de 10%. Client règle en espèces.

**Expected (ground truth):**
```text
Débit: 5161 (Caisse) 5 500 MAD
Crédit: 7121 (Ventes de services au Maroc) 5 000 MAD
Crédit: 4455 (État - TVA facturée) 500 MAD
```

**Agent response:**
```text
Pour comptabiliser la facture d'hébergement touristique de 5 000 MAD HT avec une TVA au taux réduit de 10%, voici les étapes et les comptes à utiliser :

1. **Montant HT** : 5 000 MAD
2. **TVA (10%)** : 5 000 MAD * 10% = 500 MAD
3. **Montant TTC** : 5 000 MAD + 500 MAD = 5 500 MAD

### Comptes à utiliser :
- **Ventes d'hébergement touristique** : Compte **71243** (Prestations de services)
- **TVA collectée** : Compte **4455** (TVA facturée)
- **Caisse** : Compte **5161** (Caisse)

### Écriture comptable :
- **Débit** : Compte 5161 (Caisse) : 5 500 MAD
- **Crédit** : Compte 71243 (Prestations de services) : 5 000 MAD
- **Crédit** : Compte 4455 (TVA facturée) : 500 MAD

Cette écriture reflète la vente de services d'hébergement, la collecte de la TVA, et le paiement en espèces par le client.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 1.0000 |
| Answer Correctness | 0.9103 |
| Answer Relevancy | 0.9230 |
| Context Precision | 0.3333 |
| Context Recall | 0.6667 |

---

### Question 52

**User input:**
> Vente de services à un client local: 10000 MAD HT. Query: passer l'écriture.

**Expected (ground truth):**
```text
Débit: 3421 (Clients) 12000 MAD
Crédit: 71241 (Ventes de services produits au Maroc) 10000 MAD
Crédit: 4455 (État - TVA facturée 20%) 2000 MAD
```

**Agent response:**
```text
Pour passer l'écriture de la vente de services à un client local pour un montant de 10,000 MAD HT, vous devez enregistrer les écritures comptables suivantes :

1. **Vente de services** (Compte 71243) : 10,000 MAD
2. **TVA collectée** (Compte 4455) : 20% de 10,000 MAD = 2,000 MAD
3. **Clients** (Compte 342) : Total à recevoir = 10,000 MAD + 2,000 MAD = 12,000 MAD

### Écriture comptable :

- **Débit** : Compte 342 (Clients) : 12,000 MAD
- **Crédit** : Compte 71243 (Prestations de services) : 10,000 MAD
- **Crédit** : Compte 4455 (TVA facturée) : 2,000 MAD

### Résumé de l'écriture :
- **Débit** : 342 Clients : 12,000 MAD
- **Crédit** : 71243 Prestations de services : 10,000 MAD
- **Crédit** : 4455 TVA facturée : 2,000 MAD

Cela enregistre la vente de services et la TVA associée à cette vente.
```

| Metric | Score |
| :--- | :--- |
| Faithfulness | 0.0000 |
| Answer Correctness | 0.6216 |
| Answer Relevancy | 0.8413 |
| Context Precision | 1.0000 |
| Context Recall | 0.3333 |

---
