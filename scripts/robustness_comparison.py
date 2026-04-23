
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
import os
import sys

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
    Outputs are formatted as CSV strings for easy copying.
    """
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

    # --- Print Results in CSV format for Copying ---
    print("\n" + "="*30)
    print("CLUSTERING COMPARISON (COPY-READY CSV)")
    print("="*30)
    summary_df = pd.DataFrame(results_summary)
    print(summary_df.to_csv(index=False))

    # --- Stability Analysis ---
    print("\n" + "="*30)
    print("STABILITY ANALYSIS (MEAN SILHOUETTE OVER 5 SUBSAMPLES)")
    print("="*30)
    stability_data = []
    
    for m_name in ['K-Means', 'PAM', 'FGWC']:
        if not any(d['Method'] == m_name for d in results_summary): continue
        
        scores = []
        for i in range(5):
            X_sample, indices = resample(X_scaled, np.arange(len(X_scaled)), n_samples=int(0.8*len(X_scaled)), random_state=i)
            if m_name == 'K-Means':
                model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit(X_sample)
            elif m_name == 'PAM':
                model = KMedoids(n_clusters=n_clusters, random_state=42).fit(X_sample)
            elif m_name == 'FGWC':
                c_sample = coords_scaled[indices]
                model = FGWC(n_clusters=n_clusters).fit(X_sample, c_sample)
            scores.append(silhouette_score(X_sample, model.labels_))
        
        stability_data.append({'Method': m_name, 'Mean_Silhouette': np.mean(scores), 'Std_Dev': np.std(scores)})
    
    print(pd.DataFrame(stability_data).to_csv(index=False))

    # --- Cluster Labels Output ---
    print("\n" + "="*30)
    print("CLUSTER LABELS (FIRST 20 ROWS - COPY-READY CSV)")
    print("="*30)
    print(labels_output.head(20).to_csv(index=False))

if __name__ == "__main__":
    # USER: Pointing to your actual data file
    FILE_PATH = r"C:\Users\sgabalog\Documents\P1\full_set.csv"
    
    if not os.path.exists(FILE_PATH):
        print(f"File {FILE_PATH} not found. Using synthetic data for demonstration...")
        df_demo = pd.DataFrame(np.random.rand(50, 5), columns=["feat1", "feat2", "feat3", "lat", "lon"])
        df_demo.to_csv("synthetic_data.csv", index=False)
        FILE_PATH = "synthetic_data.csv"
        FEATURES = ["feat1", "feat2", "feat3"]
        COORDINATES = ["lat", "lon"]
    else:
        # Load sample to auto-detect columns
        temp_df = pd.read_csv(FILE_PATH, nrows=5)
        cols = temp_df.columns.tolist()
        
        # Try to identify coordinates
        coord_candidates = ['lat', 'lon', 'latitude', 'longitude', 'x', 'y', 'X', 'Y', 'geometry']
        COORDINATES = [c for c in cols if any(cand == c.lower() for cand in coord_candidates)]
        
        # Identify numeric features (excluding coordinates and ID-like columns)
        FEATURES = [c for c in cols if pd.api.types.is_numeric_dtype(temp_df[c]) 
                    and c not in COORDINATES 
                    and 'id' not in c.lower() 
                    and 'index' not in c.lower()]
        
        print(f"Auto-detected Features: {FEATURES[:10]}...")
        print(f"Auto-detected Coordinates: {COORDINATES}")
        
    CLUSTERS = 3 # You can change this as needed
    
    perform_clustering_comparison(FILE_PATH, FEATURES, COORDINATES, CLUSTERS)

