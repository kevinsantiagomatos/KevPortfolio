from flask import session
from frontend_model.connectDB import *
import pymysql
from passlib.hash import sha256_crypt

def loginmodel(email, password):

    # Receive email and password to check in the "database"

    user = []
    db = Dbconnect()
    sql = "SELECT email, customer_id, password, status FROM customers WHERE email = %s"
    # Save user info in list
    userFound = db.select(sql, (email,))

    print(userFound)

    for res in userFound:
        user.append({"id": res['customer_id'], "email": res['email'], "password": res['password'], "status": res['status']})


    # Save user info in list

    # sha256_crypt.encrypt("password") = this is what is used to encrypt a password
    # sha256_crypt.verify(password_unhashed, password_hashed) = this is what is used to compare an unhashed and hashed password

    for u in user:
        if email == u['email'] and sha256_crypt.verify(password, u['password']) is True:
            session['customer'] = u['id']
            # Create the session['customer'] saving the customer ID if user is found
            return "true"
        else:
            # If it didn't find user
            return "false"


def registermodel(fname, lname, email, phonenumber, hashed_pass):
    try:
        db = Dbconnect()  # Create a new database connection
        sql = """INSERT INTO customers (first_name, last_name, email, password, status, phone_number, billing_zip) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (fname, lname, email, hashed_pass, "Active", phonenumber, email)

        # Execute the SQL query with the given parameters
        db.execute(sql, params)  
        db.commit()  # Commit the transaction to save changes in the database

        return True  # Return True if the insertion is successful
    except Exception as e:
        print(f"Error inserting user: {e}")  # Log the error
        return False  # Return False if there is an issue