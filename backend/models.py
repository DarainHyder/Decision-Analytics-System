from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    decisions = relationship("Decision", back_populates="owner")

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    category = Column(String)
    description = Column(Text, nullable=True)
    confidence_score = Column(Integer)  # 0-100
    expected_outcome = Column(Text, nullable=True)
    decision_date = Column(DateTime, default=datetime.utcnow)
    review_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Derived fields for logic later
    decision_quality = Column(String, nullable=True) # good / poor
    outcome_quality = Column(String, nullable=True) # good / poor

    owner = relationship("User", back_populates="decisions")
    options = relationship("Option", back_populates="decision")
    assumptions = relationship("Assumption", back_populates="decision")
    review = relationship("Review", back_populates="decision", uselist=False)

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"))
    option_name = Column(String)
    reasoning = Column(Text, nullable=True)

    decision = relationship("Decision", back_populates="options")

class Assumption(Base):
    __tablename__ = "assumptions"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"))
    assumption_text = Column(String)
    status = Column(String, default="pending") # pending / true / false

    decision = relationship("Decision", back_populates="assumptions")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"))
    outcome_rating = Column(Integer) # 1-5
    outcome_notes = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    decision = relationship("Decision", back_populates="review")
