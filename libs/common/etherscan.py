import requests
from web3 import Web3

node_url = "https://stylish-wider-patina.quiknode.pro/274049e810f4dee5f0807cd426196aeafd438838/"
w3 = Web3(Web3.HTTPProvider(node_url))

# get contract abi
def get_contract(contract_addr, impl_addr):
    abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={impl_addr}&api_key=HYY4PSB3NTBU6W4NCYURPJYMRET7WPBE26"
    abi = requests.get(abi_endpoint).json()
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_addr), abi=abi["result"])
    return contract