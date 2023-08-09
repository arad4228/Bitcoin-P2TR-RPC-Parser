from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from rpc_config import *
from rpc_pandas import *

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# initialBlockNumber = 400000
initialBlockNumber = 789024

listTxid = []
listTypes = []
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

            is_P2TR = False
            is_TapTree = False
            # inner transaction from addresses
            From = []

            # if transaction not coinbase, collect all vin transaction.
            for vin in Json_transaction['vin']:
                # check witness_v1_taproot
                utxo = vin['txid']
                index = vin['vout']
                utxo_transaction = rpc_connection.getrawtransaction(utxo, 2)
                From.append(utxo_transaction['vout'][index]['scriptPubKey']['address'])

                # if uxto witness is 'witness_v1_taproot
                if utxo_transaction['vout'][index]['scriptPubKey']['type'] != "witness_v1_taproot":
                    continue

                is_P2TR = True

                # if not taproot spent transaction
                if len(vin['txinwitness']) == 3:
                    is_TapTree = True
            
            # if transaction is not p2tr type
            if not is_P2TR:
                # clear From list
                From.clear()
                continue
            
            # else
            To = []
            for vout in Json_transaction['vout']:
                To.append(vout['scriptPubKey']['address'])
            
            Types = []
            if is_TapTree:
                Types.append("TapTree")
            else:
                Types.append("TapRoot")
            
            listTxid.append(transaction)
            listTypes.append(Types)
            listFrom.append(From)
            listTo.append(To)
            listURL.append(url)

except JSONRPCException as e:
    print(f'RPC 호출 Error: {e}')
    dataframe = getDataFrame(listTxid, listTypes, listFrom, listTo, listURL)
    exportDataFrame(dataframe)
except KeyboardInterrupt:
    print("현재까지 진행한 모든 것을 저장합니다.")
    dataframe = getDataFrame(listTxid, listTypes, listFrom, listTo, listURL)
    exportDataFrame(dataframe)