from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# CORS middleware settings
def add_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_credentials=True,
        allow_methods=['GET', 'POST'],
        allow_headers=['Content-Type'],
    )
