from fastapi import FastAPI, APIRouter, HTTPException, Depends, status,Header, Query,Request
from fastapi.middleware.cors import CORSMiddleware
from src.routes import query_routes
from src.routes import user_routes
from src.routes import rag_routes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(query_routes.router, prefix = '/api/v1')
app.include_router(user_routes.router, prefix = '/api/v1')
app.include_router(rag_routes.router,prefix='/api/v1')