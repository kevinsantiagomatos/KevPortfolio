import os
from functools import wraps
from flask import Flask, render_template, redirect, request, session, url_for
from backend_controller.loginController import register_admin, login_user
from backend_controller.ordersController import ordersController, getorder, getorderproducts
from backend_controller.productsController import *
from backend_controller.accountsController import *
from backend_controller.reportsController import *
from backend_controller.profileController import getAdmin
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='backend/')
app.secret_key = 'akeythatissecret'  # Asegúrate de que esto NO sea None
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('enterpage', message="Please log in first"))
        return f(*args, **kwargs)
    return decorated_function
# Página de login
@app.route("/", defaults={'message': None})
@app.route("/<message>")
def enterpage(message):
    return render_template('login (2).html', message=message)

# Página de registro
@app.route("/register", methods=["GET"])
def registerpage():
    return render_template("register.html", message=None)

# Procesamiento de registro
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
    register_admin(fname, lname, email, phonenumber, pass1)
    return redirect ('/login')

# Procesamiento de login
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    session['amount'] = 0

    admin = login_user(email, password)
    if admin:
        session['admin'] = admin['admin_id']
        return redirect("/profile")
    else:
        return redirect(url_for("enterpage", message="Login failed"))

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

@app.route("/profile")
@login_required
def profile():
    print("Admin in session:", session.get("admin"))
    admin = getAdmin(session['admin'])
    print(admin)
    return render_template("profile.html", user1=admin)

@app.route("/editinfo", methods=["POST"])
@login_required
def editinfo():
    db = Dbconnect()
    admin_id = session.get("admin")  # Ensure admin_id is in session
    if not admin_id:
        return redirect("/login")

    number = request.form.get("number")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    redirect_page = request.form.get("page", "/profile")

    if number:  # Contact number form submitted
        query = "UPDATE admins SET cellphone = %s WHERE admin_id = %s"
        db.execute(query, (number, admin_id))

    elif fname and lname and email:  # Profile info form submitted
        query = "UPDATE admins SET first_name = %s, last_name = %s, email = %s WHERE admin_id = %s"
        db.execute(query, (fname, lname, email, admin_id))

    return redirect(redirect_page)

@app.route("/password", methods=["POST"])
def password():
    return render_template("change-password.html")

@app.route("/products")
@login_required
def products():
    productsp = getProducts()
    return render_template("products.html", products=productsp)

@app.route("/product/<prod>")
@login_required
def product(prod):
    return redirect(url_for('single_product', prodID=prod))

@app.route("/single_product/<prodID>")
@login_required
def single_product(prodID):
    product = getsingleproduct(prodID)
    print("The product: ", product)
    return render_template("single_product.html", prod=product)

@app.route("/editproduct", methods=['POST'])
@login_required
def editproduct():
    data = {
        'product_id': request.form['product_id'],
        'name': request.form['name'],
        'brand': request.form['brand'],
        'color': request.form['color'],
        'price': request.form['price'],
        'cost': request.form['cost'],
        'stock': request.form['stock'],
        'description': request.form.get('desc', ''),
        'material': request.form['material'],
        'buoyancy': request.form['buoyancy'],
        'weight': request.form['weight'],
        'length': request.form['length'],
        'hooks': request.form['hooks'],
        'status': request.form['status'],
        'image': request.files['myfile'].filename if 'myfile' in request.files and request.files['myfile'].filename else None
    }

    if data['image']:
        request.files['myfile'].save('static/images/product-images/' + data['image'])

    editsingleproduct(data)
    return redirect('/products')


@app.route("/addproduct")
@login_required
def addproduct():
    productsp = getProducts()
    db = Dbconnect()
    categories = db.select("SELECT * FROM category")  
    print(categories)
    return render_template('add_product.html', prod=None, categories=categories)

@app.route("/createproduct", methods=['POST'])
@login_required
def createproduct():
    image_folder = os.path.join("static", "images", "product-images")
    os.makedirs(image_folder, exist_ok=True)

    image_filename = None
    if 'myfile' in request.files:
        file = request.files['myfile']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(image_folder, filename))
            image_filename = filename

            print("Submitted color:", request.form.get('color'))

    product_data = {
        "id": request.form['p_id'],
        "name": request.form['name'],
        "brand": request.form['brand'],
        "color": request.form.get('color',''),
        "price": request.form['price'],
        "cost": request.form['cost'],
        "stock": request.form['stock'],
        "description": request.form.get('description', ''),
        "material": request.form.get('material', ''),
        "buoyancy": request.form.get('buoyancy', ''),
        "weight": request.form.get('weight', ''),
        "length": request.form.get('length', ''),
        "hooks": request.form.get('hooks', ''),
        "category": request.form.get('category', ''),
        "image": image_filename,
        "status": request.form['status']
    }

    createproductc(product_data)
    return redirect('/products')

@app.route("/accounts/<userType>")
@login_required
def accounts(userType):
    acc = getaccounts(userType)
    return render_template("accounts.html", accounts=acc, userType=userType)

@app.route('/createaccount', methods=['GET', 'POST'])
@login_required
def createaccount():
    userType = request.args.get('userType')  # or pass as URL param

    if request.method == 'POST':
        data = request.form.to_dict()
        db = Dbconnect()

        if userType == 'admin':
            query = """
                INSERT INTO admins (first_name, last_name, email, password, cellphone, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                data['first_name'], data['last_name'], data['email'], data['password'],
                data.get('cellphone'), data['status']
            )
        elif userType == 'customer':
            query = """
                INSERT INTO customers (first_name, last_name, email, password, paypal_email, billing_zip, status, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data['first_name'], data['last_name'], data['email'], data['password'],
                data.get('paypal_email'), data.get('billing_zip'), data['status'], data.get('phone_number')
            )
        else:
            return "Invalid user type", 400

        db.execute(query, params)
        return redirect(url_for('accounts', userType=userType))

    return render_template("create_account.html", userType=userType)

@app.route('/editaccount', methods=['GET', 'POST'])
@login_required
def editaccount():
    acc_id = request.args.get('acc')
    userType = request.args.get('userType')
    db = Dbconnect()

    if request.method == 'POST':
        data = request.form.to_dict()

        if userType == 'admin':
            if data['password']:
                query = """
                    UPDATE admins
                    SET first_name=%s, last_name=%s, email=%s, password=%s, cellphone=%s, role=%s, status=%s
                    WHERE admin_id = %s
                """
                params = (
                    data['first_name'], data['last_name'], data['email'], data['password'],
                    data.get('cellphone'), data.get('role'), data['status'], acc_id
                )
            else:
                query = """
                    UPDATE admins
                    SET first_name=%s, last_name=%s, email=%s, cellphone=%s, role=%s, status=%s
                    WHERE admin_id = %s
                """
                params = (
                    data['first_name'], data['last_name'], data['email'],
                    data.get('cellphone'), data.get('role'), data['status'], acc_id
                )

        elif userType == 'customer':
            if data['password']:
                query = """
                    UPDATE customers
                    SET first_name=%s, last_name=%s, email=%s, password=%s, paypal_email=%s,
                        billing_zip=%s, status=%s, phone_number=%s
                    WHERE customer_id = %s
                """
                params = (
                    data['first_name'], data['last_name'], data['email'], data['password'],
                    data.get('paypal_email'), data.get('billing_zip'),
                    data['status'], data.get('phone_number'), acc_id
                )
            else:
                query = """
                    UPDATE customers
                    SET first_name=%s, last_name=%s, email=%s, paypal_email=%s,
                        billing_zip=%s, status=%s, phone_number=%s
                    WHERE customer_id = %s
                """
                params = (
                    data['first_name'], data['last_name'], data['email'],
                    data.get('paypal_email'), data.get('billing_zip'),
                    data['status'], data.get('phone_number'), acc_id
                )
        else:
            return "Invalid user type", 400

        db.execute(query, params)
        return redirect(url_for('accounts', userType=userType))

    # GET request → load account info
    account = getaccountmodel(userType, acc_id)
    return render_template("single_account.html", account=account, userType=userType, account_id=acc_id)

@app.route("/orders")
@login_required
def orders():
    sort = request.args.get('sort')  
    all_orders = ordersController(sort)
    return render_template("orders.html", orders=all_orders)

@app.route('/editorder/<int:order>')
@login_required
def editorder(order):
    orderProducts = getorderproducts(order)
    theorder = getorder(order)
    totalq = sum(prod['quantity'] for prod in orderProducts)

    print(theorder, orderProducts)
    return render_template('order.html', products=orderProducts, order=theorder, totalq=totalq)

@app.route('/updateorder/<int:order_id>', methods=['POST'])
@login_required
def updateorder(order_id):
    new_status = request.form.get('status')
    db = Dbconnect()
    query = "UPDATE orders SET status = %s WHERE order_id = %s"
    db.execute(query, (new_status, order_id))
    return redirect(url_for('editorder', order=order_id))

@app.route("/reports")
@login_required
def reports():
    db = Dbconnect()
    product_list = db.select("SELECT name FROM products")
    return render_template("reports.html", products=product_list)

@app.route("/report", methods=['POST'])
@login_required
def report():
    date_report = {}
    stock_report = {}
    total = 0.0

    day = request.form.get('report_day')
    week = request.form.get('report_week')
    month = request.form.get('report_month')
    product = request.form.get('products')  # can be None

    if day:
        if product:
            date_report = get_sales_by_day_and_product(day, product)
        else:
            date_report = get_sales_by_day(day)

    elif week:
        if product:
            date_report = get_sales_by_week_and_product(week, product)
        else:
            date_report = get_sales_by_week(week)

    elif month:
        if product:
            date_report = get_sales_by_month_and_product(month, product)
        else:
            date_report = get_sales_by_month(month)

    if 'stock_report' in request.form:
        stock_report = get_inventory_report()

    if date_report:
        total = round(sum(float(row['total_price']) for row in date_report.values()), 2)

    return render_template("report.html", date_report=date_report, stock_report=stock_report, total=total)

if __name__ == '__main__':
    app.run(debug=True)
