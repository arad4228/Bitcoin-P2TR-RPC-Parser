import pandas as pd

baseUrl = 'https://www.blockchain.com/explorer/transactions/btc/'

def getDataFrame(txid, types, listFrom, listTo, listURL):
    df = pd.DataFrame(
        {
            "TxId": txid,
            "P2TR_Type": types,
            "From": listFrom,
            "To": listTo,
            "Url": listURL
        }
    )
    return df

def exportDataFrame(df):
    df.to_csv('Crawling_P2TR_TapTree.csv', encoding='utf-8')