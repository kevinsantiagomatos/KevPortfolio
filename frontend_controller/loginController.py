from frontend_model.loginModel import *
from flask import redirect, render_template
from passlib.hash import sha256_crypt


def logincontroller(email, password):
    result = loginmodel(email=email, password=password)

    if 'request' in session:
        request = session['request']
        session.pop('request', None)
        return redirect(request)

    if result is "true":
        return redirect("/shop")
    else:
        return redirect("/login?error=incorrect")


def registercontroller(fname, lname, email, phonenumber, pass1, pass2):
    if not fname or not lname or not email or not phonenumber or not pass1 or not pass2:
        return '/register?message=All fields are required'

    if pass1 != pass2:
        return '/register?message=Passwords do not match'

    hashed_pass = sha256_crypt.hash(pass1) 

    res = registermodel(fname, lname, email, phonenumber, hashed_pass)

    if res:
        return '/shop'  
    else:
        return '/register?message=Registration failed'
