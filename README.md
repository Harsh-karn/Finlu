# FlowMoney 💸

A comprehensive, production-ready UPI expense tracking and money management application. FlowMoney automatically tracks your expenses from three sources:
1. Android SMS auto-parsing
2. Bank statement PDF/CSV upload with AI extraction (Gemini)
3. Manual transactions

## Tech Stack
- **Backend:** FastAPI, PostgreSQL, Redis, Celery, Alembic
- **Frontend:** Next.js 15 (App Router), Tailwind CSS, shadcn/ui, Zustand, Recharts
- **Android App:** Kotlin, MVVM, WorkManager, OkHttp
- **AI/LLM:** Google Gemini 1.5 Flash

## Local Development Setup

### 1. Prerequisites
- Docker and Docker Compose
- Node.js (v18+)
- Python 3.11+
- A Google Gemini API Key

### 2. Start the Backend Infrastructure
The database (PostgreSQL) and cache (Redis) run in Docker along with the backend API and Celery workers.
```bash
# Rename the env example (if provided) and add your GEMINI_API_KEY
# Start all backend containers
docker-compose up -d --build
```
The backend API will be available at `http://localhost:8000`.
You can view the interactive Swagger API documentation at: **[http://localhost:8000/docs](http://localhost:8000/docs)**

### 3. Start the Frontend
The Next.js frontend connects to the FastAPI backend.
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:3000`.

### 4. Android App
The Android app is located in the `android/` directory. You can open this directory in Android Studio.
The app listens for SMS broadcasts, parses UPI messages using regex, and uses a `WorkManager` background job to push the transactions securely to your local FastAPI backend.

## Features Implemented
- ✅ Full User Authentication (JWT)
- ✅ Regex-based SMS Parser for Indian Banks
- ✅ AI Categorization via Gemini 1.5 Flash
- ✅ PDF Bank Statement Parsing
- ✅ Next.js 15 Dashboard with Analytics
- ✅ Spending Budgets & Threshold Alerts
- ✅ Android SMS sync background worker

*(Demo GIF goes here)*
