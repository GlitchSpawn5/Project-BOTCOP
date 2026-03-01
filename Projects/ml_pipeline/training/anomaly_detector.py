import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import jobio
import os

class AnomalyDetector:
    def __init__(self, model_path="ml_pipeline/models/anomaly_model.joblib"):
        self.model_path = model_path
        self.clf = IsolationForest(contamination=0.05, random_state=42)
        if os.path.exists(model_path):
            self.clf = joblib.load(model_path)

    def train(self, data: pd.DataFrame):
        # Feature engineering: convert categorical to numeric for simplicity
        df = self._preprocess(data)
        self.clf.fit(df)
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.clf, self.model_path)

    def predict(self, log_feature_vector: list):
        # Returns -1 for anomaly, 1 for normal
        prediction = self.clf.predict([log_feature_vector])
        return prediction[0]

    def _preprocess(self, df):
        # Simplified preprocessing for the prototype
        # In a real system, we'd use one-hot encoding or embeddings
        return df.select_dtypes(include=[np.number])

# feature_vector mapping for prototype:
# [hour_of_day, user_id_hash, service_id_hash, status_code]
