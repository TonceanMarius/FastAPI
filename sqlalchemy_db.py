from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone

DATABASE_URL = 'sqlite:///./images.db'
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

class User(Base):

    __tablename__ = "Image Generator"

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    image_url = Column(String, nullable = False)
    description = Column(String, nullable = False)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)