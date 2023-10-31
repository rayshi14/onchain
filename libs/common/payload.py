# get erc20 balance
def get_erc20_balance_payload(id, token_contract, wallet, block_number):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_call",
        "params": [
            {
                "to": token_contract,
                "data": "0x70a08231000000000000000000000000" + wallet[2:]
            },
            hex(block_number)
        ]
    }
    return payload

# get eth balance
def get_eth_balance_payload(id, wallet, block_number):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getBalance",
        "params": [
            wallet,
            hex(block_number)
        ]
    }
    return payload

# get block info
def get_eth_block_payload(id, block_number, transaction_detail_flag=False):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getBlockByNumber",
        "params": [
            hex(block_number),
            transaction_detail_flag
        ]
    }
    return payload

def get_eth_logs_by_block_payload(id, from_block, to_block):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getLogs",
        "params": [
            {
                "fromBlock":hex(from_block),
                "toBlock":hex(to_block)
            }
        ]
    }
    return payload
    
    