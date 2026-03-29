from fastapi import FastAPI, Request
import uvicorn
import os
import httpx
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from fastapi.responses import Response
from src.TextInsightMlopsPipeline.pipeline.prediction import PredictionPipeline
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

class GenerateRequest(BaseModel):
    type: str

class EvaluateRequest(BaseModel):
    original_text: str
    summary: str

async def call_mistral(prompt: str) -> str:
    """Call Mistral API directly via HTTP."""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(MISTRAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load model ONCE at startup (singleton) — not on every request
pipeline = PredictionPipeline()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
       return templates.TemplateResponse(request, "index.html")

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful!")
    except Exception as e:
        return Response(f"Error Occurred: {e}")

@app.post("/predict")
async def predict_route(text: str):
    try:
        summary = pipeline.predict(text)
        return {"summary": summary}
    except Exception as e:
        raise e

@app.post("/generate")
async def generate_route(req: GenerateRequest):
    try:
        if req.type == "story":
            prompt = "Generate a short, engaging 2-person story. Max 200 words. Do not include intro/outro. Just the story text."
        elif req.type == "dialogue":
            prompt = "Generate a short dialogue between two people. Max 150 words. Format it like 'Person1: ...\\nPerson2: ...'. No intro/outro."
        else:
            prompt = "Generate a random short conversation or story. Max 150 words. Be creative. No intro/outro."

        text = await call_mistral(prompt)
        return {"text": text}
    except Exception as e:
        return {"text": f"Error: {str(e)}"}

@app.post("/evaluate")
async def evaluate_route(req: EvaluateRequest):
    try:
        prompt = f"Original text:\n{req.original_text}\n\nSummary:\n{req.summary}\n\nEvaluate the quality of the summary out of 10 based on the original text. Point out any missing info or hallucinations. Keep it to one short paragraph."
        evaluation = await call_mistral(prompt)
        return {"evaluation": evaluation}
    except Exception as e:
        return {"evaluation": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)