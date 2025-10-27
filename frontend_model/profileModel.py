import pymysql
from flask import session
from frontend_model.connectDB import *
from passlib.handlers.sha2_crypt import sha256_crypt


def getUserModel(customerid):
    if not customerid:
        return None  

    db = Dbconnect()
    query = "SELECT * from customers WHERE customer_id = %s"
    
   
    userFound = db.select(query, (customerid,))  

    if userFound:
        user = userFound[0]  
        user_data = {
            "id": user['customer_id'],
            "name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
            "password": user['password'],
            "phone_number": user['phone_number'],
            "status": user['status'],
            "billing_zip": user['billing_zip'],
            "paypal_email": user['paypal_email']
        }
        return user_data  

    return None  


def editnumbermodel(number):
    db = Dbconnect()
    query = "UPDATE customers SET phone_number = %s WHERE customer_id = %s"
    try:
        db.execute(query, (number, session['customer']))
        return 0

    except pymysql.Error as error:
        print(error)
        return 1


def addaddressmodel(aline1, state, zipcode, city):
    db = Dbconnect()

    # Insert into ship_address table
    query1 = (
        "INSERT INTO ship_address (customer_id, address_line, city, state, zipcode) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    db.execute(query1, (session['customer'], aline1, city, state, zipcode))

    # Update the billing_zip for the customer (NOT insert)
    query2 = "UPDATE customers SET billing_zip = %s WHERE customer_id = %s"
    db.execute(query2, (zipcode, session['customer']))

    return 0

def editaddressmodel(aline1, state, zipcode, city, a_id):
    db = Dbconnect()

    try:
        # Update ship_address
        query1 = (
            "UPDATE ship_address SET address_line = %s, city = %s, "
            "state = %s, zipcode = %s WHERE customer_id = %s AND address_id = %s"
        )
        db.execute(query1, (aline1, city, state, zipcode, session['customer'], a_id))

        # Update billing_zip in customers table
        query2 = "UPDATE customers SET billing_zip = %s WHERE customer_id = %s"
        db.execute(query2, (zipcode, session['customer']))

        return 0

    except pymysql.Error as error:
        print(error)
        return 1


def getpaymentmodel(customer):
    db = Dbconnect()
    query = "SELECT * FROM payment_method WHERE customer_id = %s"

    try:
        methods = db.select(query, (customer,))
        return methods

    except pymysql.Error as error:
        print(error)
        return []


def editpaymentmodel(name, c_type, number, exp_date):
    print("STUDENTS MUST ADD")
    return 0


def editprofilemodel(fname, lname, email):
    db = Dbconnect()
    query = "UPDATE customers SET first_name = %s, last_name = %s, email = %s WHERE customer_id = %s"
    try:
        db.execute(query,(fname, lname, email, session['customer']))
        return 0

    except pymysql.Error as error:
        print(error)
        return 1


def getAddressModel(customer):
    db = Dbconnect()
    sql = "SELECT * FROM ship_address WHERE customer_id = %s"
    result = db.select(sql, (customer))

    if result:
        address = result[0]  
        address_data = {
            "address_line": address['address_line'],
            "city": address['city'],
            "state": address['state'],
            "zipcode": address['zipcode'],
            "address_id": address['address_id']
        }
        return address_data


def changepassmodel(user_id, old_password, new_password):

    db = Dbconnect()
    query = "SELECT * FROM customers WHERE customer_id = %s"

    
    userFound = db.select(query, (user_id,))

    if not userFound:
        return 0  

    
    for user in userFound:
       
        if not sha256_crypt.verify(old_password, user['password']):
            return 2  

    
    hashed_new_password = sha256_crypt.encrypt(new_password)

    try:
        
        query2 = "UPDATE customers SET password = %s WHERE customer_id = %s"
        db.execute(query2, (hashed_new_password, user_id))
        return 1  

    except pymysql.Error as error:
        print(error)
        return 0  
    
def getUserByEmailModel(email):
    db = Dbconnect()
    query = "SELECT * FROM customers WHERE email = %s"
    result = db.select(query, (email,)) 

    
    if result:
        user = result[0]  
        c_id = user.get("customer_id")  
        return c_id  
    else:
        return None  
    


def resetpasswordModel(user_id, new_password):
    
    hashed_new_password = sha256_crypt.encrypt(new_password)

    
    db = Dbconnect()
    
   
    query = "UPDATE customers SET password = %s WHERE customer_id = %s"
    
    try:
       
        db.execute(query, (hashed_new_password, user_id))
        return 1  
    except pymysql.Error as error:
        print(error)
        return 0  