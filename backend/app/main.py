from fastapi import FastAPI

from app.api.auth_routes import router as auth_routes
from app.api.user_routes import router as user_routes
from app.api.helath_routes import router as health_routes
from app.api.chat_routes import router as chat_routes
from app.api.message_routes import router as message_routes
from app.api.document_routes import router as docment_routes
from app.api.search_routes import router as search_routes
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import global_exception_handler

from app.api.document_search import (
    router as document_search_router
)



app=FastAPI(
    name=settings.APP_NAME
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(
    Exception,
    global_exception_handler
)



app.include_router(health_routes)
app.include_router(auth_routes)
app.include_router(user_routes)
app.include_router(chat_routes)
app.include_router(message_routes)
app.include_router(docment_routes)
app.include_router(search_routes)

app.include_router(
    document_search_router
)
@app.get("/")
def root():
    return{
        "message":settings.APP_NAME
    }