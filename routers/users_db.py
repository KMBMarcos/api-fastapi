# API de los usuarios(con CRUD)

from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client # Conexion con la base de datos


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


users_list = []


@router.get("/")
async def users():
    return users_list

# Hacer un get de un usuario en la url por path. Llamando por la url http://127.0.0.1:8000/user/(id que desea)
@router.get("/{id}")
async def user(id: int):
    return search_user(id)
    
# Hacer un get de un usuario en por query. Llamando por la url como http://127.0.0.1:8000/userquery/?id=(id deseado)
@router.get("/")
async def user(id: int):
    return search_user(id)

# Operación para crear usuarios 
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    #if type(search_user(user.id)) == User: 
    #       raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    # Convertimos el parametro 'user' en un diccionario
    user_dict = dict(user)
    
    # Borramos el campo 'id' porque la db ya asigna este campo
    del user_dict["id"]
    
    # Creamos el usuario en la db
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    # Buscamos el usuario en la base de datos como un diccionario desde schemas
    new_user = user_schema(db_client.local.users.find_one({"_id":id}))
    
    # Retornamos el usuario como un diccionario
    return User(**new_user)

# Operación para actualizar usuarios
@router.put("/")
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
           users_list[index] = user
           found=True
           
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

# Operacion para borrar usuarios
@router.delete("/{id}")
async def user(id: int):
    
    found= False
    
    for index, saved_user in enumerate(users_list): # El for es para encontrar al usuario
        if saved_user.id == id:
            del users_list[index] # Operacion de borrar
            found=True
            
    if not found:
        return {"error":" No se ha eliminado el usuario"}


# Funcion para la busqueda de usuarios por id
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}