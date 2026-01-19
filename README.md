# Decision Analytics System

A minimal, clean, and smart system to log decisions, track assumptions, and review outcomes.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Dashboard+Preview) 
*(Note: Replace with actual screenshot)*

## Features

### 1. Decision Logging (The Wizard)
- **Step-by-Step Flow**: Break down decisions into context, options, and assumptions.
- **Confidence Scoring**: Visual slider to commit to a confidence level (0-100%).
- **Assumption Tracker**: Log what you believe to be true and validate it later.

### 2. Review System
- **Outcome Tracking**: Rate outcomes (1-5) and compare them with your initial confidence.
- **Lessons Learned**: Dedicated space for reflection.
- **Decision Quality Logic**: Automatically categorizes decisions as "Good", "Poor", or "Neutral" based on process quality vs outcome.

### 3. Analytics
- **Performance Gap**: Visualize the delta between your confidence and reality.
- **Calibration**: Discover if you are overconfident, underconfident, or well-calibrated.

## Tech Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy (Async), JWT Auth.
- **Frontend**: Next.js (App Router), Tailwind CSS, Zustand, Recharts.
- **Infrastructure**: Docker Compose.

## getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.9+

### Quick Start

1. **Start the Database**
   ```bash
   docker-compose up -d
   ```

2. **Run Backend**
   ```bash
   cd backend
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   # source venv/bin/activate
   
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Run Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Visit**: [http://localhost:3000](http://localhost:3000)

## Project Structure

```
├── backend/            # FastAPI app
│   ├── routers/        # API endpoints (Auth, Decisions, Analytics)
│   ├── database.py     # DB connection
│   └── models.py       # SQL Alchemy models
├── frontend/           # Next.js app
│   ├── src/app/        # Pages (Dashboard, Login, New Decision)
│   ├── src/components/ # UI Components (Shadcn-like)
│   └── src/store/      # Zustand state
└── docker-compose.yml  # Postgres service
```

## MVP Scope Completion
- [x] Auth (Register/Login)
- [x] Decision CRUD
- [x] Assumption Tracking
- [x] Review Workflow
- [x] Analytics Dashboard
