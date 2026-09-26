import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import google.generativeai as genai

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")
templates = Jinja2Templates(directory="templates")

# Configure Gemini API Key
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"Create a personalized 7-day workout plan for {username}, age {age}, with a goal of {goal} and {intensity} workout intensity. Include recovery tips."
        
        response = model.generate_content(prompt)
        workout_plan = response.text

        return templates.TemplateResponse("index.html", {
            "request": request,
            "username": username,
            "workout_plan": workout_plan
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })
