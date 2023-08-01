# API de los usuarios(con CRUD)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404:{"message":"No encontrado"}})

# Inicia el server: uvicorn usersAPI:app --reload

# Entidad users
class User(BaseModel):
    id: int
    name : str
    surname :str
    url:str
    age:int

 
users_list = [User(id=1,name="Marcos",surname="Mateo",url="https://kamby.com",age=24),
              User(id=2,name="Robin",surname="Dariurg",url="https://Dariurg.com",age=28), 
              User(id=3, name="Joyse",surname="Joyaise",url="https://Joyaise.com",age=32)]

# METODO GET --- INICIO ---
# Hacer un get de la lista de usuarios por un json en crudo
@router.get("/usersjson")
async def usersjson():
    return [{ "name":"Marcos", "surname":"Mateo","url":"https://kamby.com", "age":24 },
            { "name":"Robin", "surname":"Dariurg","url":"https://Dariurg.com", "age":28 },
            { "name":"Joyse", "surname":"Joyaise","url":"https://Joyaise.com","age":32 }]

# Hacer un get de la lista de usuarios por entidad, que la identidad es users_list
@router.get("/users")
async def users():
    return users_list

# Hacer un get de un usuario en la url por path. Llamando por la url http://127.0.0.1:8000/user/(id que desea)
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
# Hacer un get de un usuario en por query. Llamando por la url como http://127.0.0.1:8000/userquery/?id=(id deseado)
@router.get("/user/")
async def user(id: int):
    return search_user(id)

# METODO GET --- FINAL ---

# METODO POST --- INICIO ---
@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User: 
        raise HTTPException(status_code=404, detail="El usuario ya existe")
        
    
    users_list.append(user)
    return user

# METODO POST --- FINAL ---

# METODO PUT --- INICIO ---
@router.put("/user/")
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
# METODO PUT --- FINAL ---

# METODO DELETE --- INICIO ---
@router.delete("/user/{id}")
async def user(id: int):
    
    found= False
    
    for index, saved_user in enumerate(users_list): # El for es para encontrar al usuario
        if saved_user.id == id:
            del users_list[index] # Operacion de borrar
            found=True
            
    if not found:
        return {"error":" No se ha eliminado el usuario"}


# METODO DELETE --- FINAL ---

# Funcion para la busqueda de usuarios por id
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}