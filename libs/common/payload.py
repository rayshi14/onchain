def get_erc20_balance_payload(id, token_contract, wallet, block_number):
    payload = {
        "id":0,
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

def get_eth_balance_payload(id, token_contract, wallet, block_number):
    payload = {
        "id":0,
        "jsonrpc":"2.0",
        "method":"eth_getBalance",
        "params": [
            wallet,
            hex(block_number)
        ]
    }
    return payload