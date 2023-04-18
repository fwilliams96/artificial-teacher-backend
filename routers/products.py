from fastapi import APIRouter

router = APIRouter(prefix='/products', tags=['products'], responses={404: {"message": "Not found"}})

# uvicorn main:app --reload

products_list = ["Producto1", "Producto2"]

@router.get('/')
async def products():
    return products_list

@router.get('/{id}')
async def product(id: int):
    return products_list[0]
