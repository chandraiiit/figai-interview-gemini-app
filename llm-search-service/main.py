from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="LLM Search Service")


class Product(BaseModel):
    item_id: str
    listing: str
    category: str
    supplier: str
    certifications: list[str]
    suggested_use: str | None
    notes: str | None
    details: dict


class SearchRequest(BaseModel):
    query: str
    products: list[Product]


class SearchResponse(BaseModel):
    matched_ids: list[str]
    query: str


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    catalog = [p.model_dump() for p in request.products]

    prompt = f"""
You are a helpful ingredient sourcing assistant.
Given the following product catalog and a buyer's natural language query, return the item_ids of the most relevant products.

Catalog:
{json.dumps(catalog, indent=2)}

Buyer query: "{request.query}"

Rules:
- Return ONLY a valid JSON array of item_id strings, e.g. ["HV-STR-80P", "HV-WBB-WH"]
- Return an empty array if nothing matches
- Do not include any explanation or markdown, only the JSON array
"""

    try:
        result = model.generate_content(prompt)
        text = result.text.strip()

        # strip markdown code blocks if Gemini wraps response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        matched_ids = json.loads(text)

        if not isinstance(matched_ids, list):
            raise ValueError("Response is not a list")

        return SearchResponse(matched_ids=matched_ids, query=request.query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM search failed: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok"}