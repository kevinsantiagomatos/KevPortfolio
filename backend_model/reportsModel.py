# backend_model/reportsModel.py
from datetime import datetime, timedelta
from calendar import monthrange
from frontend_model.connectDB import Dbconnect

# ================================
# Reporte de ventas por día
# ================================
def get_sales_by_day(day):
    db = Dbconnect()
    sql = """
        SELECT o.order_id, o.tracking_number, p.name, p.brand, DATE(o.timestamp) AS date,
               oc.price, oc.quantity,
               ROUND(oc.price * oc.quantity, 2) AS total_price
        FROM orders o
        JOIN order_container oc ON o.order_id = oc.order_id
        JOIN products p ON oc.product_id = p.product_id
        WHERE DATE(o.timestamp) = %s
    """
    result = db.select(sql, (day,))
    return {i+1: row for i, row in enumerate(result)}

# ================================
# Reporte de inventario actual
# ================================
def get_inventory_report():
    db = Dbconnect()
    sql = "SELECT product_id, name, brand, stock AS quantity FROM products"
    result = db.select(sql)
    return {row['product_id']: row for row in result}

# ================================
# Wrapper para el controlador
# ================================
def get_sales_by_day_and_product(day, product):
    db = Dbconnect()
    sql = """
        SELECT o.order_id, o.tracking_number, p.name, p.brand, DATE(o.timestamp) AS date,
               oc.price, oc.quantity,
               ROUND(oc.price * oc.quantity, 2) AS total_price
        FROM orders o
        JOIN order_container oc ON o.order_id = oc.order_id
        JOIN products p ON oc.product_id = p.product_id
        WHERE DATE(o.timestamp) = %s AND p.name LIKE %s
    """
    result = db.select(sql, (day, f"%{product}%"))
    return {i+1: row for i, row in enumerate(result)}

def getDatedReportModel(day="2025-01-01"):
    return get_sales_by_day(day)

def getStockReportModel():
    return get_inventory_report()

# ================================
# Reporte de ventas por semana
# ================================
def get_sales_by_week(week_str):
    db = Dbconnect()

    try:
        # Parse week string like '2025-W19'
        year, week = map(int, week_str.split('-W'))

        # Get Monday of the ISO week (1 = Monday, 7 = Sunday)
        start_date = datetime.fromisocalendar(year, week, 1).date()
        end_date = start_date + timedelta(days=6)
    except Exception as e:
        print("Week parse error:", e)
        return {}

    print("Start date:", start_date)
    print("End date:", end_date)

    sql = """
        SELECT o.order_id, o.tracking_number, p.name, p.brand, DATE(o.timestamp) AS date,
               oc.price, oc.quantity,
               ROUND(oc.price * oc.quantity, 2) AS total_price
        FROM orders o
        JOIN order_container oc ON o.order_id = oc.order_id
        JOIN products p ON oc.product_id = p.product_id
        WHERE DATE(o.timestamp) BETWEEN %s AND %s
    """
    result = db.select(sql, (start_date, end_date))
    return {i+1: row for i, row in enumerate(result)}

# ================================
# Reporte de ventas por mes
# ================================
def get_sales_by_month(month_str):
    db = Dbconnect()
    
    try:
        # month_str is in format '2025-05'
        year, month = map(int, month_str.split('-'))
        start_date = datetime(year, month, 1).date()
        last_day = monthrange(year, month)[1]  # e.g., 31 for May
        end_date = datetime(year, month, last_day).date()
    except Exception as e:
        print("Month parse error:", e)
        return {}

    print("Start date:", start_date)
    print("End date:", end_date)

    sql = """
        SELECT o.order_id, o.tracking_number, p.name, p.brand, DATE(o.timestamp) AS date,
               oc.price, oc.quantity,
               ROUND(oc.price * oc.quantity, 2) AS total_price
        FROM orders o
        JOIN order_container oc ON o.order_id = oc.order_id
        JOIN products p ON oc.product_id = p.product_id
        WHERE DATE(o.timestamp) BETWEEN %s AND %s
    """
    result = db.select(sql, (start_date, end_date))
    return {i+1: row for i, row in enumerate(result)}

def get_sales_by_week_and_product(week_str, product):
    db = Dbconnect()
    try:
        year, week = map(int, week_str.split('-W'))
        start_date = datetime.fromisocalendar(year, week, 1).date()
        end_date = start_date + timedelta(days=6)
    except Exception as e:
        print("Week parse error:", e)
        return {}

    sql = """
        SELECT o.order_id, o.tracking_number, p.name, p.brand, DATE(o.timestamp) AS date,
               oc.price, oc.quantity,
               ROUND(oc.price * oc.quantity, 2) AS total_price
        FROM orders o
        JOIN order_container oc ON o.order_id = oc.order_id
        JOIN products p ON oc.product_id = p.product_id
        WHERE DATE(o.timestamp) BETWEEN %s AND %s
          AND p.name LIKE %s
    """
    result = db.select(sql, (start_date, end_date, f"%{product}%"))
    return {i+1: row for i, row in enumerate(result)}


def get_sales_by_month_and_product(month_str, product):
    db = Dbconnect()
    try:
        year, month = map(int, month_str.split('-'))
        start_date = datetime(year, month, 1).date()
        last_day = monthrange(year, month)[1]
        end_date = datetime(year, month, last_day).date()
    except Exception as e:
        print("Month parse error:", e)
        return {}

    sql = """
        SELECT o.order_id, o.tracking_number, p.name, p.brand, DATE(o.timestamp) AS date,
               oc.price, oc.quantity,
               ROUND(oc.price * oc.quantity, 2) AS total_price
        FROM orders o
        JOIN order_container oc ON o.order_id = oc.order_id
        JOIN products p ON oc.product_id = p.product_id
        WHERE DATE(o.timestamp) BETWEEN %s AND %s
          AND p.name LIKE %s
    """
    result = db.select(sql, (start_date, end_date, f"%{product}%"))
    return {i+1: row for i, row in enumerate(result)}