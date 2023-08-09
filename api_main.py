# -*- coding: utf-8 -*-
"""
Created on 03/07/2023 13:40
@author: GiovanniMINGHELLI, LU6D
"""
import warnings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sources.data_pipeline import global_transformer
from sources.preprocessor import get_match_info
from sources.utils import get_root, get_last_model, get_response
import joblib
import csv
import os
from config import USERS


warnings.filterwarnings("ignore")

project_path = get_root()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {

    "daniel" :{
        "username": "daniel",
        "password": pwd_context.hash('datascientest'),
    },
    "john" : {
        "username" :  "john",
        "password" : pwd_context.hash('secret'),
    },
    "lucie" :{
        "username": "lucie",
        "password" : pwd_context.hash('ravie')
    }
}

class UserCreate(BaseModel):
    #user: Optional[str]= None
    username : str
    password: str


@app.get("/login")
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]["password"])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        # If login is successful, redirect the user to another endpoint (e.g., "/user")
    response= RedirectResponse(url="/predict")
    return response


'''@app.get("/status")
def get_status():
    return {"status": 1}'''

@app.get('/predict/')
def get_pred(match_id: int):
    model = joblib.load(get_last_model())
    match_info = get_match_info(match_id=match_id)
    try:
        data = global_transformer(match_info[['player1_id', 'player2_id']])
        return get_response(model=model, data=data)
    except TypeError:
        return match_info


@app.post("/user")
def add_user(user_info: UserCreate):

    new_user = {
        "username": user_info.username,
        "password": pwd_context.hash(user_info.password),
    }
    #vérification s'il n'est pas déjà existant dans le fichier users.csv

    if users.get(user_info.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    #update du dictionnaire
    users[user_info.username] = new_user
    #ajout d'une ligne dans le fichier users.csv
    with open(os.path.join(get_root(), 'users.csv'), mode="a", newline="") as csvfile:
        fieldnames = ["username", "password"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(new_user)
    return {"message": "User added successfully"}

@app.post("/logout")
def logout_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Here, you can perform any necessary cleanup or token/session invalidation logic.
    # For a simple logout, you can simply return a message.
    return {"message": "Logout successful"}
