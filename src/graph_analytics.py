import pandas as pd
import networkx as nx
from typing import Dict, Any


class TransactionGraphAnalytics:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.G = nx.DiGraph()  # Directed Graph for money flow

    def build_graph(self, sample_size: int = 50000):
        """Builds directed transaction graph from financial transactions."""
        print(f"Building Directed Transaction Graph for {sample_size:,} edges...")
        sample_df = self.df.head(sample_size)

        # Add directed edges from nameOrig -> nameDest with amount attribute
        for _, row in sample_df.iterrows():
            self.G.add_edge(
                row["nameOrig"], row["nameDest"], weight=float(row["amount"])
            )

        print(
            f"✔ Graph built successfully! Nodes: {self.G.number_of_nodes():,}, Edges: {self.G.number_of_edges():,}"
        )

    def compute_node_metrics(self, account_id: str) -> Dict[str, Any]:
        """Computes graph centrality and PageRank metrics for a given account node."""
        if account_id not in self.G:
            return {
                "in_degree": 0,
                "out_degree": 0,
                "pagerank": 0.0,
                "is_hub": False,
            }

        in_deg = self.G.in_degree(account_id)
        out_deg = self.G.out_degree(account_id)

        # PageRank computation over local subgraph component for performance
        try:
            pagerank_scores = nx.pagerank(self.G, max_iter=50)
            node_pagerank = round(pagerank_scores.get(account_id, 0.0), 6)
        except Exception:
            node_pagerank = 0.0

        is_hub = out_deg > 5 or in_deg > 5

        return {
            "in_degree": in_deg,
            "out_degree": out_deg,
            "pagerank": node_pagerank,
            "is_hub": is_hub,
        }


if __name__ == "__main__":
    from ingestion import DataIngestion
    from cleaning import DataCleaner

    raw_df = DataIngestion("data/raw/PS_20174371424001719_log.csv").load_data()
    clean_df = DataCleaner(raw_df).filter_relevant_types()

    graph_analyzer = TransactionGraphAnalytics(clean_df)
    graph_analyzer.build_graph(sample_size=50000)

    # Test metrics for a sample origin account
    sample_account = clean_df["nameOrig"].iloc[0]
    metrics = graph_analyzer.compute_node_metrics(sample_account)

    print(f"\n=== Graph Metrics for Account ({sample_account}) ===")
    print(metrics)