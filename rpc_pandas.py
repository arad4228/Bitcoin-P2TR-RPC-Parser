import pandas as pd

baseUrl = 'https://www.blockchain.com/explorer/transactions/btc/'

def getDataFrame(txid, types, listBRC20 ,listFrom, listTo, listURL):
    df = pd.DataFrame(
        {
            "TxId": txid,
            "P2TR_Type": types,
            "BRC20" : listBRC20,
            "From": listFrom,
            "To": listTo,
            "Url": listURL
        }
    )
    return df

def exportDataFrame(df):
    df.to_csv('Crawling_P2TR.csv', na_rep='NULL', encoding='utf-8')