from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.services.query_service import QueryService

class QueryController:
    def __init__(self, db : Session):
        self.query_service = QueryService(db)

    async def generate_response(self, request,user_id,id):
        return await self.query_service.generate_response(request,user_id,id)
    

