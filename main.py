from fastapi import FastAPI
from routers import free_chat, auth, users, preferences, user_preferences, user_listenings, user_routines, role_play, user_pronunciations, user_descriptions, images
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
app.include_router(free_chat.router)
app.include_router(preferences.router)
app.include_router(user_preferences.router)
app.include_router(user_listenings.router)
app.include_router(user_routines.router)
app.include_router(role_play.router)
app.include_router(user_pronunciations.router)
app.include_router(user_descriptions.router)
app.include_router(images.router)

# http://localhost:8000/docs - Swagger
# http://localhost:8000/redoc - Redoc
# http://localhost:8000/openapi.json - Openapi json