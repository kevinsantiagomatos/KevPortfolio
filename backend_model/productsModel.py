from frontend_model.connectDB import Dbconnect



def getProductsModel():
    db = Dbconnect()
    query = "SELECT * FROM products"
    productList = db.select(query)
    print(productList)
    return productList


def getsingleproductmodel(prodID):
    db = Dbconnect()
    query = "SELECT * FROM products WHERE product_id = %s"
    result = db.select(query, (prodID,))
    print("--------------------")
    print(result)
    return result[0] if result else None

def editproductmodel(data):
    db = Dbconnect()
    query = """
        UPDATE products
        SET name = %s,
            brand = %s,
            color = %s,
            price = %s,
            cost = %s,
            stock = %s,
            description = %s,
            material = %s,
            buoyancy = %s,
            weight = %s,
            length = %s,
            hooks = %s,
            status = %s
            {image_clause}
        WHERE product_id = %s
    """

    if data['image']:
        image_clause = ", image = %s"
        query = query.format(image_clause=image_clause)
        params = (
            data['name'], data['brand'], data['color'], data['price'], data['cost'], data['stock'],
            data['description'], data['material'], data['buoyancy'], data['weight'],
            data['length'], data['hooks'], data['status'], data['image'], data['product_id']
        )
    else:
        image_clause = ""
        query = query.format(image_clause=image_clause)
        params = (
            data['name'], data['brand'], data['color'], data['price'], data['cost'], data['stock'],
            data['description'], data['material'], data['buoyancy'], data['weight'],
            data['length'], data['hooks'], data['status'], data['product_id']
        )

    db.execute(query, params)

def createproductmodel(data):
    db = Dbconnect()
    query = """
        INSERT INTO products (
            product_id, name, brand, color, price, cost, stock, description,
            material, buoyancy, weight, length, hooks, category_id,
            image, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
       data['id'], data['name'], data['brand'], data['color'], data['price'], data['cost'], data['stock'],
        data['description'], data['material'], data['buoyancy'], data['weight'],
        data['length'], data['hooks'], data['category'], data['image'], data['status']
    )
    db.execute(query, params) 