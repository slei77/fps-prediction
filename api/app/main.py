import joblib
import numpy as np
import pandas as pd
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="FPS Prediction API")

preprocessor = joblib.load("model/preprocessor.joblib")
models = joblib.load("model/models.joblib")

genres = ['Adventure', 'Brawler', 'Indie', 'Puzzle', 'RPG', 
            'Racing', 'Real Time Strategy', 'Shooter', 'Simulator', 
            'Sport', 'Strategy', 'Tactical', 'Turn Based Strategy']

class InputData(BaseModel):
    Preset: Literal['low', 'medium', 'high', 'ultra']
    boostClock: int
    shaders: int
    tmus: int
    rops: int
    architecture: str
    memorySize: int
    memoryBandwidth: int
    Resolution: int
    Release_Date: int
    Adventure: bool
    Brawler: bool
    Indie: bool
    Puzzle: bool
    RPG: bool
    Racing: bool
    RTS: bool = Field(alias="Real Time Strategy")
    Shooter: bool
    Simulator: bool
    Sport: bool
    Strategy: bool
    Tactical: bool
    TBS: bool = Field(alias="Turn Based Strategy")

@app.get("/")
def home():
    return {"message": "The FPS Prediction API is running!"}

@app.post("/predict")
def predict_fps(data: InputData):
    input_df = pd.DataFrame([data.model_dump(by_alias=True)])
    input_df[genres] = input_df[genres].astype(int)
    input_processed = preprocessor.transform(input_df)
    
    predictions = []
    for model in models:
        pred = model.predict(input_processed)[0]
        predictions.append(pred)

    prediction = float(sum(predictions) / len(predictions))
    prediction = np.maximum(prediction, 0) ** (10)

    return {"prediction": prediction}