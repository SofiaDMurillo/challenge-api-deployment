from pathlib import Path
import pickle
import pandas as pd

# Load model 
model_path = Path(r"C:\Users\sofia\BeCode\Projects\ImmoEliza\04 challenge-api-deployment\model\model_lightgbm_Optuna.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Prediction function
def predict(input_df: pd.DataFrame) -> list:
    """
    Predict prices given a preprocessed dataframe.
    Returns predictions as a list.
    """
    preds = model.predict(input_df)
    return preds.tolist()