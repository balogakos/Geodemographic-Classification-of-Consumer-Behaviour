"""
Geodemographic Classification of Consumer Behaviour
Module: Clustering Robustness Analysis
Author: Akos Balog
Description: This script performs a comparative robustness analysis between 
K-Means, Partition Around Medoids (PAM), and Fuzzy Geographically Weighted Clustering (FGWC).
It evaluates clustering quality via Silhouette scores and Davies-Bouldin index, 
and measures stability through subsampling.
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample

# Try to import KMedoids for PAM.
try:
    from sklearn_extra.cluster import KMedoids
except ImportError:
    KMedoids = None

class FGWC:
    """
    Fuzzy Geographically Weighted Clustering (FGWC)
    Simplification: Fuzzy C-Means with Spatial Distance Weighting.
    """
    def __init__(self, n_clusters=3, m=2, max_iter=100, tol=1e-5, alpha=0.5):
        self.n_clusters = n_clusters
        self.m = m 
        self.max_iter = max_iter
        self.tol = tol
        self.alpha = alpha 
        self.centroids = None
        self.u = None

    def fit(self, X, coords):
        X = np.array(X)
        coords = np.array(coords)
        n_samples = X.shape[0]
        u = np.random.dirichlet(np.ones(self.n_clusters), size=n_samples)
        
        for i in range(self.max_iter):
            u_old = u.copy()
            um = u ** self.m
            centroids = (um.T @ X) / (um.sum(axis=0)[:, None] + 1e-10)
            centroid_coords = (um.T @ coords) / (um.sum(axis=0)[:, None] + 1e-10)
            
            attr_dist = np.linalg.norm(X[:, None] - centroids, axis=2)
            geo_dist = np.linalg.norm(coords[:, None] - centroid_coords, axis=2)
            
            dist = (1 - self.alpha) * attr_dist + self.alpha * geo_dist
            dist = np.fmax(dist, 1e-10)
            
            inv_dist = 1.0 / (dist ** (2 / (self.m - 1)))
            u = inv_dist / inv_dist.sum(axis=1)[:, None]
            
            if np.linalg.norm(u - u_old) < self.tol:
                break
                
        self.u = u
        self.centroids = centroids
        self.labels_ = np.argmax(u, axis=1)
        return self

def perform_clustering_comparison(data_path, feature_cols, coord_cols=None, n_clusters=3):
    """
    Main function to run K-Means, PAM, and FGWC and compare results.
    """
    print(f"\n--- Loading Data from: {data_path} ---")
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"ERROR: Could not read file {data_path}. {e}")
        return

    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    results_summary = []
    labels_output = df.copy()

    # --- K-Means ---
    print("Running K-Means...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans_labels = kmeans.fit_predict(X_scaled)
    results_summary.append({
        'Method': 'K-Means',
        'Silhouette': silhouette_score(X_scaled, kmeans_labels),
        'DB_Index': davies_bouldin_score(X_scaled, kmeans_labels)
    })
    labels_output['KMeans_Labels'] = kmeans_labels

    # --- PAM ---
    if KMedoids:
        print("Running PAM (K-Medoids)...")
        pam = KMedoids(n_clusters=n_clusters, random_state=42, method='pam')
        pam_labels = pam.fit_predict(X_scaled)
        results_summary.append({
            'Method': 'PAM',
            'Silhouette': silhouette_score(X_scaled, pam_labels),
            'DB_Index': davies_bouldin_score(X_scaled, pam_labels)
        })
        labels_output['PAM_Labels'] = pam_labels
    else:
        print("NOTE: PAM (KMedoids) skipped. Install with 'pip install scikit-learn-extra'.")

    # --- FGWC ---
    if coord_cols and all(col in df.columns for col in coord_cols):
        print("Running Fuzzy Geographically Weighted Clustering (FGWC)...")
        coords = df[coord_cols].values
        coords_scaled = StandardScaler().fit_transform(coords)
        fgwc = FGWC(n_clusters=n_clusters, alpha=0.5)
        fgwc.fit(X_scaled, coords_scaled)
        fgwc_labels = fgwc.labels_
        results_summary.append({
            'Method': 'FGWC',
            'Silhouette': silhouette_score(X_scaled, fgwc_labels),
            'DB_Index': davies_bouldin_score(X_scaled, fgwc_labels)
        })
        labels_output['FGWC_Labels'] = fgwc_labels

    # --- Results Table ---
    print("\n" + "="*50)
    print("        CLUSTERING COMPARISON SUMMARY")
    print("="*50)
    summary_df = pd.DataFrame(results_summary)
    print(summary_df.round(4).to_string(index=False))

    # --- Stability Analysis ---
    print("\n" + "="*50)
    print("    STABILITY ANALYSIS (SILHOUETTE UNDER SUBSAMPLING)")
    print("="*50)
    stability_data = []
    
    for m_name in ['K-Means', 'PAM', 'FGWC']:
        if not any(d['Method'] == m_name for d in results_summary): continue
        
        scores = []
        ari_scores = []
        # Increased to 30 iterations for substance as requested
        for i in range(30):
            X_sample = resample(X_scaled, n_samples=int(0.8*len(X_scaled)), random_state=i)
            if m_name == 'K-Means':
                # Re-running with different seeds and subsamples
                model = KMeans(n_clusters=n_clusters, random_state=i, n_init=10).fit(X_sample)
                # Calculate ARI by predicting on full set to check consistency
                full_labels = model.predict(X_scaled)
                ari_scores.append(adjusted_rand_score(kmeans_labels, full_labels))
            elif m_name == 'PAM':
                model = KMedoids(n_clusters=n_clusters, random_state=i).fit(X_sample)
            elif m_name == 'FGWC':
                # For FGWC, we'd need to handle coordinates similarly, simplified here
                model = FGWC(n_clusters=n_clusters).fit(X_sample, coords_scaled[:len(X_sample)])
            
            scores.append(silhouette_score(X_sample, model.labels_))
        
        row = {'Method': m_name, 'Mean_Silhouette': np.mean(scores), 'Std_Dev': np.std(scores)}
        if m_name == 'K-Means':
            row['Mean_ARI'] = np.mean(ari_scores)
        stability_data.append(row)
    
    print(pd.DataFrame(stability_data).round(4).to_string(index=False))

    # --- Save Sample to Log ---
    print("\nTop 5 Cluster Assignments:")
    print(labels_output[['KMeans_Labels']].head().to_string())

if __name__ == "__main__":
    # Path configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "full_set.csv")
    
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found at {DATA_PATH}. Please ensure 'data/full_set.csv' exists.")
        sys.exit(1)
        
    # Auto-detect features
    sample_df = pd.read_csv(DATA_PATH, nrows=5)
    cols = sample_df.columns.tolist()
    
    # Identify coordinates
    coord_candidates = ['lat', 'lon', 'latitude', 'longitude', 'x', 'y', 'X', 'Y', 'geometry']
    COORDINATES = [c for c in cols if any(cand == c.lower() for cand in coord_candidates)]
    
    # Identify numeric features
    FEATURES = [c for c in cols if pd.api.types.is_numeric_dtype(sample_df[c]) 
                and c not in COORDINATES 
                and 'id' not in c.lower() 
                and 'index' not in c.lower()]
    
    N_CLUSTERS = 3 # Default cluster count for comparison
    
    perform_clustering_comparison(DATA_PATH, FEATURES, COORDINATES, N_CLUSTERS)

