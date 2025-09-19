from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    side = Column(String(10), nullable=False)      # 'left','right','both'
    category = Column(String(20), nullable=False)  # 'strength','mobility','balance'
    target_sets = Column(Integer, nullable=True)
    target_reps = Column(Integer, nullable=True)
    target_hold_sec = Column(Integer, nullable=True)
    schedule_dow = Column(Text, nullable=False, default="[]")  # JSON text
    created_at = Column(DateTime, default=datetime.utcnow)
    sessions = relationship("ExerciseSession", back_populates="exercise", cascade="all, delete")

class ExerciseSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    hold_sec = Column(Integer, nullable=True)
    pain_0_10 = Column(Integer, nullable=True)  # 0..10
    rom_deg = Column(Integer, nullable=True)    # e.g., 0..180
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    exercise = relationship("Exercise", back_populates="sessions")
