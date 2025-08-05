import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from flask import Flask, jsonify
from fastapi.responses import JSONResponse
from utils.db_utils import client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/user-details", response_class=HTMLResponse)
async def get_user_details(request: Request):
    return templates.TemplateResponse("user_details.html", {"request": request})

@app.post("/user-details")
async def post_user_details(request: Request, username: str = Form(...), email: str = Form(...)):
    
    db = client["test"]
    collection = db["user_info"]
    try:
        collection.insert_one({"username": username, "email": email})
        return templates.TemplateResponse(
            "success.html",
            {"request": request, "username": username}
        )
    except Exception as e:
        error_message = str(e)
        return templates.TemplateResponse(
            "user_details.html",
            {"request": request, "error": error_message}
        )

@app.get("/api")
async def api():
    data = []
    try:
        with open("user_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    return JSONResponse(content=data)
