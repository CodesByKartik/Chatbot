from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import httpx
import spacy
from dotenv import load_dotenv
import wikipediaapi

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Configure Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Function to call Groq API asynchronously
async def ask_groq(question: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json={
                    "model": "mixtral-8x7b-32768",
                    "messages": [
                        {"role": "system", "content": "You are a historical chatbot."},
                        {"role": "user", "content": question}
                    ],
                },
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
            )

        if response.status_code != 200:
            return {"error": f"Groq API Error: {response.status_code} - {response.text}"}

        return response.json()

    except httpx.RequestError as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Function to fetch relevant information from Wikipedia
def fetch_wikipedia_data(query: str) -> str:
    wiki = wikipediaapi.Wikipedia("en", user_agent="Chatbot-App/1.0 (Python; no-website)")
    page = wiki.page(query)
    
    if page.exists():
        return page.text  # Return the full content of the Wikipedia page
    else:
        return "Sorry, no relevant information found on Wikipedia."

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weapons", response_class=HTMLResponse)
async def weapons_page(request: Request):
    return templates.TemplateResponse("weapons.html", {"request": request})

@app.get("/crafts", response_class=HTMLResponse)
async def crafts_page(request: Request):
    return templates.TemplateResponse("crafts.html", {"request": request})

@app.get("/EngineeringTech", response_class=HTMLResponse)
async def engineering_tech_page(request: Request):
    return templates.TemplateResponse("Engg&Tech.html", {"request": request})

@app.get("/ChatPage", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat", response_class=JSONResponse)
async def chat(query: str = Query(..., description="Enter a historical question")):
    structured_response = await ask_groq(query)

    # Debug the response
    print("Groq API Response:", structured_response)

    if "error" in structured_response:
        # If Groq API fails, try Wikipedia as a fallback
        wiki_response = fetch_wikipedia_data(query)
        return {"response": wiki_response}

    try:
        assistant_response = structured_response["choices"][0]["message"]["content"]
        return {"response": assistant_response}
    except (KeyError, IndexError) as e:
        return JSONResponse(status_code=500, content={"error": f"Invalid response format: {str(e)}"})
