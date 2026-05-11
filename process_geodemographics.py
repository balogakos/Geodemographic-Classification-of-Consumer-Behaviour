"""
Geodemographic Data Processing Pipeline
=======================================
This script performs a sequential processing of geodemographic datasets:
1. Merges subcluster labels from CSV onto the base LSOA map shapefile.
2. Performs a spatial join between agent postcode geometries and the new subcluster map.
3. Exports the final postcode-to-subcluster mapping for use in the ABM.

Usage:
    python process_geodemographics.py
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
import os

def run_pipeline():
    # --- Paths Configuration ---
    base_dir = Path(__file__).parent
    
    # Inputs
    subclusters_csv = base_dir / "subclusters_done.csv"
    map_shp = base_dir / "map_shapefile.shp"
    postcode_shp = Path(r"c:\Users\sgabalog\Documents\P3\Model\data_local\liverpool\processed\agent_postcode_geometries.shp")
    
    # Outputs
    subclusters_map_shp = base_dir / "subclusters.shp"
    final_mapping_csv = base_dir / "postcode_subcluster_map.csv"

    # --- Step 1: Merge CSV labels to Map Shapefile ---
    print("Step 1: Merging subcluster labels to LSOA map...")
    df_labels = pd.read_csv(subclusters_csv)
    df_labels['LSOA21CD'] = df_labels['LSOA21CD'].astype(str)
    
    gdf_map = gpd.read_file(map_shp)
    gdf_map['LSOA21CD'] = gdf_map['LSOA21CD'].astype(str)
    
    # Merge Subcluster column
    gdf_merged = gdf_map.merge(df_labels[['LSOA21CD', 'Subcluster']], on='LSOA21CD', how='left')
    
    print(f"Saving merged shapefile to {subclusters_map_shp.name}...")
    gdf_merged.to_file(subclusters_map_shp)

    # --- Step 2: Spatial Join Postcodes to Subclusters ---
    print("Step 2: Performing spatial join for agent postcodes...")
    gdf_postcodes = gpd.read_file(postcode_shp)
    
    # Ensure CRS match (Postcodes are usually 4326, Map is usually 27700)
    if gdf_postcodes.crs != gdf_merged.crs:
        print(f"Reprojecting postcodes to {gdf_merged.crs}...")
        gdf_postcodes = gdf_postcodes.to_crs(gdf_merged.crs)
    
    # Join Point-in-Polygon
    print("Matching postcodes to subcluster polygons...")
    matched = gpd.sjoin(gdf_postcodes, gdf_merged[['geometry', 'Subcluster']], how='left', predicate='within')
    
    # Clean up and export
    final_mapping = matched[['Postcode', 'Subcluster']].copy()
    print(f"Saving final mapping to {final_mapping_csv.name}...")
    final_mapping.to_csv(final_mapping_csv, index=False)
    
    print("\nPipeline complete!")
    print(f"Total postcodes processed: {len(final_mapping)}")
    print(f"Unmatched postcodes: {final_mapping['Subcluster'].isna().sum()}")

if __name__ == "__main__":
    run_pipeline()
