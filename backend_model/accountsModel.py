from frontend_model.connectDB import Dbconnect



def getaccountsmodel(userType):
    db = Dbconnect()

    if userType == 'admin':
        query = "SELECT * FROM admins"
        rows = db.select(query)
        return {row["admin_id"]: {
            "c_first_name": row["first_name"],
            "c_last_name": row["last_name"],
            "c_email": row["email"],
            "c_password": row["password"],
            "c_phone_number": row["cellphone"],
            "c_status": row["status"]
        } for row in rows}

    elif userType == 'customer':
        query = "SELECT * FROM customers"
        rows = db.select(query)
        return {row["customer_id"]: {
            "c_first_name": row["first_name"],
            "c_last_name": row["last_name"],
            "c_email": row["email"],
            "c_password": row["password"],
            "c_phone_number": row["phone_number"],
            "c_status": row["status"],
            "c_paypal_email": row["paypal_email"],
            "c_billing_zip": row["billing_zip"]
        } for row in rows}

    return {}


# Get the specific account requested
# In this case, we're requesting it via the key
def getaccountmodel(userType, acc_id):
    db = Dbconnect()

    if userType == 'customer':
        query = "SELECT * FROM customers WHERE customer_id = %s"
    elif userType == 'admin':
        query = "SELECT * FROM admins WHERE admin_id = %s"
    else:
        raise ValueError("Invalid user type")

    result = db.select(query, (acc_id,))
    return result[0] if result else None

