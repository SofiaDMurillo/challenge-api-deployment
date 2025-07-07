from fastapi import FastAPI, HTTPException
from typing import List, Union

from preprocessing.clean_data import preprocess_input, PropertyInput
from predict.prediction import predict

app = FastAPI()

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
