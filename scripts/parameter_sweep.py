import pandas as pd
import numpy as np
import os
import sys
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph

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
    def __init__(self, n_clusters=4, m=2, max_iter=100, tol=1e-5, alpha=0.5):
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
        self.labels_ = np.argmax(u, axis=1)
        return self

def run_validation_sweep(data_path, feature_cols, coord_cols=None):
    if not os.path.exists(data_path):
        print(f"ERROR: File {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    if coord_cols:
        coords = df[coord_cols].values
        coords_scaled = StandardScaler().fit_transform(coords)
        # Connectivity for spatial constraint
        connectivity = kneighbors_graph(coords_scaled, n_neighbors=10, include_self=False)
    else:
        coords_scaled = None
        connectivity = None

    results = []

    def evaluate(method_name, labels, k_val):
        results.append({
            'Method': method_name,
            'K': k_val,
            'Silhouette': silhouette_score(X_scaled, labels),
            'Davies_Bouldin': davies_bouldin_score(X_scaled, labels),
            'Calinski_Harabasz': calinski_harabasz_score(X_scaled, labels)
        })

    print("Starting Comprehensive Validation Sweep (K=3, 4, 5 for all methods)...")

    for k in [3, 4, 5]:
        print(f"\n--- Testing K={k} ---")
        
        # 1. K-Means
        print(f"Running K-Means...")
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
        evaluate('K-Means', km.labels_, k)

        # 2. PAM
        if KMedoids:
            print(f"Running PAM...")
            pam = KMedoids(n_clusters=k, random_state=42, method='pam').fit(X_scaled)
            evaluate('PAM', pam.labels_, k)
        
        # 3. FGWC
        if coords_scaled is not None:
            print(f"Running FGWC...")
            fgwc = FGWC(n_clusters=k, alpha=0.5).fit(X_scaled, coords_scaled)
            evaluate('FGWC', fgwc.labels_, k)

        # 4. Hierarchical
        print(f"Running Hierarchical...")
        hier = AgglomerativeClustering(n_clusters=k).fit(X_scaled)
        evaluate('Hierarchical', hier.labels_, k)

        # 5. Model-based (GMM)
        print(f"Running Model-based (GMM)...")
        gmm = GaussianMixture(n_components=k, random_state=42).fit(X_scaled)
        evaluate('GMM (Model-based)', gmm.predict(X_scaled), k)

        # 6. Spatially Constrained
        if connectivity is not None:
            print(f"Running Spatially Constrained...")
            spat_const = AgglomerativeClustering(n_clusters=k, connectivity=connectivity).fit(X_scaled)
            evaluate('Spatially Constrained', spat_const.labels_, k)

    # --- Final Output ---
    print("\n" + "="*60)
    print("COMPREHENSIVE VALIDATION SWEEP RESULTS (COPY-READY CSV)")
    print("="*60)
    results_df = pd.DataFrame(results).sort_values(['Method', 'K'])
    print(results_df.to_csv(index=False))

if __name__ == "__main__":
    FILE_PATH = r"C:\Users\sgabalog\Documents\P1\full_set.csv"
    
    if os.path.exists(FILE_PATH):
        # Auto-detect as in previous script
        temp_df = pd.read_csv(FILE_PATH, nrows=5)
        cols = temp_df.columns.tolist()
        coord_candidates = ['lat', 'lon', 'latitude', 'longitude', 'x', 'y', 'X', 'Y', 'geometry']
        COORDINATES = [c for c in cols if any(cand == c.lower() for cand in coord_candidates)]
        FEATURES = [c for c in cols if pd.api.types.is_numeric_dtype(temp_df[c]) 
                    and c not in COORDINATES 
                    and 'id' not in c.lower() 
                    and 'index' not in c.lower()]
        
        print(f"File: {FILE_PATH}")
        print(f"Detected Coordinates: {COORDINATES}")
        print(f"Detected Features: {len(FEATURES)} features detected.")
        
        run_validation_sweep(FILE_PATH, FEATURES, COORDINATES)
    else:
        print(f"File {FILE_PATH} not found. Please check the path.")
