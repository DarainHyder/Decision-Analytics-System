import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User, Decision

async def check_data():
    async with AsyncSessionLocal() as db:
        print("\n--- 📊 Database Inspection ---\n")
        
        # Check Users
        print("👤 Users:")
        result = await db.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"   - ID: {user.id} | Name: {user.name} | Email: {user.email}")
        
        print("\n" + "-"*30 + "\n")

        # Check Decisions
        print("🧠 Decisions:")
        result = await db.execute(select(Decision))
        decisions = result.scalars().all()
        
        if not decisions:
            print("   (No decisions found)")
        
        for d in decisions:
            print(f"   - ID: {d.id} | Title: '{d.title}' | Confidence: {d.confidence_score}%")
            print(f"     Category: {d.category}")
            print(f"     Expected Outcome: {d.expected_outcome}")
            print("")

if __name__ == "__main__":
    asyncio.run(check_data())
