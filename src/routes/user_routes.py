from fastapi import APIRouter, Depends, HTTPException, Request,File, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.user_controller import UserController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import shutil
import os
import pathlib
import aiofiles

app = FastAPI(upload_max_size=1000000000)

uploads_dir = pathlib.Path("uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.get('/user/session')
async def fetch_session_chat(request : Request, db : Session = Depends(get_db)):
    return await UserController(db).fetch_session_chat(request)

@router.get('/user/{user_id}/conversations')
async def fetch_user_conversations(request : Request,user_id:int, db : Session = Depends(get_db)):
    return await UserController(db).fetch_user_conversations(request,user_id)

@router.get('/user/{user_id}/conversation/{session_id}')
async def fetch_user_conversation(request : Request,user_id:int,session_id, db : Session = Depends(get_db)):
    return await UserController(db).fetch_user_conversation(request,user_id,session_id)


@router.post("/upload/")        
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        file_name = pathlib.Path(uploads_dir, file.filename)
        async with aiofiles.open(file_name, 'wb') as f:
            contents = await file.read()  # Read the file contents
            await f.write(contents)  # Write the contents to the file
        
        return {
            "filename": file.filename,
            "content_type": file.content_type
        }
    
    except Exception as e:
        # Handle any errors that occur during file upload
        raise HTTPException(status_code=500, detail=f"There was an error uploading the file: {str(e)}")