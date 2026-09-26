from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
