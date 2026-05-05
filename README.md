# os-demo-this-
made changes in readme file
<br>
Author-piyush modani

---

## Backend (FastAPI) – AI Financial Mentor

### Setup
1. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY if you want real model responses
```

### Run the API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoint
POST `/chat`

Request body:
```json
{
  "user_id": "user-123-balanced",
  "message": "How should I rebalance given my horizon?"
}
```

Response body (example):
```json
{
  "mentor_response": "...",
  "risk_profile": "Balanced",
  "allocation": {"Stocks": 60.0, "Bonds": 35.0, "Cash": 5.0},
  "disclaimer": "This conversation provides educational information only ..."
}
```

### Personas (dummy data)
- Append suffix to `user_id` to simulate:
  - `-conservative`
  - `-aggressive`

If no suffix is used, a balanced profile is returned.
