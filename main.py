from datetime import datetime

from flask import Flask, render_template, redirect, request, session, flash, url_for, jsonify
from frontend_controller.cartController import getCart, addCartController, deleteCartItem
from frontend_controller.checkoutController import getUserCheckout
from frontend_controller.invoiceController import *
from frontend_controller.loginController import logincontroller, registercontroller
from frontend_controller.ordersController import getorder, placeOrderController
from frontend_controller.ordersController import get_all_orders_with_products
from frontend_controller.profileController import getUser, changePass, getAddress, editaddresscontroller, addaddresscontroller, editnumbercontroller, editpaymentcontroller, editprofilecontroller, getUserByEmail, resetpassword
from frontend_controller.shopController import *

app = Flask(__name__, template_folder='frontend/')
app.secret_key = 'akeythatissecret'

@app.route("/autocomplete")
def autocomplete():
    q = request.args.get("q", "")
    print("Autocomplete Query:", q)  # <-- DEBUG
    db = Dbconnect()
    results = db.select("SELECT name FROM products WHERE name LIKE %s LIMIT 5", (q + '%',))
    print("DB Results:", results)  # <-- DEBUG
    return jsonify([row["name"] for row in results])
# Redirects us here if no url is given
@app.route("/", defaults={'message': None})
# Or if any url other than the ones set in this Flask application is provided, making it a <message>
@app.route("/<message>")

def enterpage(message):

    
    products = getProducts()
    brands = getBrands()
    colors = getColors()
    categories = getCategories()
    lengths = getLength()
    weights = getWeights()
    materials = getMaterial()
    buoyancies = getBuoyancy()
    hooks=getHooks()
    
 

    
    amount = session.get('amount', 0)
    total = session.get('total', 0.00)


    
    return render_template("shop-4column.html", materials=materials, products=products, amount=amount, total=total,
                           brands=brands, colors=colors, categories=categories, lengths=lengths, weights=weights, buoyancies=buoyancies, hooks=hooks)

@app.route("/clear")
def clear():

    session.clear()
    return redirect("/")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
       
        email = request.form.get('email')
        passcode = request.form.get('password')
        session['amount'] = 0
       
       
        return logincontroller(email=email, password=passcode)
    
    
    return render_template('login (2).html')  

@app.route("/register/", defaults={'message': None})
@app.route('/register/<message>')
def register(message):
    
    return render_template('register.html', message=message)


@app.route("/registerinfo", methods=['POST'])
def registerinfo():
    
    
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')
    phonenumber = request.form.get('phonenumber')

    if not fname or not lname or not email or not pass1 or not pass2 or not phonenumber:
        return redirect('/register?message=All fields are required')

    
    if pass1 != pass2:
        return redirect('/register?message=Passwords do not match')

    
    print(pass1)
    registercontroller(fname, lname, email, phonenumber, pass1, pass2)
    return redirect ('/login')

@app.route("/shop")
def shop():
    
    products = getProducts()
    brands = getBrands()
    colors = getColors()
    categories = getCategories()
    lengths = getLength()
    weights = getWeights()
    materials = getMaterial()
    buoyancies = getBuoyancy()
    hooks=getHooks()

    # Debugging outputs
    print("Brands:", brands)
    print("Colors:", colors)
    print("Categories:", categories)
    print("Lengths:", lengths)
    print("Weights:", weights)

   
    amount = session.get('amount', 0)
    total = session.get('total', 0.00)


    
    return render_template("shop-4column.html", materials=materials, products=products, amount=amount, total=total,
                           brands=brands, colors=colors, categories=categories, lengths=lengths, weights=weights, buoyancies=buoyancies, hooks=hooks)
@app.route("/profile")
def profile():
    
    user_id = session.get("customer")
    print(user_id)
    
    
    user = getUser(user_id)
    address = getAddress(user_id)
    if not user:
        
        return redirect(url_for('login'))  
    
   
    amount = session.get('amount', 0)
    total = session.get('total', 0.00)

   
    phone_number = user.get('phone_number')
    exp_date = user.get('c_exp_date', 'N/A')
    
    num = '{:03d}-{:03d}-{:04d}'.format(
            int(str(phone_number)[:3]),
            int(str(phone_number)[3:6]),
            int(str(phone_number)[6:])
        )
    
    if address is not None:
        user.update(address)
    else:
    
        print("Address not provided, skipping update.")
   
        address = {}  
        user.update(address)
    return render_template("profile.html", user1=user, total=total, num=num, amount=amount)

@app.route('/editinfo', methods=['POST'])
def editinfo():
    user_id = session.get("customer")  
    if not user_id:
        return redirect(url_for('login'))  


    if 'fname' in request.form and 'lname' in request.form and 'email' in request.form:
       
        editprofilecontroller(request.form['fname'], request.form['lname'], request.form['email'])

    elif 'number' in request.form:
       
        editnumbercontroller(request.form['number'])

    elif 'aline1' in request.form and 'city' in request.form and 'state' in request.form and 'zipcode' in request.form:
       
       
        address_data = {
            'aline1': request.form['aline1'],
            'city': request.form['city'],
            'state': request.form['state'],
            'zipcode': request.form['zipcode']
        }
        
        existing_address = getAddress(user_id)
        if existing_address:
                 
            editaddresscontroller(address_data['aline1'], address_data['state'], address_data['zipcode'], address_data['city'], existing_address['address_id'])
        else:
           
            addaddresscontroller(address_data['aline1'], address_data['state'], address_data['zipcode'], address_data['city'])

    elif 'card_name' in request.form and 'card_num' in request.form and 'card_type' in request.form and 'date' in request.form:
       
        editpaymentcontroller(request.form['card_name'], request.form['card_type'],
                              request.form['card_num'], request.form['date'])

    elif 'old_password' in request.form and 'new_password' in request.form:
       
        changePass(user_id, request.form['old_password'], request.form['new_password'])

   
    return redirect(request.form['page'])


@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "POST":
        old_password = request.form["pass_o"]
        new_password = request.form["pass_n"]
        new_password_confirm = request.form["pass_n1"]

        
        user_id = session.get("customer")

        
        if new_password != new_password_confirm:
            flash("New passwords do not match. Please try again.")
            return redirect(url_for("password"))

       
        result = changePass(user_id, old_password, new_password)
        
        if result == 1:
            flash("Password changed successfully!")
            return redirect(url_for("profile"))  
        elif result == 2:
            flash("Old password is wrong.")
            return redirect(url_for("password"))
        else:
            flash("Incorrect old password. Please try again.")
            return redirect(url_for("password"))  

    return render_template("change-password.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_pass"]
        new_password_confirm = request.form["new_pass_confirm"]

        if new_password != new_password_confirm:
            flash("New passwords do not match. Please try again.")
            return redirect(url_for("reset_password"))

        user_id = getUserByEmail(email)  

        if user_id:
            
            result = resetpassword(user_id, new_password)  

            if result == 1:
                flash("Password reset successfully!")
                return redirect(url_for("login"))
            else:
                flash("There was an error resetting the password. Please try again.")
                return redirect(url_for("reset_password"))
        else:
            flash("No account found with that email address.")
            return redirect(url_for("reset_password"))

    return render_template("reset-password.html")

@app.route("/orders")
def orders():
    amount = session.get('amount', 0)
    total = session.get('total', 0.00)
    customer_id = session.get("customer")
    sort_by = request.args.get("sort")

    orders = get_all_orders_with_products(customer_id)

    if sort_by == "status":
        orders.sort(key=lambda x: x["status"])
    elif sort_by == "date":
        orders.sort(key=lambda x: x["order_date"])
    elif sort_by == "total":
        orders.sort(key=lambda x: x["total"])
    # Default is unsorted or as retrieved

    return render_template("orderlist.html", orders=orders, total=total, amount=amount)

from flask import request, redirect, url_for, session

@app.route('/addcart', methods=['POST'])
def addcart():
    try:
        if 'cart' not in session:
            session['cart'] = {}

        
        p_id = request.form.get('p_id')
        name = request.form.get('name')
        image = request.form.get('image')
        price = request.form.get('price')
        stock = request.form.get('stock')
        quantity = request.form.get('quantity')

        
        if not price or not quantity:
            return "Error: Missing price or quantity", 400

        price = float(price)
        quantity = int(quantity)
        total = round(price * quantity, 2)

        
        addCartController(p_id, name, image, price, stock, quantity, total)

        return redirect(url_for('shop'))  
    
    except Exception as e:
        return f"Error: {e}", 400

@app.route("/delete/<p_id>")
def delete(p_id):
   
   
    deleteCartItem(p_id)

    
    session["amount"] = sum(int(item["quantity"]) for item in session["cart"].values())
    session["total"] = sum(float(item["total_price"]) for item in session["cart"].values())

    return redirect(request.referrer)  


@app.route("/editcart", methods=["POST"])
def editcart():
    p_id = request.form.get("p_id")  
    quantity = request.form.get("quantity")

    if not p_id or not quantity.isdigit():  
        return redirect(request.referrer)

    quantity = int(quantity)

    
    if "cart" in session and p_id in session["cart"]:
        item = session["cart"][p_id]
        if quantity > 0 and quantity <= int(item["stock"]):  
            item["quantity"] = quantity
            item["total_price"] = round(float(item["price"]) * quantity, 2)
        elif quantity == 0:  
            deleteCartItem(p_id)  

   
   
    if "cart" in session and session["cart"]:
        session["amount"] = sum(int(item["quantity"]) for item in session["cart"].values())
        session["total"] = round(sum(float(item["total_price"]) for item in session["cart"].values()), 2)  
    else:
        session["amount"] = 0
        session["total"] = 0.0

        session.modified = True  
    return redirect(request.referrer)

@app.route("/checkout")
def checkout():
   
   
    if 'customer' in session:
        
        user_id = session.get("customer")
        user = getUser(user_id)
        total = 0

        address = getAddress(user_id)
        phone_number = user.get('phone_number')
        exp_date = user.get('c_exp_date', 'N/A')
    
        num = '{:03d}-{:03d}-{:04d}'.format(
            int(str(phone_number)[:3]),
            int(str(phone_number)[3:6]),
            int(str(phone_number)[6:])
        )

       
        for key, item in session['cart'].items():
            total += item['total_price']

        return render_template("checkout.html", user1=user, num=num, total=total, address=address)

    else:
       
        session['checkout'] = True
       
        return redirect(url_for('login'))  

@app.route('/placeOrder', methods=['POST'])
def placeOrder():
    print(session['cart'])

   
    customer_id = session.get("customer")
    print("Customer ID:", customer_id)

    shipping_address_id = 1 
    print("Shipping Address ID:", shipping_address_id)

    product_ids = request.form.getlist('product_ids[]')
    quantities = request.form.getlist('quantities[]')
    prices = request.form.getlist('prices[]')

    print("Product IDs:", product_ids)
    print("Quantities:", quantities)
    print("Prices:", prices)

    
    products = []
    for i in range(len(product_ids)):
        products.append((
            product_ids[i],  
            quantities[i],   
            prices[i]       
        ))
    print("Products:", products)

   
    result = placeOrderController(
        customer_id, products, shipping_address_id, payment_method="PayPal"
    )

    print("Order Result:", result)

    if result["status"] == "Order placed successfully":
       
        return redirect(url_for('invoice', order_id=result["order_id"]))
    else:
        return f"Error placing order: {result['message']}", 500
    
@app.route('/paypal_redirect', methods=['POST'])
def paypal_redirect():
    customer_id = request.form.get('customer_id')
    shipping_address_id = request.form.get('shipping_address_id')
    product_ids = request.form.getlist('product_ids[]')
    quantities = request.form.getlist('quantities[]')
    prices = request.form.getlist('prices[]')
    payment_method = "Paypal"

    products = [(product_ids[i], quantities[i], prices[i]) for i in range(len(product_ids))]
    result = placeOrderController(customer_id, products, shipping_address_id, payment_method)

    if result['status'] == "Order placed successfully":
        session.pop('cart', None)
        session["amount"] = 0
        session["total"] = 0.0
        session.modified = True
        return redirect(url_for('invoice', order_id=result['order_id']))
    else:
        return f"Error: {result['message']}", 500



    
@app.route("/invoice/int:<order_id>")
def invoice(order_id):
    
    order = getorder(order_id)
    if order:
        return render_template("invoice.html", order=order, products=order['products'])
    else:
        return "Order not found", 404
   


@app.route("/filter", methods=["GET"])
def filter():
    
    query = request.args.get("query", "")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    depth_rating = request.args.getlist("depth_rating")
    brand = request.args.getlist("brand")
    color = request.args.getlist("color")
    category = request.args.getlist("category")
    length = request.args.getlist("length")
    weight = request.args.getlist("weight")
    buoyancy = request.args.getlist("buoyancy")
    hook = request.args.getlist("hooks")
    sort_by = request.args.get("sort_by", "price_asc")  
    material = request.args.getlist("material")
    
    
    products = getProductsModel(min_price, max_price, depth_rating, color, category, length, weight, brand, buoyancy, hook, sort_by, query, material)
    
    
    brands = getBrands()
    colors = getColors()
    categories = getCategories()  
    lengths = getLength()  
    weights = getWeights()  
    materials = getMaterial()
    buoyancies = getBuoyancy()
    hooks = getHooks()
    print(hooks)
    

    
    amount = session.get('amount', 0)
    total = session.get('total', 0.00)
    
    print(color)  # Debugging line
    print("Materials in route:", materials)
    return render_template("shop-4column.html", products=products, amount=amount, total=total, brands=brands,
                           colors=colors, categories=categories, lengths=lengths, weights=weights, materials=materials, buoyancies=buoyancies, hooks=hooks, searchedname=query)

@app.route("/products")
def products():
  
    return render_template("products.html") 

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

@app.route("/search")
def search():
    query = request.args.get("query", "")
    db = Dbconnect()
    results = db.select("SELECT * FROM products WHERE name LIKE %s", ('%' + query + '%',))
    return render_template("shop-4column.html", products=results, query=query)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/