from flask import session


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



def getCartModel():
    if 'cart' in session:
        return session['cart']
    else:
        session['cart'] = []
        return session['cart']


def addCartModel(dictitems):
    check = "false"
    if 'cart' in session and session['cart'] != []:
        for key1, item1 in session['cart'].items():
            
            for key2, item2 in dictitems.items():
                if key1 == key2:
                    check = "true"
                    if int(item1['quantity']) + int(item2['quantity']) <= int(item1['stock']):
                        item1['quantity'] = int(item1['quantity']) + int(item2['quantity'])
                        item1['total_price'] += item2['total_price']
                    else:
                        print("EXCEEDING PRODUCT STOCK")
                        item1['quantity'] = int(item1['stock'])
                        item1['total_price'] = float(item1['quantity']) * float(item1['price'])
        if check == "false":
            session['cart'] = MagerDicts(session['cart'], dictitems)
    else:
        session['cart'] = dictitems

    
    session['amount'] = 0
    session['total'] = 0

    for key, item in session['cart'].items():
        session['amount'] += int(item['quantity'])
        session['total'] += float(item['total_price'])
    return


def deleteCartItemModel(p_id):
    if "cart" in session and p_id in session["cart"]:
        del session["cart"][p_id]
    return



