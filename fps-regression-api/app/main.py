import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="FPS Prediction API")

preprocessor = joblib.load("model/preprocessor.joblib")
models = joblib.load("model/models.joblib")

class InputData(BaseModel):
    Preset: str
    boostClock: int
    shaders: int
    tmus: int
    rops: int
    architecture: str
    memorySize: int
    memoryBandwidth: int
    Resolution: int
    Release_Date: int
    Adventure: int
    Brawler: int
    Indie: int
    Puzzle: int
    RPG: int
    Racing: int
    RTS: int = Field(alias="Real Time Strategy")
    Shooter: int
    Simulator: int
    Sport: int
    Strategy: int
    Tactical: int
    TBS: int = Field(alias="Turn Based Strategy")

@app.get("/")
def home():
    return {"message": "The FPS Prediction API is running!"}

@app.post("/predict")
def predict_fps(data: InputData):
    input_df = pd.DataFrame([data.model_dump(by_alias=True)])
    input_processed = preprocessor.transform(input_df)
    
    predictions = []
    for model in models:
        pred = model.predict(input_processed)[0]
        predictions.append(pred)

    return {"prediction": float(sum(predictions) / len(predictions))}