from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
import models, database, auth_utils

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)

@router.get("/overview")
async def get_analytics(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    # Total decisions
    result = await db.execute(
        select(func.count(models.Decision.id)).filter(models.Decision.user_id == current_user.id)
    )
    total_decisions = result.scalar()
    
    # Reviewed vs Pending
    result = await db.execute(
        select(func.count(models.Decision.id))
        .filter(models.Decision.user_id == current_user.id, models.Decision.decision_quality.isnot(None))
    )
    reviewed = result.scalar()
    pending = total_decisions - reviewed
    
    # Avg Confidence vs Avg Outcome
    # We need to join with Review to get outcome
    res_conf = await db.execute(
        select(func.avg(models.Decision.confidence_score))
        .filter(models.Decision.user_id == current_user.id)
    )
    avg_confidence = res_conf.scalar() or 0
    
    res_outcome = await db.execute(
        select(func.avg(models.Review.outcome_rating))
        .join(models.Decision)
        .filter(models.Decision.user_id == current_user.id)
    )
    avg_outcome = res_outcome.scalar() or 0
    
    return {
        "total_decisions": total_decisions,
        "reviewed_decisions": reviewed,
        "pending_decisions": pending,
        "average_confidence": round(avg_confidence, 1),
        "average_outcome": round(avg_outcome, 1)
    }
