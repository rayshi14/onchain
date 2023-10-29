from web3 import Web3

def get_function_hex(function_sig): # function_sig = "balanceOf(address)"
    return Web3.keccak(text=function_sig)[:4].hex()