from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    guidelines_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    events = relationship("Event", back_populates="brand")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String, nullable=False)
    location = Column(String)
...
    assets = relationship("Asset", back_populates="event")
    generations = relationship("Generation", back_populates="event")
    brand = relationship("Brand", back_populates="events")

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    file_path = Column(String, nullable=False)
    file_type = Column(String) # image, video
    technical_score = Column(Integer)
    marketing_score = Column(Integer)
    justification = Column(String)
    metadata_json = Column(JSON)
    is_selected = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    event = relationship("Event", back_populates="assets")

class Generation(Base):
    __tablename__ = "generations"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    platform = Column(String) # linkedin, instagram, case_study
    content = Column(String)
    qa_report = Column(String)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    event = relationship("Event", back_populates="generations")
