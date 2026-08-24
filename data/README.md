# Data Sources

All data files can be found at the sources listed below. No actual data should be stored or shared in this folder.

The following datasets are required to reproduce the geodemographic classification. Each must be downloaded separately from its original source. Links and access requirements are provided below.

---

## Required Datasets

### 1. PDV Consumer Lifestyles Survey (microsimulation input)
- **File(s):** Used internally to produce `lsoa_synthetic_population.csv`
- **Source:** [Geographic Data Service (GeoDS) — PDV Consumer Lifestyle Surveys](https://data.geods.ac.uk/)
- **Access:** Secure dataset — requires institutional `.ac.uk` email, ethics approval, Safe Researcher Training (SRT), and a signed data licence. Access is via the GeoDS Trusted Research Environment (TRE). Application process typically takes 2-4 months.
- **Note:** This dataset contains over 15 million responses (2001-2023) across 515 variables related to consumer shopping, lifestyle and financial behaviour. Contact the corresponding author for further guidance.

---

### 2. Census 2021 — LSOA-level variables
- **File(s):** `census_2021_lsoa.csv`
- **Source:** [ONS Census 2021 — Nomis Custom Download Tool](https://www.nomisweb.co.uk/sources/census_2021)
- **Coverage:** England and Wales, LSOA level
- **Licence:** Open Government Licence v3.0

---

### 3. LSOA 2021 Boundary Shapefile
- **File(s):** `Lower_layer_Super_Output_Areas_(December_2021)_Boundaries_EW_BFC_(V10).*` (`.shp`, `.dbf`, `.prj`, `.shx`, `.cpg`)
- **Source:** [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bfc-v10/about)
- **Licence:** Open Government Licence v3.0

---

### 4. LSOA 2011 to 2021 Best Fit Lookup
- **File(s):** `LSOA_(2011)_to_LSOA_(2021)_to_Local_Authority_District_(2022)_Best_Fit_Lookup_for_EW_(V2).csv`
- **Source:** [ONS Open Geography Portal — Lookups](https://geoportal.statistics.gov.uk/datasets/ons::lsoa-2011-to-lsoa-2021-to-local-authority-district-2022-best-fit-lookup-for-ew-v2/about)
- **Used for:** Harmonising LSOA boundaries from 2011 to 2021, following Harris (2022)
- **Licence:** Open Government Licence v3.0

---

### 5. Rural Urban Classification (RUC) 2011
- **File(s):** Used to derive urbanity category per LSOA
- **Source:** [ONS Open Geography Portal — Rural Urban Classification 2011 of LSOAs in EW](https://geoportal.statistics.gov.uk/datasets/ons::rural-urban-classification-2011-of-lsoas-in-ew/about)
- **Note:** Applies 2011 LSOA boundaries; requires harmonisation with 2021 boundaries before use
- **Licence:** Open Government Licence v3.0

---

### 6. Great Britain Accessibility Indicators (GBAI) 2023
- **File(s):** `accessibility_indicators_gbai.csv`, `supermarket_accessibility_lsoa.csv`
- **Source:** [UBDC Data Hub — Accessibility Indicators](https://data.ubdc.ac.uk/dataset/accessibility-indicators) · also available via [Zenodo](https://zenodo.org)
- **Description:** Provides small-area accessibility indicators (distances from LSOA centroids to urban centres, supermarkets, and other services) for public transport, walking, and cycling modes
- **Reference:** UBDC (2023). *Great Britain Accessibility Indicators 2023 (AI23)*. Urban Big Data Centre. doi: [10.31235/osf.io/qb9j4](https://doi.org/10.31235/osf.io/qb9j4)

---

### 7. Internet User Classification (IUC) 2018
- **File(s):** `internet_user_classification_lsoa.csv`
- **Source:** [Consumer Data Research Centre — Internet User Classification](https://data.cdrc.ac.uk/dataset/internet-user-classification)
- **Access:** Requires free CDRC account registration
- **Reference:** Singleton, A. et al. (2020). Licence: Open Government Licence

---

## File-to-Notebook Mapping

| File | Used in |
|------|---------|
| PDV data → `lsoa_synthetic_population.csv` | `03_clustering_analysis.ipynb` |
| `census_2021_lsoa.csv` | `02_data_synthesis.ipynb` |
| `internet_user_classification_lsoa.csv` | `02_data_synthesis.ipynb` |
| `accessibility_indicators_gbai.csv`, `supermarket_accessibility_lsoa.csv` | `02_data_synthesis.ipynb` |
| `Lower_layer_Super_Output_Areas_*` | `02_data_synthesis.ipynb`, `scripts/data_harmonization.Rmd` |
| `LSOA_(2011)_to_LSOA_(2021)_*` | `scripts/data_harmonization.Rmd` |
| Rural Urban Classification 2011 | `01_variable_selection.ipynb`, `02_data_synthesis.ipynb` |
| `lsoa_cluster_assignments.csv` | Output of `03_clustering_analysis.ipynb` |
| `lsoa_subcluster_assignments.csv` | Output of `03_clustering_analysis.ipynb` |
