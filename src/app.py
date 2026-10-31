import os
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from src.schemas import GridLoadInput, GridLoadPrediction

MODEL_PATH = "model.joblib"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if not os.path.exists(MODEL_PATH):
        from src.model import train_and_save_model
        train_and_save_model(MODEL_PATH)
    model = joblib.load(MODEL_PATH)
    yield

app = FastAPI(
    title="German Power Grid Load Forecasting API",
    description="Microservice providing real-time load estimation for TSO balancing.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=GridLoadPrediction)
def predict(payload: GridLoadInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model artifact is not loaded.")
    
    input_df = pd.DataFrame([payload.model_dump()])
    prediction = model.predict(input_df)[0]
    
    return GridLoadPrediction(
        predicted_load_mw=round(float(prediction), 2),
        model_version="random-forest-v1"
    )