# Open Geodemographic Classification of Consumer Behaviour (England & Wales)

[![DOI](https://img.shields.io/badge/DOI-10.1108%2FIJRDM--06--2025--0436-blue)](https://doi.org/10.1108/IJRDM-06-2025-0436)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Published paper:** Balog, Á., Dolega, L., Mahabir, R., Ballantyne, P. & Williamson, P. (2026). Developing an open, national-level, small-area geodemographic classification of consumer behaviour. *International Journal of Retail & Distribution Management*, 1–16. https://doi.org/10.1108/IJRDM-06-2025-0436

## Overview
Consumer shopping behaviours have become increasingly dynamic, shaped by technological advancements and shifting lifestyle priorities. The rise of digital platforms and personalised recommendations has empowered consumers to tailor their retail experiences across channels. Furthermore, sustainability, the cost-of-living crisis, and flexible working have further influenced these behaviours, with shoppers increasingly seeking convenience, eco-friendly options, value-for-money, and delivery services.

Therefore, consumer behaviour, and the way in which it is shifting, is becoming increasingly complex and multi-dimensional. Understanding these behavioural shifts is essential for urban planners and retail managers for interventions, ensuring that physical retail spaces remain competitive in this landscape.

## Purpose
The purpose of this study is to develop an **openly available, national-level, small-area geodemographic classification dataset** that captures the multidimensional nature of consumer behaviour across England and Wales.

Unlike earlier classifications, which have largely centred on socioeconomic structure, this study advances a theoretically grounded framework in which demographic, behavioural, digital, and accessibility dimensions are treated as co-determining drivers of consumer behaviour. This approach offers a refined conceptual lens for understanding how multiple domains collectively shape contemporary consumption patterns.

## Methodology
The classification is developed at the **Lower Super Output Area (LSOA)** level and is underpinned by complex analytical components:
- **Microsimulation**: Based on a proprietary consumer behavioural survey (PDV Consumer Lifestyle Survey).
- **Demographic Factors**: 2021 Census-based socioeconomic attributes.
- **Accessibility Measures**: Spatial context and physical accessibility.
- **Digital Capability**: Online usage patterns and digital accessibility.

Eight analytical domains were derived from a conceptual framework: household composition, financial resilience, lifestyle, mobility, online engagement, social networks, shopping patterns, and socioeconomic status.

Clustering yields **4 primary clusters** and **9 subclusters**:

| Cluster | Label | Subclusters |
|---------|-------|-------------|
| 1 | Affluent Professional Consumers | 1.1 Affluent Suburban Professionals · 1.2 Urban Digital Millennials |
| 2 | Budget-Conscious Young Urbanites | 2.1 Value-Driven Young Spenders · 2.2 Price-Sensitive Digital Shoppers |
| 3 | Family-Oriented Suburban Consumers | 3.1 Established Families · 3.2 Suburban Empty Nesters · 3.3 High-End Consumers |
| 4 | Traditional Rural Consumers | 4.1 Affluent Rural Empty Nester Consumers · 4.2 Rural Retirees |

## Repository Structure
```
├── notebooks/          # Sequential Jupyter notebooks (run in order)
│   ├── 01_variable_selection.ipynb
│   ├── 02_data_synthesis.ipynb
│   ├── 03_clustering_analysis.ipynb
│   ├── 04_silhouette_validation.ipynb
│   └── 05_silhouette_revision_stability.ipynb
├── scripts/            # Supporting analysis scripts
│   ├── data_harmonization.Rmd   # LSOA 2011→2021 boundary harmonization (R)
│   ├── parameter_sweep.py       # Multi-algorithm parameter sweep (K=3,4,5)
│   └── robustness_comparison.py # K-Means vs PAM vs FGWC comparison
├── data/               # Source data (not tracked — see data/README.md)
├── results/figures/    # Publication figures
├── docs/               # Manuscript and supplementary documentation
├── process_geodemographics.py   # Post-classification pipeline (ABM integration)
├── subcluster_priors.py         # Subcluster z-score priors for ABM
├── requirements.txt    # Python dependencies
└── CITATION.cff        # Machine-readable citation metadata
```

## Installation

```bash
git clone https://github.com/balogakos/Geodemographic-Classification-of-Consumer-Behaviour.git
cd Geodemographic-Classification-of-Consumer-Behaviour
pip install -r requirements.txt
```

For the R data harmonization script, install the required packages:
```r
install.packages(c("data.table", "tidyverse", "stringr", "sf", "RANN"))
```

## How to Use
1. **Prepare Data**: Follow `data/README.md` for data sources and download instructions.
2. **Harmonize Boundaries**: Run `scripts/data_harmonization.Rmd` to align LSOA 2011→2021.
3. **Run Pipeline**: Follow the numbered notebooks in `notebooks/` to reproduce the classification.
4. **Validate**: Use `scripts/robustness_comparison.py` or `scripts/parameter_sweep.py` to evaluate clustering performance against PAM, FGWC, GMM, and spatially constrained methods.

## Classification Outputs
The final classification (`lsoa_subcluster_assignments.csv`) maps each LSOA in England and Wales to one of 4 primary clusters and 9 subclusters. Spatial outputs are provided as shapefiles.

## Citation
If you use this code or classification in your research, please cite:

```bibtex
@article{balog2026geodemographic,
  author  = {Balog, {\'A}kos and Dolega, Les and Mahabir, Ron and Ballantyne, Patrick and Williamson, Paul},
  title   = {Developing an open, national-level, small-area geodemographic classification of consumer behaviour},
  journal = {International Journal of Retail \& Distribution Management},
  year    = {2026},
  pages   = {1--16},
  doi     = {10.1108/IJRDM-06-2025-0436},
  url     = {https://doi.org/10.1108/IJRDM-06-2025-0436}
}
```

## Licence
This software is released under the [MIT Licence](LICENSE).
