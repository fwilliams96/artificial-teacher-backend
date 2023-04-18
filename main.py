from fastapi import FastAPI
from routers import products, users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

# uvicorn main:app --reload

@app.get('/')
async def root():
    return { "message": "Hola FastAPI" }

# http://localhost:8000/docs - Swagger
# http://localhost:8000/redoc - Redoc
# http://localhost:8000/openapi.json - Openapi json