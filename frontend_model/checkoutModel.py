import pymysql
from flask import session
from frontend_model.connectDB import *


def validateUserModel():
    user = []
    db = Dbconnect()
    
    query = "SELECT * from customers WHERE c_id = %s"

    userFound = db.select(query, (session['customer'],))

    for users in userFound:
        user.append({"id": users['c_id'], "name": users['c_first_name'], "last_name": users['c_last_name'],
                     "email": users['c_email'],
                     "password": users['c_password'], "phone_number": users['c_phone_number'],
                     "status": users['c_status']})

    return user
