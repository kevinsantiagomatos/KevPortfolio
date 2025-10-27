import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend_model.connectDB import Dbconnect
from passlib.hash import sha256_crypt

# Registrar administrador
def register_admin(fname, lname, email, phone, password):
    db = Dbconnect()  
    hashed_pw = sha256_crypt.hash(password)
    try:
        sql = """
            INSERT INTO admins (first_name, last_name, email, cellphone, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute(sql, (fname, lname, email, phone, hashed_pw))
        return True
    except Exception as e:
        print("DB Error:", e)
        return False

# Login de administrador
def login_user(email, password):
    db = Dbconnect()
    try:
        sql = "SELECT * FROM admins WHERE email = %s"
        result = db.select(sql, (email,))
        print("Resultado de consulta:", result)

        if result:
            is_valid = sha256_crypt.verify(password, result[0]['password'])
            print("¿Password correcto?:", is_valid)
            if is_valid:
                return result[0] 
    except Exception as e:
        print("Error en login:", e)
    return None

# Obtener información del admin
def getUser(email):
    db = Dbconnect()
    try:
        sql = "SELECT * FROM admins WHERE email = %s"
        result = db.select(sql, (email,))
        return result[0] if result else None
    except Exception as e:
        print("Error obteniendo admin:", e)
        return None
