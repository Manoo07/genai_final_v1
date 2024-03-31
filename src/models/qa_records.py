from sqlalchemy import  Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum
from src.config.database import base
from sqlalchemy.sql import func

class QARecords(base):
    __tablename__ = "qa_records"
    Id = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, nullable=False)
    SessionId = Column(Text,nullable=True)
    Question = Column(Text, nullable=False)
    Answer = Column(Text)
    Status = Column(Enum('Pending', 'Inprogress', 'Completed', 'Failed'))
    CreatedAt = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    UpdatedAt = Column(TIMESTAMP)