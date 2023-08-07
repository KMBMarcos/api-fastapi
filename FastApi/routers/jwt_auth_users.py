# API para la autenticacion JWT del usuario

from fastapi import APIRouter,HTTPException,Depends,status # "Depends" indica la dependencia de alguna entidad 
from pydantic import BaseModel 

# "OAuth2PasswordBearerm" es para hacer la autenticacion del usuario
# "OAuth2PasswordRequestForm" es para enviar el usuario y la contraseña del usuario para autenticar
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importamos "JWT" para la autenticacion
from jose import jwt, JWTError

# Libreria para el proceso de encriptado
from passlib.context import CryptContext

from datetime import datetime,timedelta

# Algoritmo para la encriptación
ALGORITHM = "HS256"

# Duracion del token para autenticar
ACCESS_TOKEN_DURATION = 1


SECRET = "qB&T!%AE$EHfDj$wxEzgYafoVPDt%WuS@o^jX#uUWxB^eGQCmghTC$TGVKHGVhg@fMS,FHG@%*@^faUY%&g&"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Proceso de encriptacion
crypt = CryptContext(schemes=["bcrypt"]) # "bcrypt" es el que define el algoritmo de encriptación


# Entidad usuario
class User(BaseModel):
    username : str
    full_name : str
    email: str
    disabled: bool
    
# Entidad usuario de la base de datos
class UserDB(User):
    password: str

    
users_db = {
    "kambyjh" : {
        "username" : "kambyjh",
        "full_name" : "Marcos Mateo",
        "email": "kamby@mckamby.com",
        "disabled": False,
        "password" : "$2a$12$eDamhXpNMhZHPLcT/9s2WuHshJsmeV3KKXDBb8InZW0tbvh6jWWmG"
    },
    "kambyj0" : {
        "username" : "kambyj0",
        "full_name" : "Marcos Mateo",
        "email": "kamby0j@mckamby.com",
        "disabled": True,
        "password" : "$2a$12$YEwA//vWLWgEHlFtGVVrSOn2AYwPdMm04Jo4r6OnW3nuQImu4XDJe"
    }
}


# Operacion para buscar UserDB
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Operacion para buscar User
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Para buscar el usuario autenticado
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        # Desencriptamos el token
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:  # Evitamos que el explote si el username esta vacio
            raise exception
            
    except JWTError:
        raise exception
    
    # retornamos el usuario
    return search_user(username)
# Para saber si el usuario esta disable 
async def current_user(user: User = Depends(auth_user)): 
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo")
    return user

# Operacion de autenticacion
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )
    
    # Ya tenemos el usuario de la DB
    user = search_user_db(form.username)

    # Verificamos si la contraseña que le pasamos es la que esta en la DB encriptada
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta")
    
    # Aqui le damos un tiempo de caducidad al token
    access_token = {
        "sub": user.username, 
        "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)         
    }
    
    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

# Operación para obtener mis datos 
@router.get("/users/me") 
async def me(user: User = Depends(current_user)): 
    return user
