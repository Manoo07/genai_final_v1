from fastapi import APIRouter, Depends, HTTPException, Request,FastAPI
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.query_controller import QueryController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/query/{user_id}/{id}')
async def generate_response(request : Request,user_id:int,id, db : Session = Depends(get_db)):
    return await QueryController(db).generate_response(request,user_id,id)

@router.post('/query/{user_id}')
async def generate_response(request : Request,user_id:int, db : Session = Depends(get_db)):
    id=None
    return await QueryController(db).generate_response(request,user_id,id)

