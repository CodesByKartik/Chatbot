from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import openai
from fastapi import Request

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
    return template.TemplateResponse("chat.html", {"request": request})

@app.get("/chat", response_class=JSONResponse)
async def chat(query: str = Query(..., description="Enter a historical question")):
    """FastAPI endpoint to handle user queries."""
    # Fetch the structured response from Groq API
    structured_response = ask_groq(query)
    
    # Return a valid JSON response
    if "error" in structured_response:
        return JSONResponse(status_code=400, content=structured_response)
    
    return structured_response
