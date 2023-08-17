from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from rpc_config import *
from rpc_pandas import *

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# initialBlockNumber = 400000
# initialBlockNumber = 789024
initialBlockNumber = 790734

listTxid = []
listTypes = []
listBRC20 = []
listFrom = []
listTo = []
listURL = []

try:
    while True:
        print(f"Current Block: {initialBlockNumber}")
        block_hash = rpc_connection.getblockhash(initialBlockNumber)
        block_info = rpc_connection.getblock(block_hash)
        transactions = block_info['tx']

        for transaction in transactions:
            print(f'Reading Transction is {transaction}')
            url = baseUrl+transaction
            Json_transaction = rpc_connection.getrawtransaction(transaction, 2)
            # if transaction is coinbase, skip transaction next
            if 'coinbase' in Json_transaction['vin'][0]:
                print("this transaction is coinbase transaction")
                continue
                
            # check P2TR, TapTree, BRC-20
            # initial value is false
            is_P2TR = False
            is_TapTree = False
            is_BRC_20 = False

            BRC20 = ""
            Types = ""
            From = ""
            To = ""

            # if transaction not coinbase, collect all vin transaction.
            for vin in Json_transaction['vin']:
                # check witness_v1_taproot
                utxo = vin['txid']
                index = vin['vout']
                utxo_transaction = rpc_connection.getrawtransaction(utxo, 2)
                From += (utxo_transaction['vout'][index]['scriptPubKey']['address']+', ')

                # if uxto witness is 'witness_v1_taproot
                if utxo_transaction['vout'][index]['scriptPubKey']['type'] != "witness_v1_taproot":
                    continue

                is_P2TR = True

                # if not taproot spent transaction
                if len(vin['txinwitness']) == 3:
                    is_TapTree = True
                    # check BRC-20
                    script = vin['txinwitness'][1]
                    decoded_script = rpc_connection.decodescript(script)
                    if 'OP_IF' in decoded_script['asm'] and '6582895' in decoded_script['asm']:
                        is_BRC_20 = True
            
            # if transaction is not p2tr type
            if not is_P2TR:
                continue
            
            # else
            for vout in Json_transaction['vout']:
                if "address" in vout['scriptPubKey']:
                    To += ((vout['scriptPubKey']['address'])+', ')
                else:
                    To += ('NULL, ')
            
            if is_TapTree:
                Types = 'TapTree'
            else:
                Types = 'TapRoot'
            
            if is_BRC_20:
                BRC20 = "BRC-20"
            else:
                BRC20 = "Not BRC-20"

            From = From[:len(From)-2]
            To = To[:len(To)-2]

            listTxid.append(transaction)
            listTypes.append(Types)
            listBRC20.append(BRC20)
            listFrom.append(From)
            listTo.append(To)
            listURL.append(url)
        
        initialBlockNumber+=1

except JSONRPCException as e:
    print(f'RPC 호출 Error: {e}')
    dataframe = getDataFrame(listTxid, listTypes, listBRC20 ,listFrom, listTo, listURL)
    exportDataFrame(dataframe)

except Exception as e:
    print(f'Error 발생: {e}')
    print("현재까지 진행한 모든 것을 저장합니다.")
    dataframe = getDataFrame(listTxid, listTypes, listBRC20, listFrom, listTo, listURL)
    exportDataFrame(dataframe)

except:
    print("현재까지 진행한 모든 것을 저장합니다.")
    dataframe = getDataFrame(listTxid, listTypes, listBRC20, listFrom, listTo, listURL)
    exportDataFrame(dataframe)
