# LLM Search Service

A FastAPI microservice that provides natural language search over an ingredient catalog using Google Gemini.

---

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.13
- **LLM Provider**: Google Gemini (`gemini-2.0-flash`)
- **Server**: Uvicorn

---

## Getting Started

### 1. Create and activate virtual environment

```bash
cd llm-search-service
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file:

```env
GEMINI_API_KEY=your-api-key-here
```

### 4. Start the service

```bash
uvicorn main:app --port 8000 --reload
```

### 5. Verify it's running

```bash
GET http://localhost:8000/health
```

Expected response:
```json
{ "status": "ok" }
```

---

## API Endpoints

### `POST /search`

Accepts a natural language query and a product catalog, returns matched product IDs.

**Request body:**
```json
{
  "query": "I need an organic freeze dried fruit for a smoothie line",
  "products": [
    {
      "item_id": "HV-STR-80P",
      "listing": "Freeze-Dried Strawberry Powder, Organic — Harvest Valley Co.",
      "category": "Fruits",
      "supplier": "Harvest Valley Co.",
      "certifications": ["USDA Organic", "OU-D Kosher"],
      "suggested_use": "Smoothie mixes, nutrition bars",
      "notes": "Vibrant red color.",
      "details": { "form": "Powder", "process": "Freeze-Dried" }
    }
  ]
}
```

**Response:**
```json
{
  "matched_ids": ["HV-STR-80P", "HV-WBB-WH"],
  "query": "I need an organic freeze dried fruit for a smoothie line"
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{ "status": "ok" }
```

---

## How It Works

1. The main NestJS API calls `POST /search` with the buyer's query and the full product catalog
2. The service builds a prompt with the catalog and query and sends it to Gemini
3. Gemini returns a JSON array of matching `item_ids`
4. The service parses and returns them to the main API
5. The main API fetches the full product details from PostgreSQL and returns them to the buyer

---