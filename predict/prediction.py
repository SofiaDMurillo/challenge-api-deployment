import joblib
import pandas as pd
from pathlib import Path

# This code will use the trained model, take the preprocessed input from the user and make a prediction

# STEP 1 - Load the pkl model
model_path = Path("C:/Users/sofia/BeCode/Projects/ImmoEliza/04 challenge-api-deployment/model/model_lightgbm_Optuna_retrained.pkl")
model = joblib.load(model_path)                    

# STEP 2 - Load the preprocessed input


# STEP 3 - Make prediction and return result of prediction


def predict_price(preprocessed_data: dict) -> float:
    """
    Takes a dictionary of preprocessed input data,
    runs the prediction using the trained model,
    and returns the predicted price as a float.
    """
    # Convert input dict to single-row DataFrame
    input_df = pd.DataFrame([preprocessed_data])

    # Run prediction
    prediction = model.predict(input_df)

    # Extract the first (and only) prediction value
    predicted_value = float(prediction[0])

    return predicted_value

