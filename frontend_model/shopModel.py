import pymysql
from frontend_model.connectDB import *



def getProductsModel(min_price=None, max_price=None, depth_rating=None, color=None, category=None, length=None, weight=None, brand=None, buoyancy=None, hooks=None, sort_by=None, searchedname=None, materials=None):
    productList = []
    db = Dbconnect()

   
    query = "SELECT * FROM products WHERE status = 'active'"
    filters = []

    
    if min_price:
        query += " AND price >= %s"
        filters.append(min_price)
    if max_price:
        query += " AND price <= %s"
        filters.append(max_price)

    
    if depth_rating:
        query += " AND brand IN (%s)" % ', '.join(['%s'] * len(depth_rating))
        filters.extend(depth_rating)

   
    if color:
        query += " AND color IN (%s)" % ', '.join(['%s'] * len(color))
        filters.extend(color)

   
    if category:
        query += " AND category_id IN (%s)" % ', '.join(['%s'] * len(category))
        filters.extend(category)

   
    if length:
        query += " AND length IN (%s)" % ', '.join(['%s'] * len(length))
        filters.extend(length)

    
    if weight:
        query += " AND weight IN (%s)" % ', '.join(['%s'] * len(weight))
        filters.extend(weight)

    if buoyancy:
        query += " AND buoyancy IN (%s)" % ', '.join(['%s'] * len(buoyancy))
        filters.extend(buoyancy)

    
    if brand:
        query += " AND brand IN (%s)" % ', '.join(['%s'] * len(brand))
        filters.extend(brand)
    
    if hooks:
        query += " AND hooks IN (%s)" % ', '.join(['%s'] * len(hooks))
        filters.extend(hooks)

    if materials:
        query += " AND material IN (%s)" % ', '.join(['%s'] * len(materials))
        filters.extend(materials)

    if searchedname:
        query += " AND name LIKE %s"
        filters.append(f"%{searchedname}%")
    
    if sort_by:
        if sort_by == "price_asc":
            query += " ORDER BY price ASC"
        elif sort_by == "price_desc":
            query += " ORDER BY price DESC"
        elif sort_by == "product_name_asc":
            query += " ORDER BY name ASC"
        elif sort_by == "product_name_desc":
            query += " ORDER BY name DESC"

    
    if filters:
        results = db.select(query, tuple(filters))
    else:
        
        results = db.select(query)

    
    for res in results:
        productList.append({
            "id": res['product_id'],
            "name": res['name'],
            "brand": res['brand'],
            "desc": res['description'],
            "color": res['color'],
            "img": res['image'],
            "stock": res['stock'],
            "cost": res['cost'],
            "price": res['price'],
            "status": res['status'],
            "material": res['material'],
            "length": res['length'],
            "weight": res['weight'],
            "buoyancy": res['buoyancy'],
            "hooks": res['hooks']
        })

    return productList

def getBrandsModel():
    
    db = Dbconnect()
    query = ("SELECT DISTINCT brand "
             "FROM products "
             "WHERE status = 'active'"
             "ORDER BY brand;")
    brands = db.select(query)
    return brands

def getColorsModel():
    db = Dbconnect()
    query = ("SELECT DISTINCT color "
             "FROM products "
             "WHERE status = 'active'"
             "ORDER BY color;")
    colors = db.select(query)
    return colors





def getMaterialModel():
    db = Dbconnect()
    query = ("SELECT DISTINCT material "
             "FROM products "
             "WHERE status = 'active';")
    material = db.select(query)
    return material

def getLengthModel():
    db = Dbconnect()
    query = ("SELECT DISTINCT length "
             "FROM products "
             "WHERE status = 'active';")
    length = db.select(query)
    return length

def getWeightsModel():
    db = Dbconnect()
    query = ("SELECT DISTINCT weight "
             "FROM products "
             "WHERE status = 'active';")
    weight = db.select(query)
    return weight

def getCategoriesModel():
    db = Dbconnect()
    query = "SELECT category_id, category_name FROM category ORDER BY category_name;"
    categories = db.select(query)
    print(categories)
    return categories

def getBuoyancyModel():
    db = Dbconnect()
    query = ("SELECT DISTINCT buoyancy "
             "FROM products "
             "WHERE status = 'active';")
    buoyancy = db.select(query)
    print(buoyancy)
    return buoyancy

def getHooksModel():
    db = Dbconnect()
    query = ("SELECT DISTINCT hooks "
             "FROM products "
             "WHERE status = 'active';")
    hooks = db.select(query)
    print(hooks)
    print(hooks)
    print(hooks)
    print(hooks)
    print(hooks)
    print(hooks)
    return hooks