from sqlalchemy.orm import Session
from src.models.qa_records import QARecords
from fastapi import Response
from sqlalchemy import func
from fastapi.responses import JSONResponse
import json
import uuid
class UserDAO:
    def __init__(self, db:Session):
        self.db = db

    async def fetch_session_chat(self, session_id):

        response_dictionary = {}
        if not session_id:
            session_id = str(uuid.uuid4())
            response_dictionary['session_id'] = session_id
            response_dictionary['previous_chat'] = []
            return response_dictionary

        previous_chat_questions = self.db.query(QARecords.Question).filter(QARecords.SessionId == session_id).all()
        previous_chat_answers = self.db.query(QARecords.Answer).filter(QARecords.SessionId == session_id).all()
        previous_chat = []
        for i in range(len(previous_chat_questions)):
            temp_dict = {}
            temp_dict['user'] = str(previous_chat_questions[i][0])
            temp_dict['bot'] = str(previous_chat_answers[i][0])
            previous_chat.append(temp_dict)
        response_dictionary['session_id'] = session_id
        response_dictionary['previous_chat'] = previous_chat
        return response_dictionary
    

    async def fetch_user_conversations(self, request,user_id):
        sessions = self.db.query(QARecords.SessionId).filter(QARecords.UserId == user_id).all()
        user_conversations = []

        for session_id in sessions:
            session_chat = await self.fetch_session_chat(session_id[0])
            user_conversations.append({'session_id': session_id[0], 'previous_chat': session_chat['previous_chat']})
    
        return JSONResponse(content=user_conversations)
    
    async def fetch_user_conversations_session_id(self, request,user_id,session_id):
        sessions = self.db.query(QARecords.SessionId).filter(QARecords.UserId == user_id).filter(QARecords.SessionId == session_id).all()
        user_conversations = []

        for session_id in sessions:
            session_chat = await self.fetch_session_chat(session_id[0])
            user_conversations.append({'session_id': session_id[0], 'previous_chat': session_chat['previous_chat']})
    
        return JSONResponse(content=user_conversations)



    async def fetch_field(self, request, required_field):
        data = await request.json()
        return data.get(required_field, None)