import libs.common.utils as utils

# get erc20 balance
def erc20_balance_payload(id, token_contract, wallet, block_number):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_call",
        "params": [
            {
                "to": token_contract,
                "data": "0x70a08231000000000000000000000000" + wallet[2:]
            },
            block_number
        ]
    }
    return payload

# get eth balance
def eth_balance_payload(id, wallet, block_number):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getBalance",
        "params": [
            wallet,
            block_number
        ]
    }
    return payload

def erc20_decimals_payload(id, token_contract):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_call",
        "params": [
            {
                "to": token_contract,
                "data": "0x313ce567"
            }
        ]
    }
    return payload

# get block info
def eth_block_payload(id, block_number, transaction_detail_flag=False):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getBlockByNumber",
        "params": [
            block_number,
            transaction_detail_flag
        ]
    }
    return payload

def eth_logs_by_block_payload(id, from_block, to_block):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getLogs",
        "params": [
            {
                "fromBlock":from_block,
                "toBlock":to_block
            }
        ]
    }
    return payload


def eth_logs_by_block_address_payload(id, from_block, to_block, addresses):
    payload = {
        "id":id,
        "jsonrpc":"2.0",
        "method":"eth_getLogs",
        "params": [
            {
                "fromBlock":from_block,
                "toBlock":to_block,
                "address":addresses
            }
        ]
    }
    return payload

# generic payload for function calls
def func_call_payload(id, contract_address, function_sig, block_number, values):
    func_hex = utils.get_function_hex(function_sig)
    param_types = utils.get_function_param_types(function_sig)
    assert len(param_types) == len(values)
    data = func_hex
    
    for t, v in zip(param_types,values):
        if type(v) == str: # address
            data += v[2:].zfill(64)
        else:
            data += hex(v)[2:].zfill(64)
    
    payload = {
        "id":0,
        "jsonrpc":"2.0",
        "method":"eth_call",
        "params": [
            {
                "to": contract_address,
                "data": data
            },
            block_number
        ]
    }
    return payload