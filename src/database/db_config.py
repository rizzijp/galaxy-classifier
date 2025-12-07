from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Usamos el archivo predictions.db que ya tienes en src/database/
DATABASE_URL = "sqlite:///predictions.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
