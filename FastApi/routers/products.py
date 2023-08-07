# API de los productos

from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404:{"message":"No encontrado"}})

products_lists = ["producto 1","producto 2","producto 3","producto 4","producto 5",]

@router.get("/")
async def products():
    return products_lists

@router.get("/{id}")
async def products(id: int):
    return products_lists[id] 