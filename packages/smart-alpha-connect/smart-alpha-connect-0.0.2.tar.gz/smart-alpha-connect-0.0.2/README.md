# Smart Alpha Connect API

## Installation

Run the following command to install :

```bash
pip install smart-alpha-connect
```

## Usage

```python
from SmartAlphaConnect import create_session
# Create a session using your clientID and smarttraderkey
session_data = create_session(clientID, smarttraderkey)
if session_data is not None:
    print(session_data)

# Get the access token from the response received through create_session in session_data
access_token = session_data.get("accesstoken")

# Import all the other functionalities
from SmartAlphaConnect import get_funds,get_orderbook,place_order,get_tradebook

# Get the funds data
funds_data = get_funds(clientID, access_token)
if funds_data is not None:
    print(funds_data)

# Get the orderbook data
orderbook_data = get_orderbook(clientID, access_token)
if orderbook_data is not None:
    print(orderbook_data)

# Place an order
placeorder_data = place_order(access_token, exchange, token,action, producttype, quantity, price, clientID, orderidentifier)
if placeorder_data is not None:
    print(placeorder_data)

# Get the tradebook data
tradebook_data = get_tradebook(clientID, access_token)
if tradebook_data is not None:
    print(tradebook_data)

```
