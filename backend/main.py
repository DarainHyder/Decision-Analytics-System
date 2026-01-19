from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, decisions, analytics
from database import engine, Base, AsyncSessionLocal

app = FastAPI(
    title="Decision Analytics System",
    description="Backend API for Decision Analytics System MVP",
    version="0.1.0"
)

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(decisions.router)
app.include_router(analytics.router)

# Scheduler for Review Reminders
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from datetime import datetime
import models

scheduler = AsyncIOScheduler()

async def check_due_reviews():
    # In a real app, this would send emails.
    # Here we just log or tag them.
    # For MVP: We print to console.
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(models.Decision.title, models.User.email)
            .join(models.User)
            .filter(
                models.Decision.review_date <= datetime.utcnow(),
                models.Decision.review == None
            )
        )
        due_decisions = result.fetchall()
        if due_decisions:
            print(f"--- [REMINDER] Found {len(due_decisions)} decisions due for review! ---")
            for title, email in due_decisions:
                print(f"User: {email} | Decision: {title}")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Start Scheduler
    scheduler.add_job(check_due_reviews, "interval", minutes=60)
    scheduler.start()


@app.get("/")
async def root():
    return {"message": "Welcome to Decision Analytics System API"}
