
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from pydantic import BaseModel



# Now you can use bcrypt functions, e.g. bcrypt.hashpw() or bcrypt.checkpw()

api_user = FastAPI()
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


@api_user.get("/login")
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]["password"])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        # If login is successful, redirect the user to another endpoint (e.g., "/user")
    response= RedirectResponse(url="/user")
    return response


@api_user.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return "Hello"


@api_user.post("/user")
def add_user(user_info: UserCreate):

    new_user = {
        "username": user_info.username,
        "password": pwd_context.hash(user_info.password),
    }
    users[user_info.username] = new_user
    return {"message": "User added successfully"}

@api_user.post("/logout")
def logout_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Here, you can perform any necessary cleanup or token/session invalidation logic.
    # For a simple logout, you can simply return a message.
    return {"message": "Logout successful"}

