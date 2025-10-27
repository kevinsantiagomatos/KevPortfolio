from frontend_model.connectDB import Dbconnect

def getAdminModel(adminid):
    if not adminid:
        return None  

    db = Dbconnect()
    query = "SELECT * from admins WHERE admin_id = %s"
    
   
    userFound = db.select(query, (adminid,))  

    if userFound:
        user = userFound[0]  
        print(user)
        user_data = {
            "id": user['admin_id'],
            "name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
            "password": user['password'],
            "phone_number": user['cellphone'],
            "status": user['status']
        }
        return user_data  

    return None  
