# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the API"}

@app.get("/hello")
def read_hello():
    return {"message": "hello word"}

@app.get("/apprunner")
def apprunner():
    return {"message": "AWS is configured and App Runner successfully"}


