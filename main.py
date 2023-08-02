# API principal 


# Documentacion de FastAPi: https://fastapi.tiangolo.com/es/

# Documentacion Swagger url local: http://127.0.0.1:8000/docs
# Documentacion ReDoc Url local: http://127.0.0.1:8000/redoc

# Instala FastAPI oficial: pip install "fastapi[all]"

# Importacion de librerias
from fastapi import FastAPI
from routers import products, users, basic_auth_users,jwt_auth_users,users_db
from fastapi.staticfiles import StaticFiles


# Intancia de FastAPI
app = FastAPI(prefix="/main",
                tags=["main"],
                responses={404:{"message":"No encontrado"}})

# routers
app.include_router(products.router) # router de products
app.include_router(users.router) # router de users
app.include_router(basic_auth_users.router) # router de basic auth
app.include_router(jwt_auth_users.router) # router de jwt auth
app.include_router(users_db.router) # router de users_db
app.mount("/static", 
          StaticFiles(directory="static"),
          name="static"
          )


# URl local: http://127.0.0.1:8000

@app.get("/")
async def root():
    return "Hola FastAPI!!"

# Url local: http://127.0.0.1:8000/

@app.get("/url")
async def root():
    return { "url_curso":"https://jayhcourse.net/python" }

# Inicia el server: uvicorn usersAPI:app --reload
# Detener el server: CTR + C