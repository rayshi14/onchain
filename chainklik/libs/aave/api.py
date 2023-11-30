import requests
import libs.common.etherscan as etherscan_api
from collections import namedtuple

ReserveConfig = namedtuple("ReserveConfig", "ltv liqThreshold liqBonus decimals active frozen borrowEnabled stableRateEnabled reserved reserveFactor")

class ReserveData:
    def __init__(self, raw_data):
        config_bits = [0,16,32,48,56,57,58,59,60,64,80]
        # get reserve config
        # bit 0-15: LTV
        # bit 16-31: Liq. threshold
        # bit 32-47: Liq. bonus
        # bit 48-55: Decimals
        # bit 56: Reserve is active
        # bit 57: reserve is frozen
        # bit 58: borrowing is enabled
        # bit 59: stable rate borrowing enabled
        # bit 60-63: reserved
        # bit 64-79: reserve factor
        b = "{0:b}".format(raw_data[0][0])
        b = '0'*(80-len(b)) + b
        self.reserve_config = ReserveConfig._make([int(b[len(b)-min(len(b),config_bits[i]):len(b)-min(len(b),config_bits[i-1])],2) for i in range(1,len(config_bits))])
        
        # the liquidity index. Expressed in ray
        self.liquidity_index = raw_data[1]/1e27
        # variable borrow index. Expressed in ray
        self.variable_borrow_index = raw_data[2]/1e27
        # the current supply rate. Expressed in ray
        self.current_liquidity_rate = raw_data[3]/1e27
        # the current variable borrow rate. Expressed in ray
        self.current_variable_borrow_rate = raw_data[4]/1e27
        # the current stable borrow rate. Expressed in ray
        self.current_stable_borrow_rate = raw_data[5]/1e27
        self.last_update_timestamp = raw_data[6]
        # tokens addresses
        self.aToken_address = raw_data[7]
        self.stable_debt_token_address = raw_data[8]
        self.variable_debt_token_address = raw_data[9]
        # address of the interest rate strategy
        self.interest_rate_strategy_address = raw_data[10]
        # the id of the reserve. Represents the position in the list of the active reserves
        self.id = raw_data[11]

# totalCollateralETH the total collateral in ETH of the user
# totalDebtETH the total debt in ETH of the user
# availableBorrowsETH the borrowing power left of the user
# currentLiquidationThreshold the liquidation threshold of the user
# ltv the loan to value of the user
# healthFactor the current health factor of the user
UserAccountData = namedtuple("UserAccountData", "totalCollateralETH totalDebtETH availableBorrowsETH currentLiquidationThreshold ltv healthFactor")

class PoolV2:
    def __init__(self, proxy_addr = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", impl_addr = "0x085E34722e04567Df9E6d2c32e82fd74f3342e79"):
        self.pool_contract = etherscan_api.get_contract(proxy_addr,impl_addr)
    
    def get_user_account(self, wallet, block_number):
        raw_data = self.pool_contract.functions.getUserAccountData(wallet).call(block_identifier=block_number)
        raw_data[0]/=1e18
        raw_data[1]/=1e18
        raw_data[2]/=1e18
        raw_data[5]/=1e18
        return UserAccountData._make(raw_data)
    
    def get_reserve_data(self, token_contract, block_number):
        raw_data = self.pool_contract.functions.getReserveData(token_contract).call(block_identifier=block_number)
        return ReserveData(raw_data)
    