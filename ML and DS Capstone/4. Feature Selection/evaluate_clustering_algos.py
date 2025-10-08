import numpy as np
import pandas as pd
from sklearn.cluster import (
    KMeans, AgglomerativeClustering, SpectralClustering, Birch,
    DBSCAN, OPTICS, AffinityPropagation, MeanShift
)
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (
    silhouette_score, davies_bouldin_score, calinski_harabasz_score
)
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler

scalers = [
    ('RobustScaler', RobustScaler()),
    ('MinMaxScaler', MinMaxScaler()),
    ('StandardScaler', StandardScaler()),
]

results_table = []

def evaluate_clustering_algorithms(
    X,
    no_clust=3,
    rand_state=10,
    min_samples=None,
    top_n=3,
    verbose=True
):
    if min_samples is None:
        min_samples = X.shape[1] * 2

    results = {}

    def count_clusters(labels):
        return len(set(labels)) - (1 if -1 in labels else 0)

    def evaluate_clustering(model, X, model_name):
        labels = model.fit_predict(X)
        n_clusters = count_clusters(labels)
        if n_clusters > 1:
            sil = silhouette_score(X, labels)
            db = davies_bouldin_score(X, labels)
            ch = calinski_harabasz_score(X, labels)
        else:
            sil = db = ch = np.nan
        results[model_name] = {
            'Num_Clusters': n_clusters,
            'Silhouette': sil,
            'DaviesBouldin': db,
            'CalinskiHarabasz': ch
        }

    # Evaluate clustering models
    evaluate_clustering(KMeans(n_clusters=no_clust, random_state=rand_state), X, 'KMeans')
    evaluate_clustering(AgglomerativeClustering(n_clusters=no_clust), X, 'Agglomerative')

    # Gaussian Mixture
    gmm = GaussianMixture(n_components=no_clust, random_state=rand_state)
    labels = gmm.fit_predict(X)
    n_clusters = count_clusters(labels)
    if n_clusters > 1:
        sil = silhouette_score(X, labels)
        db = davies_bouldin_score(X, labels)
        ch = calinski_harabasz_score(X, labels)
    else:
        sil = db = ch = np.nan
    results['GaussianMixture'] = {
        'Num_Clusters': n_clusters,
        'Silhouette': sil,
        'DaviesBouldin': db,
        'CalinskiHarabasz': ch
    }

    evaluate_clustering(SpectralClustering(n_clusters=no_clust, random_state=rand_state, affinity='nearest_neighbors'), X, 'SpectralClustering')
    evaluate_clustering(Birch(n_clusters=no_clust), X, 'Birch')

    # DBSCAN with eps from k-distance curve
    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X)
    distances, _ = neighbors.kneighbors(X)
    k_distances = np.sort(distances[:, -1])
    kneedle = KneeLocator(range(len(k_distances)), k_distances, curve='convex', direction='increasing')
    eps = k_distances[kneedle.knee] if kneedle.knee is not None else np.percentile(k_distances, 90)
    evaluate_clustering(DBSCAN(eps=eps, min_samples=min_samples), X, 'DBSCAN')
    evaluate_clustering(OPTICS(min_samples=min_samples), X, 'OPTICS')
    evaluate_clustering(AffinityPropagation(random_state=rand_state), X, 'AffinityPropagation')
    evaluate_clustering(MeanShift(), X, 'MeanShift')

    # Create DataFrame
    df_results = pd.DataFrame(results).T

    # Format the numeric output columns for display
    for col in ['Silhouette', 'DaviesBouldin', 'CalinskiHarabasz']:
        df_results[col] = df_results[col].apply(lambda x: "Not available" if pd.isna(x) else f"{x:.4f}")

    if verbose:
        print(df_results)

        # For top N display, note: lower DaviesBouldin is better; others, higher is better.
        metrics_direction = {
            'Silhouette': False,
            'CalinskiHarabasz': False,
            'DaviesBouldin': True
        }

        for metric, asc in metrics_direction.items():
            topn = df_results[df_results[metric] != "Not available"].copy()
            topn[metric] = topn[metric].astype(float)
            topn = topn.sort_values(by=metric, ascending=asc).head(top_n)
            print(f"\nTop {top_n} Algorithms for {metric}:")
            print(topn[['Num_Clusters', metric]])

    return df_results



def run_all_scalers_unified(clust_algos, dataset_unscaled, no_clust=3, rand_state=10, top_n=3, verbose=True):
    all_df_scores = {}
    for scaler_name, scaler in scalers:
        X_scaled = scaler.fit_transform(dataset_unscaled)
        print(f'Scores for Dataset scaled with {scaler_name}\n')
        df_scores = evaluate_clustering_algorithms(X_scaled, no_clust=no_clust, rand_state=rand_state, top_n=top_n, verbose=verbose)
        all_df_scores[scaler_name] = df_scores
        # Find best for each metric and algorithm
        best_sil = df_scores[df_scores['Silhouette'] != 'Not available']['Silhouette'].astype(float).idxmax()
        best_ch = df_scores[df_scores['CalinskiHarabasz'] != 'Not available']['CalinskiHarabasz'].astype(float).idxmax()
        best_db = df_scores[df_scores['DaviesBouldin'] != 'Not available']['DaviesBouldin'].astype(float).idxmin()
        results_table.append({
            'Scaler': scaler_name,
            'Best_Silhouette_Algo': best_sil,
            'Best_Silhouette': float(df_scores.loc[best_sil, 'Silhouette']),
            'Best_CalinskiHarabasz_Algo': best_ch,
            'Best_CalinskiHarabasz': float(df_scores.loc[best_ch, 'CalinskiHarabasz']),
            'Best_DaviesBouldin_Algo': best_db,
            'Best_DaviesBouldin': float(df_scores.loc[best_db, 'DaviesBouldin']),
        })
        print(df_scores)
        print('\n')
    return pd.DataFrame(results_table), all_df_scores
