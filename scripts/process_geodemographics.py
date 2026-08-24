"""
Geodemographic Data Processing Pipeline
=======================================
This script performs a sequential processing of geodemographic datasets:
1. Merges subcluster labels from CSV onto the base LSOA map shapefile.
2. Performs a spatial join between agent postcode geometries and the new subcluster map.
3. Exports the final postcode-to-subcluster mapping for use in the ABM.

Usage:
    python process_geodemographics.py [--postcode-shp PATH]

Arguments:
    --postcode-shp  Path to the agent postcode geometries shapefile.
                    Defaults to the POSTCODE_SHP environment variable,
                    or can be set directly in the script's DEFAULT_POSTCODE_SHP below.

Associated paper:
    Balog et al. (2026). Developing an open, national-level, small-area
    geodemographic classification of consumer behaviour.
    International Journal of Retail & Distribution Management, 1-16.
    https://doi.org/10.1108/IJRDM-06-2025-0436
"""

import argparse
import os
import geopandas as gpd
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Optional: set a default path here if not passing via CLI or environment var
# ---------------------------------------------------------------------------
DEFAULT_POSTCODE_SHP = os.environ.get("POSTCODE_SHP", "")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge geodemographic subcluster labels and perform postcode spatial join."
    )
    parser.add_argument(
        "--postcode-shp",
        type=str,
        default=DEFAULT_POSTCODE_SHP,
        help="Path to agent postcode geometries shapefile. "
             "Can also be set via the POSTCODE_SHP environment variable.",
    )
    return parser.parse_args()


def run_pipeline(postcode_shp_path: str):
    base_dir = Path(__file__).parent

    # Inputs
    subclusters_csv = base_dir / "lsoa_subcluster_assignments.csv"
    map_shp = base_dir / "map_shapefile.shp"
    postcode_shp = Path(postcode_shp_path)

    # Outputs
    subclusters_map_shp = base_dir / "subclusters.shp"
    final_mapping_csv = base_dir / "postcode_subcluster_map.csv"

    if not postcode_shp.exists():
        raise FileNotFoundError(
            f"Postcode shapefile not found: {postcode_shp}\n"
            "Supply the path via --postcode-shp or the POSTCODE_SHP environment variable."
        )

    # --- Step 1: Merge CSV labels to Map Shapefile ---
    print("Step 1: Merging subcluster labels to LSOA map...")
    df_labels = pd.read_csv(subclusters_csv)
    df_labels['LSOA21CD'] = df_labels['LSOA21CD'].astype(str)

    gdf_map = gpd.read_file(map_shp)
    gdf_map['LSOA21CD'] = gdf_map['LSOA21CD'].astype(str)

    gdf_merged = gdf_map.merge(df_labels[['LSOA21CD', 'Subcluster']], on='LSOA21CD', how='left')

    print(f"Saving merged shapefile to {subclusters_map_shp.name}...")
    gdf_merged.to_file(subclusters_map_shp)

    # --- Step 2: Spatial Join Postcodes to Subclusters ---
    print("Step 2: Performing spatial join for agent postcodes...")
    gdf_postcodes = gpd.read_file(postcode_shp)

    if gdf_postcodes.crs != gdf_merged.crs:
        print(f"Reprojecting postcodes to {gdf_merged.crs}...")
        gdf_postcodes = gdf_postcodes.to_crs(gdf_merged.crs)

    print("Matching postcodes to subcluster polygons...")
    matched = gpd.sjoin(gdf_postcodes, gdf_merged[['geometry', 'Subcluster']], how='left', predicate='within')

    final_mapping = matched[['Postcode', 'Subcluster']].copy()
    print(f"Saving final mapping to {final_mapping_csv.name}...")
    final_mapping.to_csv(final_mapping_csv, index=False)

    print("\nPipeline complete!")
    print(f"Total postcodes processed: {len(final_mapping)}")
    print(f"Unmatched postcodes: {final_mapping['Subcluster'].isna().sum()}")


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.postcode_shp)
