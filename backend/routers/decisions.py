from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime
import models, schemas, database, auth_utils

router = APIRouter(
    prefix="/decisions",
    tags=["decisions"],
)

async def get_decision_or_404(id: int, user: models.User, db: AsyncSession):
    result = await db.execute(
        select(models.Decision)
        .options(
            selectinload(models.Decision.options),
            selectinload(models.Decision.assumptions),
            selectinload(models.Decision.review)
        )
        .filter(models.Decision.id == id, models.Decision.user_id == user.id)
    )
    decision = result.scalars().first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

@router.post("/", response_model=schemas.Decision)
async def create_decision(
    decision: schemas.DecisionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    db_decision = models.Decision(
        user_id=current_user.id,
        title=decision.title,
        category=decision.category,
        description=decision.description,
        confidence_score=decision.confidence_score,
        expected_outcome=decision.expected_outcome,
        decision_date=decision.decision_date or datetime.utcnow(),
        review_date=decision.review_date
    )
    db.add(db_decision)
    await db.commit()
    await db.refresh(db_decision)

    # Add options
    for opt in decision.options:
        db_option = models.Option(
            decision_id=db_decision.id,
            option_name=opt.option_name,
            reasoning=opt.reasoning
        )
        db.add(db_option)
    
    # Add assumptions
    for asm in decision.assumptions:
        db_asm = models.Assumption(
            decision_id=db_decision.id,
            assumption_text=asm.assumption_text,
            status=asm.status
        )
        db.add(db_asm)
    
    await db.commit()
    # Re-fetch with relationships
    return await get_decision_or_404(db_decision.id, current_user, db)

@router.get("/", response_model=List[schemas.Decision])
async def get_decisions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    result = await db.execute(
        select(models.Decision)
        .filter(models.Decision.user_id == current_user.id)
        .options(
            selectinload(models.Decision.options),
            selectinload(models.Decision.assumptions),
            selectinload(models.Decision.review)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/{id}", response_model=schemas.Decision)
async def get_decision(
    id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    return await get_decision_or_404(id, current_user, db)

@router.put("/{id}", response_model=schemas.Decision)
async def update_decision(
    id: int,
    decision_update: schemas.DecisionBase,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    db_decision = await get_decision_or_404(id, current_user, db)
    
    for key, value in decision_update.dict(exclude_unset=True).items():
        setattr(db_decision, key, value)
    
    await db.commit()
    await db.refresh(db_decision)
    return db_decision

@router.post("/{id}/assumptions", response_model=schemas.Assumption)
async def add_assumption(
    id: int,
    assumption: schemas.AssumptionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    # Verify ownership
    await get_decision_or_404(id, current_user, db)
    
    db_assumption = models.Assumption(
        decision_id=id,
        assumption_text=assumption.assumption_text,
        status=assumption.status
    )
    db.add(db_assumption)
    await db.commit()
    await db.refresh(db_assumption)
    return db_assumption

@router.patch("/assumptions/{assumption_id}", response_model=schemas.Assumption)
async def update_assumption_status(
    assumption_id: int,
    update: schemas.AssumptionUpdate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    # Find assumption and verify decision ownership
    result = await db.execute(
        select(models.Assumption)
        .join(models.Decision)
        .filter(models.Assumption.id == assumption_id, models.Decision.user_id == current_user.id)
    )
    db_assumption = result.scalars().first()
    if not db_assumption:
        raise HTTPException(status_code=404, detail="Assumption not found")
    
    db_assumption.status = update.status
    await db.commit()
    await db.refresh(db_assumption)
    return db_assumption

@router.post("/{id}/review", response_model=schemas.Review)
async def review_decision(
    id: int,
    review: schemas.ReviewCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    db_decision = await get_decision_or_404(id, current_user, db)
    
    if db_decision.review:
         raise HTTPException(status_code=400, detail="Decision already reviewed")

    db_review = models.Review(
        decision_id=id,
        outcome_rating=review.outcome_rating,
        outcome_notes=review.outcome_notes,
        lessons_learned=review.lessons_learned
    )
    db.add(db_review)
    
    # Logic: Calculate Decision Quality
    # Simple logic: 
    # High Confidence (>=80) + High Rating (>=4) = Good Decision
    # High Confidence (>=80) + Low Rating (<=2) = Poor Decision (Overconfidence)
    # Low Confidence (<=40) + High Rating (>=4) = Poor Decision (Underconfidence/Luck)
    # Low Confidence (<=40) + Low Rating (<=2) = Good Decision (Calibrated)
    # Else: Mixed/Neutral
    
    conf = db_decision.confidence_score
    rating = review.outcome_rating
    
    quality = "Neutral"
    outcome_q = "Average"
    
    if rating >= 4:
        outcome_q = "Good"
        if conf >= 70: quality = "Good"
        elif conf <= 40: quality = "Poor" # Luck
    elif rating <= 2:
        outcome_q = "Poor"
        if conf >= 70: quality = "Poor" # Overconfidence
        elif conf <= 40: quality = "Good" # Calibrated caution
        
    db_decision.decision_quality = quality
    db_decision.outcome_quality = outcome_q
    
    await db.commit()
    await db.refresh(db_review)
    return db_review
