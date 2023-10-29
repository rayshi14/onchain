import requests
import libs.common.etherscan as etherscan_api

class PoolV2:
    def __init__(self, proxy_addr = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", impl_addr = "0x085E34722e04567Df9E6d2c32e82fd74f3342e79"):
        self.pool_contract = etherscan_api.get_contract(proxy_addr,impl_addr)
    
    def get_user_account(self, wallet, block_number):
        return self.pool_contract.functions.getUserAccountData(wallet).call(block_identifier=block_number)