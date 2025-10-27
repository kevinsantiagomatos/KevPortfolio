from backend_model.ordersModel import *


def ordersController(sort=None):
    return ordersModel(sort)


def getorder(ID):
    return getordermodel(ID)


def getorderproducts(ID):
    return getorderproductsmodel(ID)
