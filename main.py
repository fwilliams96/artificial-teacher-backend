from fastapi import FastAPI
from routers import chat, chat_text, chat_voice
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
#app.include_router(products.router)
# app.include_router(users.router)
# app.include_router(users_db.router)
# app.include_router(jwt_auth_users.router)
#app.include_router(chatgpt_chat.router)
app.include_router(chat.router)
app.include_router(chat_text.router)
app.include_router(chat_voice.router)

#app.mount('/static', StaticFiles(directory='static'), name='static')

# uvicorn main:app --reload

# @app.get('/')
# async def root():
#     return { "message": "Hola FastAPI" }

# http://localhost:8000/docs - Swagger
# http://localhost:8000/redoc - Redoc
# http://localhost:8000/openapi.json - Openapi json