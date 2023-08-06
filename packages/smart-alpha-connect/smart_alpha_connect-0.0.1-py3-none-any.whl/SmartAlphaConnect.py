import requests

# function to create a new session for a user
def create_session(clientID , smarttraderkey):
    url = "http://mysmartalpha.com/create_session"

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    payload = {
        "clientid": clientID,
        "smarttraderkey": smarttraderkey,
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        session_data = response.json()
        return session_data
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None


# function to access the funds for a user using their session token
def get_funds(clientID,access_token):
    url = "http://mysmartalpha.com/get_funds"
    query_params = {
        'vendorname': 'nirmalbang',
        'clientid': clientID
    }
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(url, params=query_params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code: ", response.status_code)
        return None


# function to get the orderbook for a user using their session token
def get_orderbook(clientID,access_token):
    url = "http://mysmartalpha.com/get_orderbook"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    query_params = {
        "vendorname": "nirmalbang",
        "clientid": clientID
    }

    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        orderbook_data = response.json()
        return orderbook_data
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None


# function to place an order for a user using their session token
def place_order(access_token):
    url = "http://mysmartalpha.com/placeorder"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    payload = {
        "exch": "NSE_EQ",
        "token": "22",
        "action": "BUY",
        "producttype": "DELIVERY",
        "qty": "1",
        "price": "250",
        "vendorname": "nirmalbang",
        "clientid": "SBH001",
        "orderidentifer": "test1"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        order_data = response.json()
        return order_data
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None
    

# function to get the tradebook for a user using their clientID and session token
def get_tradebook(clientID, access_token):
    url = "http://mysmartalpha.com/get_tradebook"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    query_params = {
        "vendorname": "nirmalbang",
        "clientid": clientID
    }

    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        tradebook_data = response.json()
        return tradebook_data
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None
