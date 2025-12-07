from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

Base = declarative_base()

class PredictionHistory(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    predicted_class = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
