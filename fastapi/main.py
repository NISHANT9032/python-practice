from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()



app = FastAPI()

@app.get("/")

def read_root():
    return {"Hello": "World"}  

@app.get("/margin")
def margin(revenue : float , expenses: float):
    profit = revenue - expenses
    margin = (profit / revenue) * 100   
    return {"Profit": profit, 
            "Margin": margin
            }

class Review(BaseModel):
    text: str

class Sentiment(BaseModel):
    label: str          
    score: int   

@app.post("/sentiment")
def analyze_sentiment(review: Review):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=(
            "Find the sentiment of this customer review. "
            "label must be 'positive', 'negative', or 'neutral'. "
            "score must be a number from 1 (very bad) to 5 (very good). "
            f"Review: {review.text}"
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Sentiment,
        ),
    )
    return response.parsed

class ProductRequest(BaseModel):
    product: str



@app.post("/tagline")
def generate_tagline(request: ProductRequest):
    prompt = f"""
    Create a short, catchy, one-line marketing tagline for:
    {request.product}

    Also provide one matching emoji.

    Return only valid JSON in this format:
    {{
        "tagline": "Your catchy tagline",
        "emoji": "😊"
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text