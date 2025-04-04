from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from threading import Lock

load_dotenv()

def add_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:5173', 'http://localhost:3000'],
        allow_credentials=True,
        allow_methods=['GET', 'POST'],
        allow_headers=['Content-Type'],
    )

request_lock = Lock()

def processing_limiter():
    if not request_lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail='⏳ Request already in progress. Please wait.')
