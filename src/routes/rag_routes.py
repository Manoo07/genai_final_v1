from fastapi import FastAPI, APIRouter, HTTPException, Depends, status,Header, Query,Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
import faiss
from langchain_community.document_loaders import PyPDFLoader
import tiktoken
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import pathlib
import aiofiles
from fastapi import File, UploadFile
from ..services.rag_services.rag_service import RagService

router = APIRouter()

uploads_dir = pathlib.Path("uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)

@router.post('/upload/pdf')
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
        raise HTTPException(status_code=500, detail=f"There was an error uploading the file: {str(e)}")

@router.post('/query/pdf/{filename:path}/{user_id}/{session_id}')
async def query_pdf(filename: str, request: Request,session_id,user_id):
    data = await request.json()
    user_query = data.get('user',None)

    return await RagService().rag_response(user_query,user_id,session_id,filename)