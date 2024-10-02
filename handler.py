from plugin.feature.mega_leilao.gateway.gateway_injector_impl import GatewayInjectorImpl

presenter = GatewayInjectorImpl.inject()

def house_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))
    
    body = {}
    statusCode = 200        
    presenter.get_house(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }

    return res

def apartments_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))
    
    body = {}
    statusCode = 200        
    presenter.get_apartment(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }

    return res

def sheds_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))
    body = {}
    statusCode = 200
    presenter.get_shed(page=scrap_page)
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    return res

def lands_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_land(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res



def garage_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_garage_deposit(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res

def commercial_real_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_commercial_real_estate(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res

def parking_spaces_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_parking_spaces(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res

def plots_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_plots(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res

def rural_properties_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_rural_properties(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res

def rural_real_estate_per_page(event, context):
    scrap_page = event["page"]
    print("page: "+ str(scrap_page))

    body = {}
    statusCode = 200
    presenter.get_rural_real_estate(page=scrap_page)

    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return res