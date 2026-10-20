from pymongo import MongoClient
import clickhouse_connect
from datetime import datetime

def load_to_clickhouse():
    print("Перенос данных из MongoDB в ClickHouse")

    mongo_client = MongoClient('mongodb://mongo:27017/')
    mongo_collection = mongo_client['web3_datalake']['usdt_raw_transfers']
    
    raw_data = list(mongo_collection.find())
    
    clickhouse_data = []
    for tx in raw_data:
        clickhouse_data.append([
            int(tx['blockNumber']),
            datetime.fromtimestamp(int(tx['timeStamp'])),
            tx['hash'],
            tx['from'],
            tx['to'],
            float(tx['value']) / 10**6,
            int(tx['gasUsed'])
        ])

    ch_client = clickhouse_connect.get_client(host='clickhouse', port=8123, username='default', password='')
    
    ch_client.command("TRUNCATE TABLE web3_dwh.stg_usdt_transfers")
    
    ch_client.insert(
        'web3_dwh.stg_usdt_transfers', 
        clickhouse_data, 
        column_names=['blockNumber', 'timeStamp', 'hash', 'from_address', 'to_address', 'value', 'gasUsed']
    )
    print("Данные успешно загружены в ClickHouse")