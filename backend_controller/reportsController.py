from backend_model.reportsModel import *

def getDatedReport(day):
    return get_sales_by_day(day)

def getStockReport():
    return get_inventory_report()

def getDatedReport():
    return getDatedReportModel() 


def getStockReport():
    return getStockReportModel()
