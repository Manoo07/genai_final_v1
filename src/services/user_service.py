from sqlalchemy.orm import Session
from src.dao.user_dao import UserDAO
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse

class UserService:
    def __init__(self, db: Session):
        self.user_dao = UserDAO(db)

    async def fetch_session_chat(self, request):
        session_id = await self.fetch_session_id(request)
        response_dictionary = await self.user_dao.fetch_session_chat(session_id)
        return JSONResponse(content = response_dictionary)
    
    async def fetch_user_conversations(self,request,user_id):
        return await self.user_dao.fetch_user_conversations(request,user_id)

    async def fetch_user_conversation(self,request,user_id,session_id):
        return await self.user_dao.fetch_user_conversations_session_id(request,user_id,session_id)
    
    async def fetch_session_id(self, request):
        data = await request.json()
        return data.get('session_id', None)