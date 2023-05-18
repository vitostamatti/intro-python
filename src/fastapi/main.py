from dataclasses import asdict
from typing import Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import pandas as pd
from pydantic import BaseModel
from sklearn.base import BaseEstimator
from sklearn.cluster import KMeans
import pickle
from sklearn.cluster import KMeans



def load_model(path) -> KMeans:
    with open(path, "rb") as f:
        return pickle.load(f)
    
class PredictionRequest(BaseModel):
    user_id: str
    frequency: float
    recency: float
    T: float
    monetary_value: float


class PredictionResponse(BaseModel):
    user_id: str
    cluster: int


model = load_model(path="../../data/models/rfm-kmeans.pkl")


app = FastAPI(
    title="Predictions Api",
    description="Minimal Api to run predictions on customers"
)


@app.get("/", include_in_schema=False)
async def index():
    response = RedirectResponse(url='/docs')
    return response


@app.post("/predict", summary="run predictions")
def read_item(req:PredictionRequest) -> PredictionResponse:
    """Returns the corresponding cluster of the given user info
    """
    X = pd.DataFrame([req.dict()]).drop(columns=['user_id'])
    cluster = model.predict(X)
    return PredictionResponse(
        user_id=req.user_id,
        cluster=cluster
    )