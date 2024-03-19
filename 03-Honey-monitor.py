import time
from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import honey_swap_address, usdc_address, honey_address

from dotenv import dotenv_values

#config = dotenv_values(".env")

#token_address_list_str = config['KEY_LIST']
#token_address_list = token_address_list_str.split(',')

def honeyTaskHoney():
    while True:
        config = dotenv_values(".env")
        token_address_list_str = config['KEY_LIST']
        token_address_list = token_address_list_str.split(',')
        for token_address in token_address_list:
            try:
                account = Account.from_key(token_address)
                bera = BeraChainTools(private_key=account.key, solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
               
                # 授权usdc
                approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
                if approve_result != True:
                    tx_receipt_usdc_swap_approve = bera.w3.eth.wait_for_transaction_receipt(approve_result)
                    logger.debug(f"[Honey]confirm approve_token success {tx_receipt_usdc_swap_approve}")

                # 使用usdc mint honey
                usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
                logger.debug(f"[Honey] usdc_balance before honey_mint {usdc_balance}")

                result = bera.honey_mint(int(usdc_balance * 0.5))
                logger.debug(f"[Honey] honey_mint start {result}")

                tx_receipt_usdc_honey_mint = bera.w3.eth.wait_for_transaction_receipt(result)
                logger.debug(f"[Honey]confirm honey_mint success {tx_receipt_usdc_honey_mint}")

                # 授权honey
                approve_result_swap = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
                if approve_result != True:
                    tx_receipt_usdc_swap_approve = bera.w3.eth.wait_for_transaction_receipt(approve_result_swap)
                    logger.debug(f"[Honey]confirm honey_swap_address approve_token success {tx_receipt_usdc_swap_approve}")
                # 赎回 
                honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
                result = bera.honey_redeem(int(honey_balance * 0.5))
                tx_receipt_eth_liquid = bera.w3.eth.wait_for_transaction_receipt(result)
                logger.debug(f"[Honey]honey honey_redeem success: {tx_receipt_eth_liquid}")

            except Exception as e:
                print(f"发生错误: {e}")
                time.sleep(1000)  # 休眠10秒
                continue

if __name__ == "__main__":
    honeyTaskHoney() 