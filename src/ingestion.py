import os
import pandas as pd
import numpy as np

class DataIngestion:
    def __init__(self, raw_data_path="data/raw/PS_20174371424001719_log.csv"):
        self.raw_data_path = raw_data_path

    def load_data(self):
        # 1. Local path try karo agar file exist karti hai
        if os.path.exists(self.raw_data_path):
            return pd.read_csv(self.raw_data_path)
        
        # 2. Cloud Fallback: Direct repo folder check
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alt_path = os.path.join(base_dir, "data", "raw", "PS_20174371424001719_log.csv")
        if os.path.exists(alt_path):
            return pd.read_csv(alt_path)

        # 3. Graceful Fallback: Render par dataset na hone par mock dataframe generate karo
        data = {
            'step': [1] * 100,
            'type': ['TRANSFER'] * 50 + ['CASH_OUT'] * 50,
            'amount': np.random.uniform(100, 500000, 100),
            'nameOrig': [f'C{i}' for i in range(100)],
            'oldbalanceOrg': np.random.uniform(1000, 500000, 100),
            'newbalanceOrig': np.random.uniform(0, 50000, 100),
            'nameDest': [f'M{i}' for i in range(100)],
            'oldbalanceDest': np.random.uniform(0, 50000, 100),
            'newbalanceDest': np.random.uniform(0, 100000, 100),
            'isFraud': [0] * 90 + [1] * 10,
            'isFlaggedFraud': [0] * 100
        }
        return pd.DataFrame(data)