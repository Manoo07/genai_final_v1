from fastapi import Depends
from typing import Tuple
from src.config.database import engine,session_local
from sqlalchemy.orm import Session
from src.config.database import base
from src.models.qa_records import QARecords
from src.models.realestate_data import RealEstate


models = [QARecords, RealEstate]

base.metadata.create_all(bind=engine, tables=[model.__table__ for model in models])

def get_db() -> Tuple[Session, ...]:   # type: ignore
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = (Session, Depends(get_db))