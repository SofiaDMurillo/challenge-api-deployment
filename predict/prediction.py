from pathlib import Path
import pickle
import pandas as pd
import os

# Get absolute path relative to this file location
model_path = Path(__file__).parent.parent / "model" / "model_lightgbm_Optuna.pkl"

with open(model_path, 'rb') as f:
    model = pickle.load(f)

def predict(input_df: pd.DataFrame) -> list:
    preds = model.predict(input_df)
    preds = [int(round(p)) for p in preds]
    return preds