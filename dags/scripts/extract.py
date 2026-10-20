import requests
from pymongo import MongoClient

API_KEY = "G9N7CEPJ9UYPP4WJVR3QG3FUXTV5MQMT6A"

def extract_to_mongo():
    print("Сбор данных с Etherscan")
    url = (
        f"https://api.etherscan.io/v2/api?"
        f"chainid=1&"
        f"module=account&"
        f"action=tokentx&"
        f"contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&"
        f"page=1&"
        f"offset=100&"
        f"sort=desc&"
        f"apikey={API_KEY}"
    )

    response = requests.get(url, timeout=15).json()
    transactions = response.get('result', [])
    
    if not transactions:
        print("Данные не получены")
        return

    client = MongoClient('mongodb://mongo:27017/')
    db = client['web3_datalake']
    collection = db['usdt_raw_transfers']
    
    collection.delete_many({})
    
    collection.insert_many(transactions)
    print(f"Успешно сохранено {len(transactions)} записей в MongoDB.")