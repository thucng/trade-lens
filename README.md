# TradeLens

Global trade insights by country. An English-only dashboard for exploring a country's import/export situation over the latest 5 available official years (annual, HS2 classification, USD).

## Stack

- **Frontend:** Vite + React + TypeScript, TanStack Query, Recharts, Tailwind CSS
- **Backend:** FastAPI + Pydantic, local JSON storage
- **Data source:** UN Comtrade (integration pending; currently mock data for USA)

## Run locally

Backend (http://localhost:8000):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (http://localhost:5173):

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — you'll be redirected to `/countries`. USA is the only cached country so far; open its dashboard to see the full UI.

## API

| Endpoint | Description |
|---|---|
| `GET /api/health` | Health check |
| `GET /api/countries` | All supported countries |
| `GET /api/countries/cached` | Countries with dashboard data |
| `GET /api/countries/{iso3}` | Country metadata |
| `GET /api/countries/{iso3}/dashboard?years=5` | Processed dashboard JSON |

Interactive docs: http://localhost:8000/docs
