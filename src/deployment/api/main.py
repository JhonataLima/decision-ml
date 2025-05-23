from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

pipeline = joblib.load("models/pipeline_transformacao.pkl")
modelo = joblib.load("models/random_forest_model.pkl")

app = FastAPI(title="Decision ML API", version="1.0")

class InputData(BaseModel):
    dados: dict

@app.get("/")
def read_root():
    return {"mensagem": "API de Previsão funcionando!"}

@app.post("/predict")
def predict(input_data: InputData):
    try:
        df = pd.DataFrame([input_data.dados])

        X_transformed = pipeline.transform(df)

        pred = modelo.predict(X_transformed)

        return {"previsao": int(pred[0])}
    except Exception as e:
        return {"erro": str(e)}
