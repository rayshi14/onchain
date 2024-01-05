from web3 import Web3
from .base import *

class TxNode(Node):
    def __init__(self, id: str, deps: dict, params: dict, w3: Web3, pk: str):
        super().__init__(id, deps, params)
        self.wallet = params["wallet"]
        self.to = params["to"]
        self.amount = params["amount"]
        self.finality = params["finality"] if "finality" in params else 2
        self.gas = params["gas"] if "gas" in params else 21000
        self.output = None
        self.w3 = w3
        self.pk = pk
    
    def run(self, ctx: dict, values: dict):
        if self.finalized: # a new or finalized txn
            latest_block = self.w3.eth.get_block("latest")
            base_fee_per_gas = latest_block.baseFeePerGas   # Base fee in the latest block (in wei)
            max_priority_fee_per_gas = self.w3.to_wei(1, 'gwei') # Priority fee to include the transaction in the block
            max_fee_per_gas = (5 * base_fee_per_gas) + max_priority_fee_per_gas # Maximum amount you’re willing to pay 
            
            transaction_params = {
                'from': self.wallet,
                'to': self.to,
                'value': self.w3.to_wei(self.amount, 'ether'),
                'nonce': self.w3.eth.get_transaction_count(self.wallet) + ctx["pending_txs"][self.wallet],
                'gas': self.gas, 
                'maxFeePerGas': max_fee_per_gas, # Maximum amount you’re willing to pay 
                'maxPriorityFeePerGas': max_priority_fee_per_gas, # Priority fee to include the transaction in the block
                'chainId': 11155111 # ChainId of Sepolia Testnet
            }

            print('New transaction.', self.id)
            ctx["pending_txs"][self.wallet] += 1
            transaction = self.w3.eth.account.sign_transaction(transaction_params, self.pk)
            self.transaction_hash = self.w3.eth.send_raw_transaction(transaction.rawTransaction)
            
            print('Transaction sent!', self.id)
            self.tx_block = ctx["block_time"]
            self.finalized = False
            self.active = True
        elif ctx["block_time"] - self.tx_block >= self.finality:
            try:
                tx = self.w3.eth.get_transaction(self.transaction_hash)
                print('Transaction finalized.', self.id, tx)
                ctx["pending_txs"][self.wallet] -= 1
                self.finalized = True
                self.active = True
            except Exception as e:
                ctx["pending_tx"][self.wallet] -= 1
                print(e)