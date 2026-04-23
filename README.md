# Open Geodemographic Classification of Consumer Behaviour (England & Wales)

## Overview
Consumer shopping behaviours have become increasingly dynamic, shaped by technological advancements and shifting lifestyle priorities. The rise of digital platforms and personalised recommendations has empowered consumers to tailor their retail experiences across channels. Furthermore, sustainability, the cost-of-living crisis, and flexible working have further influenced these behaviours, with shoppers increasingly seeking convenience, eco-friendly options, value-for-money, and delivery services.

Therefore, consumer behaviour, and the way in which it is shifting, is becoming increasingly complex and multi-dimensional. Understanding these behavioural shifts is essential for urban planners and retail managers for interventions, ensuring that physical retail spaces remain competitive in this landscape.

## Purpose
The purpose of this study is to develop an **openly available, national-level, small-area geodemographic classification dataset** that captures the multidimensional nature of consumer behaviour across England and Wales. 

Unlike earlier classifications, which have largely centred on socioeconomic structure, this study advances a theoretically grounded framework in which demographic, behavioural, digital, and accessibility dimensions are treated as co-determining drivers of consumer behaviour. This approach offers a refined conceptual lens for understanding how multiple domains collectively shape contemporary consumption patterns.

## Methodology
The classification is developed at the **Lower Super Output Area (LSOA)** level and is underpinned by complex analytical components:
- **Microsimulation**: Based on a proprietary consumer behavioural survey.
- **Demographic Factors**: Census-based socioeconomic attributes.
- **Accessibility Measures**: Spatial context and physical accessibility.
- **Digital Capability**: Online usage patterns and digital accessibility.

Through this contribution, the study extends existing geodemographic approaches by generating new empirical insight into how consumer behaviour varies spatially beyond what can be inferred from census-based classifications alone.

## Repository Structure
- `notebooks/`: Sequential Jupyter notebooks covering variable selection, data synthesis, and clustering analysis.
- `scripts/`: Python and R scripts for data harmonization and clustering robustness comparisons.
- `data/`: (Local only) Source data and lookups. Note: Large data files are ignored by version control.
- `results/`: Visual outputs, cluster characteristics, and final sub-classification figures.
- `docs/`: Manuscript and supplementary documentation.

## How to Use
1. **Prepare Data**: Ensure the LSOA indicators are placed in the `data/` directory.
2. **Run Pipeline**: Follow the numbered notebooks in the `notebooks/` directory to reproduce the classification.
3. **Validate**: Use the `scripts/robustness_comparison.py` to evaluate clustering performance against other methods like PAM or FGWC.

