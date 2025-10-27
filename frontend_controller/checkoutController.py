from flask import url_for, redirect
from frontend_model.checkoutModel import *

def getUserCheckout():
    user = validateUserModel()

    for u in user:
        if u['phone_number'] == 0 or u['phone_number'] is None or u['phone_number'] == '':
            message = "Phone number is required."
            return redirect(url_for('checkout', message=message))

        if u['email'] == '' or u['email'] is None:
            message = "Email address is required."
            return redirect(url_for('checkout', message=message))

        return redirect("/invoice")