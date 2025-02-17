from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import openai
from fastapi import Request
import httpx
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

# Configure Jinja2 templates directory
template = Jinja2Templates(directory="templates")

# Serve static files (e.g., for CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Groq API Configuration
GROQ_API_KEY = "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"
openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"


# Weather API Configuration
TWC_API_KEY = "a77d354c6b5b4546a5c151114251502"
TWC_API_BASE = "http://api.weatherapi.com/v1"
LOCATION = "Mumbai"  # Change to your desired location
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(TWC_API_KEY)
@app.get("/api/weather", response_class=JSONResponse)
async def get_weather():
    try:
        """Fetch current weather data from Weather API"""
        url = f"{TWC_API_BASE}/current.json?key={TWC_API_KEY}&q={LOCATION}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print(response)  # To check the status and headers of the response

        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={"error": "Failed to fetch weather data"})

        return response.json()

    except Exception as e:
        # Log error to help identify issues
        return {"error": f"Error occurred: {str(e)}"}
    
@app.get("/api/weather/history", response_class=JSONResponse)
async def get_weather():
    try:
        """Fetch current weather data from Weather API"""
        url = f"{TWC_API_BASE}/history.json?key={TWC_API_KEY}&q={LOCATION}&days=14"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print(response)  # To check the status and headers of the response

        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={"error": "Failed to fetch weather data"})

        return response.json()

    except Exception as e:
        # Log error to help identify issues
        return {"error": f"Error occurred: {str(e)}"}

def ask_groq(question: str) -> dict:
    """Query Groq API (Mixtral model) for an AI-generated response in a structured format."""
    try:
        # Prepare request to the Groq API (Mixtral model)
        response = openai.ChatCompletion.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a historical chatbot. Provide detailed and accurate historical insights."},
                {"role": "user", "content": f"User's Question: {question}"}
            ]
        )
        
        chatbot_answer = response.choices[0].message['content']
        
        # Structure the response
        structured_response = {
            "answer": chatbot_answer,
            "context": "This answer is based on historical knowledge and context.",
        }
        
        return structured_response
    
    except Exception as e:
        # Log error to help identify issues
        return {"error": f"Error occurred: {str(e)}"}


@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/weapons", response_class=HTMLResponse)
async def get_html(request: Request):
    return template.TemplateResponse("weapons.html", {"request": request})

@app.get("/ChatPage", response_class=HTMLResponse)
async def get_html(request: Request):
    return template.TemplateResponse("chat.html", {"request": request})

@app.get("/crafts", response_class=HTMLResponse)
async def get_html(request: Request):
    return template.TemplateResponse("crafts.html", {"request": request})

@app.get("/EngineeringTech", response_class=HTMLResponse)
async def get_html(request: Request):
    return template.TemplateResponse("Engg&Tech.html", {"request": request})

@app.get("/chat", response_class=JSONResponse)
async def chat(query: str = Query(..., description="Enter a historical question")):
    """FastAPI endpoint to handle user queries."""
    # Fetch the structured response from Groq API
    structured_response = ask_groq(query)
    
    # Return a valid JSON response
    if "error" in structured_response:
        return JSONResponse(status_code=400, content=structured_response)
    
    return structured_response
