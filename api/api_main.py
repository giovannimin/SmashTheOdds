# -*- coding: utf-8 -*-
"""
Created on 03/07/2023 13:40
@author: GiovanniMINGHELLI
"""
import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sources.data_pipeline import global_transformer
from sources.preprocessor import get_match_info
from sources.utils import get_root, get_last_model, get_response
import joblib

warnings.filterwarnings("ignore")

project_path = get_root()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/status")
def get_status():
    return {"status": 1} if True else {"status": 0}


@app.get("/predict")
def get_pred(match_id: int):
    model = joblib.load(get_last_model())
    match_info = get_match_info(match_id=match_id)
    try:
        data = global_transformer(match_info[['player1_id', 'player2_id']])
        return get_response(model=model, data=data)
    except TypeError:
        return match_info


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
