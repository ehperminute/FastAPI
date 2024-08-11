import uvicorn
from fastapi import FastAPI, Response, Cookie, status
from pydantic import BaseModel
from string import ascii_letters
from random import sample


class User(BaseModel):
    username: str
    password: str


app = FastAPI()

db = {f"user{n}": f"pass{n}" for n in range(5)}
tokens = {}

def gen_token():
    return "".join(sample(ascii_letters, 16))

@app.get("/user")
def getuser(response: Response, session_token=Cookie()):
    if not session_token or session_token not in tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Unauthorized"}
    username = tokens[session_token]
    return {username: db[username]}


@app.post("/login")
def login(user: User, response: Response):
    if user.username not in db:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "user not found"}
    if db[user.username] != user.password:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "invalid password"}
    token = gen_token()
    response.set_cookie(key="session_token", value=token, httponly=True)
    tokens[token] = user.username
    return {"user": user}

@app.post("/signup")
def signup(user: User, response: Response):
    if user.username in db:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "username taken"}
    db[user.username] = user.password
    return {"message": f"account {user.username} created"}

@app.post("/signout")
def signout(response: Response, session_token=Cookie()):
    if not session_token or session_token not in tokens:
        return
    tokens.pop(session_token, None)
    response.delete_cookie("session_token", httponly=True)
    return {"message": "you have successfully logged out"}

@app.get("/users")
def users():
    return db

@app.get("/t")
def get_t():
    return tokens

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8000,
        reload=True
    )
