from frontend_model.profileModel import *
from flask import session

def getUser(customerid):
    return getUserModel(customerid)

def getAddress(customer):
    return getAddressModel(customer)

def editnumbercontroller(number):
    return editnumbermodel(number)

def addaddresscontroller(aline1, state, zipcode, city):
    return addaddressmodel(aline1, state, zipcode, city)


def editaddresscontroller(aline1, state, zipcode, city, a_id):
    return editaddressmodel(aline1, state, zipcode, city, a_id)

def getpaymentcontroller():
    return getpaymentmodel(session['customer'])


def editpaymentcontroller(name, c_type, number, exp_date):
    return editpaymentmodel(name, c_type, number, exp_date)


def editprofilecontroller(fname, lname, email):
    return editprofilemodel(fname, lname, email)


def changePass(userid, old_password, new_password):
    return changepassmodel(userid, old_password, new_password)

def getUserByEmail(email):
    return getUserByEmailModel(email)

def resetpassword(user_id, new_password):
    return resetpasswordModel(user_id, new_password)
