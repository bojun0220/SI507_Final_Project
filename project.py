import requests
import os
import json


consumer_key = 'nd4NS71uCJTZGuPOCHN1rM8Zp'
consumer_secret = 'E1HNKIUcFppyxpRDnKuRunjuyHxIqd5kE2Ks05z8F57YRzwOpM'
access_token = '1651554944-ufxm9RHaQymvAjFL9uPfYI2BYcM59Q9yasD92Gt'
access_token_secret = 'bDCsj0TW8niCvwqxqazQW3covotTytLbVbB9dwPRaXAZu'

def get_trend(loc):
    '''
    get trend of a location
    loc: location id
    return: json

    '''
    loc_id = get_loc_id(loc)
    url = "https://api.twitter.com/1.1/trends/place.json?"
    payload={}
    headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANqNkAEAAAAAGE4dok9Xdo2JMETUzd83dT%2FbbQQ%3DojdPCxtNep21wPeMRxks8gOsxlsoDCpSDY2FtlGjiVpn5ziHPe',
    'Cookie': 'guest_id=v1%3A167038332417705283; guest_id_ads=v1%3A167038332417705283; guest_id_marketing=v1%3A167038332417705283; personalization_id="v1_z0N8FmK/dY4thiNY6w314g=="; lang=zh-tw'
    }
    params = {
        'id': loc_id
    }
    response = requests.get(url, headers=headers, data=payload, params=params).json()
    for i in range(len(response[0]['trends'])):
        print(f'{i}: {response[0]["trends"][i]["name"]}')
    return response

def get_loc_id(loc):
    '''
    get location id
    loc: location name
    return: location id
    '''
    id_list = json.load(open('id_list.json'))
    for i in range(len(id_list)):
        if loc.lower() in id_list[i]['name'].lower():
            return id_list[i]['woeid']
    print("Location not found")
def main():
    get_trend('Detroit')


if __name__ == '__main__':
    main()
    


