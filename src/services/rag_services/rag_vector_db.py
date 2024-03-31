# from fastapi import FastAPI, APIRouter, HTTPException, Depends, status,Header, Query,Request
# from fastapi.middleware.cors import CORSMiddleware
# from langchain.docstore.document import Document
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
# import pathlib
# import aiofiles
from src.services.rag_services.token_len import tiktoken_len
# from fastapi import File, UploadFile



async def rag_db(filename):
    db_filename = f"FAISS_DB/{filename}+faiss_index"
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name='gpt-3.5-turbo',
        temperature=0
    )
    embed = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            openai_api_key=api_key
        )
    if not os.path.exists(db_filename):
        
        loader = PyPDFLoader(f"uploads/{filename}")
        pages = loader.load_and_split()
        tokenizer = tiktoken.get_encoding('cl100k_base')
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20,
            length_function = tiktoken_len,
            separators=["\n\n", "\n", " ", ""]
        )
        data = text_splitter.split_documents(pages)
        db = FAISS.from_documents(data, embed)
        
        retriever = db.as_retriever()
        
        db.save_local(db_filename)
    else:
        print("Here in the else statement")
        db = FAISS.load_local(db_filename,embed, allow_dangerous_deserialization=True)
        retriever = db.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    return qa