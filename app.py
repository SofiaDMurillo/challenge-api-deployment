from fastapi import FastAPI, HTTPException
from typing import List, Union

from preprocessing.clean_data import preprocess_input, PropertyInput
from predict.prediction import predict

app = FastAPI()

# Health check
@app.get("/")
async def health():
    return {"status": "alive"}

# GET request to explain the POST input format (because I made it consistent with model, otherwise thre will be an error)
@app.get("/info")
async def get_info():
    return {
        "message": "Welcome to the ImmoEliza price prediction API!",
        "post_endpoint": "/predict",
        "expected_input_format": {
            "habitableSurface": "float",
            "bedroomCount": "int",
            "buildingCondition": "int",
            "hasGarden": "int (0 or 1)",
            "gardenSurface": "float",
            "hasTerrace": "int (0 or 1)",
            "epcScore": "float",
            "hasParking": "int (0 or 1)",
            "postCode": "int",
            "type": "string",
            "province": "string",
            "subtype": "string",
            "region": "string"
        },
        "example_input": {
            "habitableSurface": 120.5,
            "bedroomCount": 3,
            "buildingCondition": 4,
            "hasGarden": 1,
            "gardenSurface": 50.0,
            "hasTerrace": 0,
            "epcScore": 180.0,
            "hasParking": 1,
            "postCode": 1000,
            "type": "Apartment",
            "province": "Brussels",
            "subtype": "Penthouse",
            "region": "Brussels-Capital"
        }
    }

# Existing POST route for predictions
@app.post("/predict")
def predict_price(properties: Union[PropertyInput, List[PropertyInput]]):
    try:
        input_df = preprocess_input(properties)
        preds = predict(input_df)
        return {"predictions": preds}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
