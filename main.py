from fastapi import FastAPI
from routers import chat, auth, users, listening, sentences, preferences, user_preferences
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = FastAPI()

origins = [os.environ.get("FRONTEND_DOMAIN")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(listening.router)
app.include_router(sentences.router)
app.include_router(preferences.router)
app.include_router(user_preferences.router)

# http://localhost:8000/docs - Swagger
# http://localhost:8000/redoc - Redoc
# http://localhost:8000/openapi.json - Openapi json