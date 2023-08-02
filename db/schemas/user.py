
# Operacion para convertir el usuario en un diccionario
def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}
