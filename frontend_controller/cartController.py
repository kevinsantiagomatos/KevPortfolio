from frontend_model.cartModel import *


def getCart():
    #get cart items and session variables: total and quantity
    if 'amount' not in session:
        session['amount'] = 0
    if 'total' not in session:
        session['total'] = 0
    return getCartModel()


def addCartController(p_id, name, image, price, stock, quantity, total):
    dictitems = {p_id: {'name': name, 'image': image, 'price': price, 'quantity': quantity,
                        'total_price': total, 'stock': stock}}
    return addCartModel(dictitems)


def deleteCartItem(p_id):
    return deleteCartItemModel(p_id)



