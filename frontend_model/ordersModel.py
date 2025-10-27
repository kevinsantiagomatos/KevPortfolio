from datetime import datetime
import random
import time
from frontend_model.connectDB import *

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

def getorderModel(order_id):
    db = Dbconnect()


    query = """
    SELECT 
    o.order_id, o.timestamp, o.total, o.status, o.tracking_number, o.transaction_number,
    c.first_name AS customer_first_name, c.last_name AS customer_last_name, c.email AS customer_email, 
    s.address_line, s.city, s.state, s.zipcode,
    oc.product_id, p.name, p.price, oc.quantity, (oc.quantity * p.price) AS total_price,
    p.image, p.brand
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN ship_address s ON o.address_id = s.address_id
    JOIN order_container oc ON o.order_id = oc.order_id
    JOIN products p ON oc.product_id = p.product_id
    WHERE o.order_id = %s;
    """



    result = db.select(query, (order_id,))
    if result:
        order_details = {
            "order_id": result[0]['order_id'],
            "order_date": result[0]['timestamp'],
            "total": result[0]['total'],
            "status": result[0]['status'],
            "transaction_number": result[0]['transaction_number'],
            "tracking_number": result[0]['tracking_number'],

            "customer": {
                "first_name": result[0]['customer_first_name'],
                "last_name": result[0]['customer_last_name'],
                "email": result[0]['customer_email']
            },
            "shipping_address": {
                "line_1": result[0]['address_line'],
                "city": result[0]['city'],
                "state": result[0]['state'],
                "zipcode": result[0]['zipcode']
            },
            "products": []
        }
        for row in result:
            order_details['products'].append({
                "product_id": row['product_id'],
                "": row['name'],
                "price": row['price'],
                "quantity": row['quantity'],
                "total_price": row['total_price'],
                "image": row['image'],
                "brand": row['brand']
            })
        return order_details

    return None




from datetime import datetime
from copy import deepcopy

def placeOrderModel(customer_id, products, shipping_address_id, payment_method):
    db = Dbconnect()

    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total = sum([float(product[2]) * int(product[1]) for product in products])
    status = "Pending"

    # Optional: Check if address exists
    address_check = db.select("SELECT address_id FROM ship_address WHERE address_id = %s", (shipping_address_id,))
    if not address_check:
        return {"status": "Error", "message": "Shipping address not found."}

    # Generate unique tracking_number and transaction_number (simple version)
    timestamp_part = int(time.time())  # current timestamp in seconds
    rand_part = random.randint(1000, 9999)
    tracking_number = random.randint(1000000000, 2147483647)  # max 10 digits
    transaction_number = random.randint(1000000000, 2147483647)

    
    # Insert into orders
    insert_order_query = """
        INSERT INTO orders (customer_id, timestamp, address_id, status,
                            tracking_number, transaction_number, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    order_params = (
        customer_id, order_date, shipping_address_id, status,
        tracking_number, transaction_number, total
    )
    db.execute(insert_order_query, order_params)

    result = db.select("SELECT LAST_INSERT_ID() AS last_id")
    if not result:
        return {"status": "Error", "message": "Failed to retrieve order_id."}

    order_id = result[0]['last_id']

    for product in products:
        db.execute(
        "UPDATE products SET stock = stock - %s WHERE product_id = %s",
        (int(product[1]), product[0])
)
        db.execute(
            "INSERT INTO order_container (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_id, product[0], int(product[1]), float(product[2]))
        )

    return {
        "order_id": order_id,
        "tracking_number": tracking_number,
        "transaction_number": transaction_number,
        "status": "Order placed successfully"
    }



def getAllOrdersWithProducts(customer_id):
    db = Dbconnect()


    query = """
    SELECT 
        o.order_id, o.timestamp, o.total, o.status,
        s.address_line, s.city, s.state, s.zipcode,
        p.name, p.price, oc.quantity, p.image, p.brand
    FROM orders o
    JOIN ship_address s ON o.address_id = s.address_id
    JOIN order_container oc ON o.order_id = oc.order_id
    JOIN products p ON oc.product_id = p.product_id
    WHERE o.customer_id = %s
    ORDER BY o.order_id DESC
    """

    result = db.select(query, (customer_id,))
    
    orders = {}
    for row in result:
        order_id = row['order_id']
        if order_id not in orders:
            orders[order_id] = {
                'order_id': order_id,
                'order_date': row['timestamp'],
                'total': row['total'],
                'status': row['status'],
                'shipping_address': {
                    'line_1': row['address_line'],
                    'city': row['city'],
                    'state': row['state'],
                    'zipcode': row['zipcode']
                },
                'products': []
            }
        orders[order_id]['products'].append({
            'product_name': row['name'],
            'price': row['price'],
            'quantity': row['quantity'],
            'image': row['image'],
            'brand': row['brand']
        })
    
    return list(orders.values())
