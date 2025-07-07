from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Literal
import pandas as pd
import joblib
import os

# Définir le chemin du modèle à partir de ce fichier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_FILENAME = "model_lightgbm_Optuna_retrained.pkl"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

# Charger le modèle
model = joblib.load(MODEL_PATH)
print("Model expects features:", model.feature_name_)


# Expected columns from the model
expected_columns = [
    "habitableSurface",
    "bedroomCount",
    "buildingCondition",
    "hasGarden",
    "gardenSurface",
    "hasTerrace",
    "postCode",
    "type"
]

app = FastAPI()

# Input data from the api request
class InputData(BaseModel):
    area: int = Field(..., alias="area")
    property_type: Literal["APARTMENT", "HOUSE", "OTHERS"] = Field(..., alias="property-type")
    rooms_number: int = Field(..., alias="rooms-number")
    zip_code: int = Field(..., alias="zip-code")
    land_area: Optional[int] = Field(None, alias="land-area")
    garden: Optional[bool] = True
    garden_area: Optional[int] = Field(0, alias="garden-area")
    equipped_kitchen: Optional[bool] = True
    full_address: Optional[str] = Field(None, alias="full-address")
    swimming_pool: Optional[bool] = True
    furnished: Optional[bool] = True
    open_fire: Optional[bool] = True
    terrace: Optional[bool] = True
    terrace_area: Optional[int] = Field(0, alias="terrace-area")
    facades_number: Optional[int] = Field(0, alias="facades-number")
    building_state: Optional[Literal[
        "NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"
    ]] = Field("UNKNOWN", alias="building-state")


class PredictionOutput(BaseModel):
    predicted_price: float

@app.post("/predict", response_model=PredictionOutput)
def predict(data: InputData):
    features = {
        "habitableSurface": data.area,
        "bedroomCount": data.rooms_number,
        "buildingCondition": data.building_state or "UNKNOWN",
        "hasGarden": data.garden or False,
        "gardenSurface": data.garden_area or 0,
        "hasTerrace": data.terrace or False,
        "postCode": data.zip_code,
        "type": data.property_type
    }

    # Create the DataFrame with columns in the expected order
    df = pd.DataFrame([features])[expected_columns]

    # Explicit conversion of categorical columns
    df["type"] = df["type"].astype("category")
    df["buildingCondition"] = df["buildingCondition"].astype("category")

    # Get the predicted price for the single input row (first element of the output array)
    prediction = model.predict(df)[0]

    return PredictionOutput(predicted_price=round(float(prediction), 2))


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

