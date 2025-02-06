from fastapi import FastAPI
from app.routes import auth, rag, upload
from app.db import init_db
from decouple import config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG API",
    description="API pour des fonctionnalités de RAG enrichies",
    version="1.0.0"
)

origins = [
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
# app.include_router(upload.router, prefix="/upload", tags=["upload"])

@app.get("/")
async def root():
    return {
        "message": "welcome to Abraham's api version 1.1 !",
        }