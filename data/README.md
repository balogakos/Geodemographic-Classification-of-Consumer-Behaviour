# Data Sources

> ⚠️ **All data files can be found at the sources listed below. No actual data should be stored or shared in this folder.**

The following datasets are required to reproduce the geodemographic classification. Each must be downloaded separately from its original source. Links and access requirements are provided below.

---

## Required Datasets

### 1. PDV Consumer Lifestyles Survey (microsimulation input)
- **File(s):** Used internally to produce `full_set.csv` (synthetic population output)
- **Source:** [Geographic Data Service (GeoDS) — PDV Consumer Lifestyle Surveys](https://data.geods.ac.uk/)
- **Access:** ⛔ **Secure dataset** — requires institutional `.ac.uk` email, ethics approval, Safe Researcher Training (SRT), and a signed data licence. Access is via the GeoDS Trusted Research Environment (TRE). Application process typically takes 2–4 months.
- **Note:** This dataset contains over 15 million responses (2001–2023) across 515 variables related to consumer shopping, lifestyle and financial behaviour. The synthetic population output (`full_set.csv`) is the direct input to the clustering pipeline. Contact the corresponding author for further guidance.

---

### 2. Census 2021 — LSOA-level variables
- **File(s):** `census.csv`
- **Source:** [ONS Census 2021 — Nomis Custom Download Tool](https://www.nomisweb.co.uk/sources/census_2021)
- **Coverage:** England and Wales, LSOA level (90 variables)
- **Licence:** Open Government Licence v3.0

---

### 3. LSOA 2021 Boundary Shapefile
- **File(s):** `Lower_layer_Super_Output_Areas_(December_2021)_Boundaries_EW_BFC_(V10).*` (`.shp`, `.dbf`, `.prj`, `.shx`, `.cpg`)
- **Source:** [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bfc-v10/about)
- **Licence:** Open Government Licence v3.0

---

### 4. LSOA 2011→2021 Best Fit Lookup
- **File(s):** `LSOA_(2011)_to_LSOA_(2021)_to_Local_Authority_District_(2022)_Best_Fit_Lookup_for_EW_(V2).csv`
- **Source:** [ONS Open Geography Portal — Lookups](https://geoportal.statistics.gov.uk/datasets/ons::lsoa-2011-to-lsoa-2021-to-local-authority-district-2022-best-fit-lookup-for-ew-v2/about)
- **Used for:** Harmonising LSOA boundaries from 2011 to 2021 (35,753 → 35,799 units), following Harris (2022)
- **Licence:** Open Government Licence v3.0

---

### 5. Rural Urban Classification (RUC) 2011
- **File(s):** Used to derive urbanity category per LSOA
- **Source:** [ONS Open Geography Portal — RUC 2011 of LSOAs in EW](https://geoportal.statistics.gov.uk/datasets/ons::rural-urban-classification-2011-of-lsoas-in-ew/about)
- **Note:** Applies 2011 LSOA boundaries; requires harmonisation with 2021 boundaries before use
- **Licence:** Open Government Licence v3.0

---

### 6. Great Britain Accessibility Indicators (GBAI) 2023
- **File(s):** `dsh_data.csv`, `supermarket_ready.csv`
- **Source:** [UBDC Data Hub — Accessibility Indicators](https://data.ubdc.ac.uk/dataset/accessibility-indicators) · also available via [Zenodo](https://zenodo.org)
- **Description:** Provides small-area accessibility indicators (distances from LSOA centroids to urban centres, supermarkets, and other services) for public transport, walking, and cycling modes
- **Reference:** UBDC (2023). *Great Britain Accessibility Indicators 2023 (AI23)*. Urban Big Data Centre. doi: [10.31235/osf.io/qb9j4](https://doi.org/10.31235/osf.io/qb9j4)

---

### 7. Internet User Classification (IUC) 2018
- **File(s):** `IUC_grouped.csv`, `iuc_new.csv`
- **Source:** [Consumer Data Research Centre — Internet User Classification](https://data.cdrc.ac.uk/dataset/internet-user-classification)
- **Access:** Requires free CDRC account registration
- **Reference:** Singleton, A. et al. (2020). *The Internal Structure of Cities*. Licence: OGL

---

### 8. Agent-Based Model Variable List
- **File(s):** `Agent-Based_Model_Variables.csv`
- **Description:** Researcher-compiled mapping of PDV Consumer Lifestyle Survey variables selected for microsimulation input (52 variables across 8 analytical domains). See paper Table 1 for full variable descriptions and selection rationale.

---

## File-to-Notebook Mapping

| File | Used in |
|------|---------|
| PDV → `full_set.csv` | `03_clustering_analysis.ipynb` |
| `census.csv` | `02_data_synthesis.ipynb` |
| `IUC_grouped.csv` | `02_data_synthesis.ipynb` |
| `dsh_data.csv`, `supermarket_ready.csv` | `02_data_synthesis.ipynb` |
| `Lower_layer_Super_Output_Areas_*` | `02_data_synthesis.ipynb`, `scripts/data_harmonization.Rmd` |
| `LSOA_(2011)_to_LSOA_(2021)_*` | `scripts/data_harmonization.Rmd` |
| RUC 2011 | `01_variable_selection.ipynb`, `02_data_synthesis.ipynb` |
| `all_done.csv` | Output of `03_clustering_analysis.ipynb` |
