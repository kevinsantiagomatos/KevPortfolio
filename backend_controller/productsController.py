from backend_model.productsModel import *


def getProducts():
    products = getProductsModel()
    return products


def getsingleproduct(prodID):
    return getsingleproductmodel(prodID)

def editsingleproduct(data):
    return editproductmodel(data)

def createproductc(product_data):
    return createproductmodel(product_data)