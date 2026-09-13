import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Any
from config import N_CLUSTERS, RANDOM_STATE

class PlayerClusteringModel:
    """
    Machine Learning model for player tactical profile classification (K-Means)
    and spatial dimensionality reduction (PCA).
    Combines official Starting XI positions with match activity features.
    """

    def __init__(self, n_clusters: int = N_CLUSTERS):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=RANDOM_STATE, n_init=10)
        self.pca = PCA(n_components=2, random_state=RANDOM_STATE)

    def _derive_authentic_role(self, row: pd.Series) -> str:
        """
        Derives an authentic tactical role profile combining official position metadata
        and pitch activity features (xG, pass volume, pressure intensity).
        """
        pos = str(row.get("official_position", "")).lower()
        xg = row.get("total_xg", 0.0)
        passes = row.get("passes_completed", 0.0)
        pressures = row.get("pressures", 0.0)
        avg_x = row.get("avg_x", 60.0)

        # Goalkeeper
        if "goalkeeper" in pos or "keeper" in pos:
            return "Goalkeeper"

        # Center Forward / Striker
        if "forward" in pos or "striker" in pos or "center forward" in pos:
            return "Attacking Forward / Striker"

        # Wingers
        if "wing" in pos or "winger" in pos:
            if passes >= 15 or xg >= 0.1:
                return "Progressive Wing Attacker"
            return "Wide Attacking Winger"

        # Attacking Midfield
        if "attacking midfield" in pos:
            return "Attacking Midfield Creator"

        # Defensive / Central Midfield
        if "defensive midfield" in pos or "center defensive midfield" in pos:
            return "Holding Midfield Anchor / Pivot"

        if "central midfield" in pos or "center midfield" in pos:
            if pressures >= 4:
                return "Box-to-Box Pressing Midfielder"
            return "Central Midfield Playmaker"

        # Full Backs / Wing Backs
        if "back" in pos and ("left" in pos or "right" in pos) and "center" not in pos:
            return "Overlapping Full-Back / Wing-Back"

        # Center Backs
        if "center back" in pos or "centre back" in pos:
            return "Central Defender / Ball-Playing CB"

        # Fallback spatial activity classification
        if xg >= 0.15 or avg_x >= 80:
            return "Attacking Forward / Striker"
        elif avg_x < 50:
            return "Defensive Back / Center Back"
        elif passes >= 15:
            return "Central Playmaker / Controller"
        
        return "Versatile Core Player"

    def train_and_predict(self, player_stats_df: pd.DataFrame) -> pd.DataFrame:
        """
        Trains K-Means & PCA on player feature vectors and profiles dynamic tactical roles.
        """
        if player_stats_df.empty:
            return pd.DataFrame()

        df = player_stats_df.copy()
        
        feature_cols = [
            "avg_x", "avg_y", "passes_completed", "pass_completion_pct", 
            "shots", "goals", "total_xg", "pressures", "blocks"
        ]
        
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0.0

        # Assign authentic tactical roles based on position + activity
        df["tactical_role"] = df.apply(self._derive_authentic_role, axis=1)

        X = df[feature_cols].fillna(0).values
        actual_clusters = min(self.n_clusters, len(df))
        if actual_clusters < 1:
            return df

        kmeans_model = KMeans(n_clusters=actual_clusters, random_state=RANDOM_STATE, n_init=10)
        X_scaled = self.scaler.fit_transform(X)
        df["cluster_id"] = kmeans_model.fit_predict(X_scaled)

        # Fit PCA
        pca_coords = self.pca.fit_transform(X_scaled)
        df["pca_x"] = pca_coords[:, 0]
        df["pca_y"] = pca_coords[:, 1]
        
        return df

    def find_similar_players(self, player_name: str, df_clustered: pd.DataFrame, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Calculates Euclidean similarity distance between players in PCA feature space.
        """
        if df_clustered.empty or player_name not in df_clustered["player"].values:
            return []

        target_row = df_clustered[df_clustered["player"] == player_name].iloc[0]
        target_vec = np.array([target_row["pca_x"], target_row["pca_y"]])
        
        similarities = []
        for idx, row in df_clustered.iterrows():
            if row["player"] == player_name:
                continue
            curr_vec = np.array([row["pca_x"], row["pca_y"]])
            dist = float(np.linalg.norm(target_vec - curr_vec))
            sim_score = round(max(0.0, 100.0 - (dist * 20.0)), 1)
            similarities.append({
                "player": row["player"],
                "team": row["team"],
                "official_position": row.get("official_position", "Field Player"),
                "tactical_role": row["tactical_role"],
                "similarity_score": sim_score
            })
            
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similarities[:top_n]

if __name__ == "__main__":
    from modules.data_loader import DataLoader
    loader = DataLoader()
    matches = loader.fetch_all_matches()
    events = loader.fetch_match_events(matches["match_id"].iloc[0])
    p_stats = loader.get_player_stats_for_events(events)
    model = PlayerClusteringModel()
    res = model.train_and_predict(p_stats)
    print(res[["player", "official_position", "tactical_role"]])
