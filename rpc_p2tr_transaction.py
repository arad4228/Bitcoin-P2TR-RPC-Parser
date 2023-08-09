# 동작 과정에 대한 흐름.
# 가장 먼저 블록에서 모든 transaction을 가져온다.
# 해당 transaction에서 p2tr형식의 주소에서 나가는 transaction인지 check.
# 확인 방법은 vin의 transaction에 대해서 해당 transaction이 witness_v1_taproot인지 확인
# 만약 p2tr을 사용하는 transaction에서 taptree를 사용하는 transaction을 고른다.
# 고르는 방법은 cblock에 대한 정보를 확인한다. (Json Parsing)
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from rpc_config import *
import pandas as pd

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

initialBlockNumber = 400000

try:
    block_hash = rpc_connection.getblockhash(initialBlockNumber)
    block_info = rpc_connection.getblock(block_hash)
    transactions = block_info['tx']

    for transaction in transactions:
        print(f'Reading Transction is {transaction}')
        Json_transaction = rpc_connection.getrawtransaction(transaction, 2)
        # if transaction is coinbase, skip transaction next
        if 'coinbase' in Json_transaction['vin'][0]:
            print("this transaction is coinbase transaction")
            continue
        
except JSONRPCException as e:
    print(f'RPC 호출 Error: {e}')