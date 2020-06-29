import requests
import json
import sys
from websocket import create_connection
import asyncio
import websockets
from config import LoginData,LoginCheckData

def LoginRequestMobileNewbyEmail(login_data):
    jsondata = {
        "head": {
            "appName"       : login_data.head["appName"],
            "appVer"        : login_data.head["appVer"],
            "key"           : login_data.head["key"],
            "osName"        : login_data.head["osName"],
            "requestCode"   : login_data.head["requestCode"],
            "userId"        : login_data.head["userId"],
            "password"      : login_data.head["password"]
        },
        "body": {
            "Email_id"      : login_data.body["Email_id"],
            "Password"      : login_data.body["Password"],
            "LocalIP"       : login_data.body["LocalIP"],
            "PublicIP"      : login_data.body["PublicIP"],
            "HDSerailNumber": login_data.body["HDSerailNumber"],
            "MACAddress"    : login_data.body["MACAddress"],
            "MachineID"     : login_data.body["MachineID"],
            "VersionNo"     : login_data.body["VersionNo"],
            "RequestNo"     : login_data.body["RequestNo"],
            "My2PIN"        : login_data.body["My2PIN"],
            "ConnectionType": login_data.body["ConnectionType"]
        }
    }
    z = requests.post('https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/LoginRequestMobileNewbyEmail', json=jsondata)


def LoginCheck(login_check_data):
    login_check_json_data = {
        "head": {
            "appName": login_check_data.head["appName"],
            "appVer": login_check_data.head["appVer"],
            "key": login_check_data.head["key"],
            "osName": login_check_data.head["osName"],
            "requestCode":login_check_data.head["requestCode"]
        },
        "body": {
            "userId" : login_check_data.body["userId"],
            "password": login_check_data.body["password"]
        }
    }
    y = requests.post('https://openfeed.5paisa.com/Feeds/api/UserActivity/LoginCheck', json=login_check_json_data)
    data={}
    paisa = y.cookies.get('.ASPXAUTH', domain=".5paisa.com")
    openfeed = y.cookies.get('.ASPXAUTH', domain="openfeed.5paisa.com")
    data['paisa']=paisa
    data['openfeed']=openfeed
    return y.cookies

async def test():
    # login user
    my_login_config = LoginData()
    LoginRequestMobileNewbyEmail(my_login_config)
    
    # login user and return the cookies
    my_login_check_config = LoginCheckData()
    my_cookies = LoginCheck(my_login_check_config)
    
    client_code = '56886446'
    registration_id = my_login_check_config.body["userId"]
    
    on_message = json.dumps({ 
            "Method":"MarketFeedV3",
            "Operation":"Subscribe",
            "ClientCode":"56886446",
            "MarketFeedData":[ 
                { 
                "Exch":"N",
                "ExchType":"C",
                "ScripCode":15083
                }
            ]
        })
    api_link = 'wss://websocket.5paisa.com/TTWebSocket/api/chat?Value1='+client_code+'|'+registration_id    
    on_error = 'some error ocurred'
    on_close = 'colsed'
    cookie_string = "; ".join([str(x)+"="+str(y) for x,y in my_cookies.items()])
    ws = websocket.WebSocketApp(api_link,
                      on_message = message,
                      on_error = on_error,
                      on_close = on_close,
                      cookie = cookie_string
                      )

asyncio.get_event_loop().run_until_complete(test())
