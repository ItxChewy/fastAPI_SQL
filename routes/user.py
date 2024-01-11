from fastapi import APIRouter, Response, HTTPException
from sqlalchemy import text
from config.db import conn
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get('/users')
def get_users():
    try:
        result = conn.execute(text("SELECT * FROM fastAPI")).fetchall()
        users_list = [{"id": row.id, "username": row.username, "name": row.name, "weight": row.weight, "date": row.date} for row in result]
        return users_list
    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")




@user.post('/users')
def create_user(user: User):
    try:
        new_user = {"username": user.username, "name": user.name, "weight": user.weight, "date": user.date}
        new_user["password"] = f.encrypt(user.password.encode("utf-8"))
        result = conn.execute(users.insert().values(new_user)) 
        conn.commit()

        # Obtener solo los datos necesarios
        user_data = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
        return {"id": user_data.id, "username": user_data.username, "name": user_data.name, "weight": user_data.weight, "date": user_data.date}
    except Exception as e:
        print(f"Error al crear usuario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@user.get('/users/{id}')
def get_user(id: str):
    try:
        # Obtener las claves de la tabla directamente
        user_data = conn.execute(users.select().where(users.c.id == id)).first()
        print(f"user_data type: {type(user_data)}")  # Nuevo print
        if user_data:
            table_columns = users.c.keys()
            # Convertir el objeto Row a un diccionario de forma más robusta
            user_dict = dict(zip(table_columns, user_data))
            print(f"user_dict: {user_dict}")  # Nuevo print
            return user_dict
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except HTTPException as e:
        # Manejar específicamente la excepción HTTPException con código de estado 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        print(f"Error al obtener usuario por ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")



@user.delete('/users/{id}')
def delete_user(id: str):
    try:
        conn.execute(users.delete().where(users.c.id == id))
        print(f"Usuario con ID {id} eliminado exitosamente")  # Nuevo print
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        print(f"Error al eliminar usuario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@user.put('/users/{id}')
def update_user(id: str, user: User):
    try:
        # Obtener el usuario existente
        existing_user = conn.execute(users.select().where(users.c.id == id)).first()

        if existing_user:
            # Actualizar solo los campos proporcionados en el cuerpo de la solicitud
            update_data = {}

            if user.username:
                update_data["username"] = user.username
            if user.name:
                update_data["name"] = user.name
            if user.password:
                update_data["password"] = f.encrypt(user.password.encode("utf-8"))
            if user.weight:
                update_data["weight"] = user.weight
            if user.date:
                update_data["date"] = user.date

            # Realizar la actualización en la base de datos
            conn.execute(users.update().values(**update_data).where(users.c.id == id))

            # Obtener los datos actualizados del usuario después de la actualización
            updated_user = conn.execute(users.select().where(users.c.id == id)).first()

            # Convertir el objeto Row a un diccionario para evitar errores de serialización
           # user_dict = dict(updated_user)

            # Devolver los datos actualizados del usuario en la respuesta
            return {"message " : "Usuario actualizado"}
        else:
            # Usuario no encontrado, devolver respuesta 404
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except HTTPException as e:
        # Manejar específicamente la excepción HTTPException con código de estado 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")





