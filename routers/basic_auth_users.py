# API para la autenticacion basica del usuario

from fastapi import APIRouter,HTTPException,Depends,status # "Depends" indica la dependencia de alguna entidad 
from pydantic import BaseModel 

# "OAuth2PasswordBearerm" es para hacer la autenticacion del usuario
# "OAuth2PasswordRequestForm" es para enviar el usuario y la contraseña del usuario para autenticar
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

# Instancia de la autenticacion
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Entidad usuario
class User(BaseModel):
    username : str
    full_name : str
    email: str
    disabled: bool

# Entidad usuario de la DB
class UserDB(User):
    password: str


users_db = {
    "kambyjh" : {
        "username" : "kambyjh",
        "full_name" : "Marcos Mateo",
        "email": "kamby@mckamby.com",
        "disabled": False,
        "password" : "123456"
    },
    "kambyj0" : {
        "username" : "kambyj0",
        "full_name" : "Marcos Mateo",
        "email": "kamby0j@mckamby.com",
        "disabled": True,
        "password" : "123465"
    }
}

# Operacion para buscar UserDB
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


# Oeracion para busacr User
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Operacion para verificar si el token dado al usuario es correcto cuando se solicito dicho token
async def current_user(token: str = Depends(oauth2)): # Tiene dependen de las credenciales del login
    user = search_user(token) # Buscamos el token que es el "username" en la DB
    if not user: # Si el usuario no esta logeado lanza un error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo")
    return user

# Operacion de autenticacion
@router.post("/basic/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) # verificamos que el usuario de la base de datos exista
    if not user_db: # Si el usuario no esta en la base de datos lanza un error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto")

    # Ya tenemos el usuario de la base de datos!!
    user = search_user_db(form.username)
    if not form.password == user.password: # Si la contraseña no esta en la base de datos lanza un error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}

# Operacion para que devuelva el usuario una ves autenticado
@router.get("/basic/users/me")
async def me(user: User = Depends(current_user)): # Tiene dependencia de autenticacion del token dado
    return user