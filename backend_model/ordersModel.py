from frontend_model.connectDB import Dbconnect

def ordersModel(sort=None):
    db = Dbconnect()
    query = "SELECT * FROM orders"

    if sort == 'date':
        query += " ORDER BY timestamp DESC"
    elif sort == 'total':
        query += " ORDER BY total DESC"
    elif sort == 'dateo':
        query += " ORDER BY total ASC"
    elif sort == 'totall':
        query += " ORDER BY total ASC"

    result = db.select(query)
    return result

def getordermodel(ID):
    db = Dbconnect()
    query = "SELECT * FROM orders WHERE order_id = %s"
    result = db.select(query, (ID,))
    return result[0] if result else None

def getorderproductsmodel(order_id):
    db = Dbconnect()
    query = """
        SELECT p.name, p.image, p.brand, oc.product_id, oc.quantity, oc.price
        FROM order_container oc
        JOIN products p ON oc.product_id = p.product_id
        WHERE oc.order_id = %s
    """
    result = db.select(query, (order_id,))

    for prod in result:
        prod['total_price'] = round(prod['price'] * prod['quantity'], 2)

    print(result,"<-------------------------")
    return result


