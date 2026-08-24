# Data Sources

This directory holds source data required to reproduce the geodemographic classification. **All data files are excluded from version control** due to file size. Download or obtain the files listed below before running the pipeline.

---

## Required Files

### 1. Census 2021 — LSOA-level variables
- **File:** `census.csv`
- **Source:** [ONS Census 2021 — Custom Download Tool](https://www.nomisweb.co.uk/sources/census_2021)
- **Coverage:** England and Wales, LSOA level

### 2. LSOA 2021 Boundary Shapefile
- **Files:** `Lower_layer_Super_Output_Areas_(December_2021)_Boundaries_EW_BFC_(V10).*`
- **Source:** [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bfc-v10/about)
- **Format:** Shapefile (`.shp`, `.dbf`, `.prj`, `.shx`, `.cpg`)

### 3. LSOA 2011→2021 Best Fit Lookup
- **File:** `LSOA_(2011)_to_LSOA_(2021)_to_Local_Authority_District_(2022)_Best_Fit_Lookup_for_EW_(V2).csv`
- **Source:** [ONS Open Geography Portal — Lookups](https://geoportal.statistics.gov.uk/datasets/ons::lsoa-2011-to-lsoa-2021-to-local-authority-district-2022-best-fit-lookup-for-ew-v2/about)

### 4. Internet User Classification (IUC)
- **File:** `IUC_grouped.csv` / `iuc_new.csv`
- **Source:** [Consumer Data Research Centre — IUC 2018](https://data.cdrc.ac.uk/dataset/internet-user-classification)
- **Note:** Requires free CDRC account registration.

### 5. DSH / Supermarket Accessibility Data
- **File:** `dsh_data.csv`, `supermarket_ready.csv`
- **Source:** Derived from OS Points of Interest and Ordnance Survey datasets. See paper methodology (Section 3) for derivation details.

### 6. Agent-Based Model Variable List
- **File:** `Agent-Based_Model_Variables.csv`
- **Description:** Mapping of PDV Consumer Lifestyle Survey variables used in microsimulation. See paper Table 1 for full variable descriptions.

### 7. PDV Consumer Lifestyle Survey (microsimulation input)
- **Note:** The PDV Consumer Lifestyle Survey is **proprietary** and cannot be redistributed. The final synthetic population output (`full_set.csv`) is the direct input to the clustering pipeline. Contact the corresponding author for access enquiries.

---

## File Naming Summary

| Filename | Step Used |
|----------|-----------|
| `census.csv` | `02_data_synthesis.ipynb` |
| `IUC_grouped.csv` | `02_data_synthesis.ipynb` |
| `dsh_data.csv` | `02_data_synthesis.ipynb` |
| `supermarket_ready.csv` | `02_data_synthesis.ipynb` |
| `full_set.csv` | `03_clustering_analysis.ipynb` |
| `Lower_layer_Super_Output_Areas_*` | `02_data_synthesis.ipynb`, `scripts/data_harmonization.Rmd` |
| `LSOA_(2011)_to_LSOA_(2021)_*` | `scripts/data_harmonization.Rmd` |
| `all_done.csv` | Output of `03_clustering_analysis.ipynb` |
