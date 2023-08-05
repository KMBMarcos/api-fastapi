# API de los usuarios(con CRUD)

from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.schemas.user import user_schema,users_schema
from db.client import db_client # Conexion con la base de datos
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


# Operacion para obtener todos los usuarios
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

# Hacer un get de un usuario en la url por path. Llamando por la url http://127.0.0.1:8000/user/(id que desea)
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
# Hacer un get de un usuario en por query.  
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Operación para crear usuarios 
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User: 
           raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
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
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

# Operacion para borrar usuarios por id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found= db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error" : " No se ha eliminado el usuario"}

# Funcion para buscar usuarios en la DB por email
def search_user(field: str, key):
    
    try:
        user = db_client.local.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado el usuario"}
