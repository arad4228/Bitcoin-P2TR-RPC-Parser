import pandas as pd

baseUrl = 'https://www.blockchain.com/explorer/transactions/btc/'

def getDataFrame(listBlockNumber, txid, types, listBRC20 ,listFrom, listTo, listCountofScripts, listURL):
    df = pd.DataFrame(
        {
            "BlockNumber": listBlockNumber,
            "TxId": txid,
            "P2TR_Type": types,
            "BRC20" : listBRC20,
            "From": listFrom,
            "To": listTo,
            "CountOfScirpts": listCountofScripts,
            "Url": listURL
        }
    )
    return df

def exportDataFrame(df, lastBlock):
    df.to_csv(f'Crawling_P2TR_{lastBlock}.csv', na_rep='NULL', encoding='utf-8')