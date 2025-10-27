from frontend_model.ordersModel import *


def getorder(order_id):
    return getorderModel(order_id)


def placeOrderController(customer_id, products, shipping_address_id, payment_method):
    return placeOrderModel(customer_id, products, shipping_address_id, payment_method)

from frontend_model.ordersModel import getAllOrdersWithProducts  


def get_all_orders_with_products(customer_id):
    return getAllOrdersWithProducts(customer_id)

