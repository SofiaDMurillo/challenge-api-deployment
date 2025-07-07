import sys, os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Literal
import joblib
import pandas as pd

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

# Load the model (adjust path if needed)
MODEL_PATH = os.path.join(project_root, "app/backend/model/model_lightgbm_Optuna_retrained.pkl")
model = joblib.load(MODEL_PATH)

app = FastAPI()

# ----- INPUT SCHEMA -----
class InputData(BaseModel):
    area: int = Field(..., alias="area")
    property_type: Literal["APARTMENT", "HOUSE", "OTHERS"] = Field(..., alias="property-type")
    rooms_number: int = Field(..., alias="rooms-number")
    zip_code: int = Field(..., alias="zip-code")
    land_area: Optional[int] = Field(None, alias="land-area")
    garden: Optional[bool]
    garden_area: Optional[int] = Field(None, alias="garden-area")
    equipped_kitchen: Optional[bool] = Field(None, alias="equipped-kitchen")
    full_address: Optional[str] = Field(None, alias="full-address")
    swimming_pool: Optional[bool] = Field(None, alias="swimming-pool")
    furnished: Optional[bool]
    open_fire: Optional[bool] = Field(None, alias="open-fire")
    terrace: Optional[bool]
    terrace_area: Optional[int] = Field(None, alias="terrace-area")
    facades_number: Optional[int] = Field(None, alias="facades-number")
    building_state: Optional[Literal[
        "NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"
    ]] = Field(None, alias="building-state")


class PredictionOutput(BaseModel):
    predicted_price: float

# ----- PREDICTION ROUTE -----
@app.post("/predict", response_model=PredictionOutput)
def predict(data: InputData):
    features = {
        "habitableSurface": data.area,
        "bedroomCount": data.rooms_number,
        "buildingCondition": data.building_state or "UNKNOWN",
        "hasGarden": data.garden if data.garden is not None else False,
        "gardenSurface": data.garden_area or 0,
        "hasTerrace": data.terrace if data.terrace is not None else False,
        "postCode": data.zip_code,
        "type": data.property_type
    }

    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]

    return PredictionOutput(predicted_price=round(prediction, 2))

# ----- HEALTH CHECK -----
@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}



