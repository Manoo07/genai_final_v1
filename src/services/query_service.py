from sqlalchemy.orm import Session
from src.dao.query_dao import QueryDAO
from src.dao.user_dao import UserDAO
from fastapi import HTTPException, Response
from src.services.gen_ai_service import GenAiService
from fastapi.responses import JSONResponse
import uuid


class QueryService:
    def __init__(self, db: Session):
        self.query_dao = QueryDAO(db)
        self.gen_ai = GenAiService(db)
    
    async def generate_response(self, request,user_id,id):
        user_query = await self.fetch_query(request)
        if(not id):
            session_id = str(uuid.uuid4())
        else:
            session_id = id
        task_id = await self.query_dao.add_record_to_db(user_id, user_query,session_id)
        await self.query_dao.update_status(task_id, 'Inprogress')

        generated_response = await self.gen_ai.generate_response(user_query, user_id, session_id)
        response = await self.query_dao.fetch_session_chat(session_id)
        #  = previous_chat
        print(response)
        await self.query_dao.update_answer_field(task_id, generated_response)
        await self.query_dao.update_status(task_id, 'Completed')
        return {'bot':generated_response,'session_id':session_id}
    
    async def fetch_query(self, request):
        data = await request.json()
        return data.get('user', None)

    
