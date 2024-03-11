import time
from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address,bex_swap_address
)

from dotenv import dotenv_values

config = dotenv_values(".env")

token_address_list_str = config['KEY_LIST']
token_address_list = token_address_list_str.split(',')

def bexTaskDex():
    while True:
        for token_address in token_address_list:
            try:
                account = Account.from_key(token_address)
                bera = BeraChainTools(private_key=account.key, solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')

                # # # bex 使用bera交换usdc
                bera_balance = bera.w3.eth.get_balance(account.address)
                logger.debug(f"[Bex]{account.address} bera_balance get_balance {bera_balance}")

                result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, usdc_address)
                logger.debug(f"[Bex]bex_swap wbear_address  usdc_address :{result}")


            #     # # bex 使用usdc交换weth
                usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
                logger.debug(f"[Bex]{account.address} usdc_balance get_balance {usdc_balance}")


            # #    #授权usdc
                approve_result_usdc_swap =  bera.approve_token(bex_swap_address, int("0x" + "f" * 64, 16), usdc_address)
                logger.debug(f"[Bex]bex_swap_address start approve usdc_address waiting confirm:{approve_result_usdc_swap}")
                if approve_result_usdc_swap != True:
                    tx_receipt_usdc_swap_approve = bera.w3.eth.wait_for_transaction_receipt(approve_result_usdc_swap)
                    logger.debug(f"[Bex]confirm approve_token success {tx_receipt_usdc_swap_approve}")

                result = bera.bex_swap(int(usdc_balance * 0.2), usdc_address, weth_address)
                logger.debug(f"[Bex]bex_swap usdc_address start bex_swap :{result}")



                tx_receipt = bera.w3.eth.wait_for_transaction_receipt(result)
                logger.debug(f"[Bex]bex_swap usdc_address success bex_swap :{tx_receipt}")

            #     # 授权usdc
                approve_result_usdc = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
                logger.debug(f"[Bex]bex_approve_liquidity_address start approve usdc_address waiting confirm:{approve_result_usdc}")
                if approve_result_usdc !=True:
                    tx_receipt_usdc = bera.w3.eth.wait_for_transaction_receipt(approve_result_usdc)
                    logger.debug(f"[Bex]bex_approve_liquidity_address approve success:{tx_receipt_usdc}")


                # bex 增加 usdc 流动性
                usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
                result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
                logger.debug(f"[Bex]bex_add_liquidity usdc_address success: {result}")

                #授权weth
                approve_result_eth_liquid = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
                logger.debug(f"[Bex]bex_approve_liquidity_address start approve weth_address waiting confirm:{approve_result_eth_liquid}")

                if approve_result_eth_liquid !=True:
                    tx_receipt_eth_liquid = bera.w3.eth.wait_for_transaction_receipt(approve_result_eth_liquid)
                    logger.debug(f"[Bex]bex_approve_liquidity_address approve success: {tx_receipt_eth_liquid}")

                # bex 增加 weth 流动性
                weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
                logger.debug(f"[Bex]call weth_balance  balance: {weth_balance}")

                result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
                logger.debug(f"[Bex]bex_add_liquidity weth_address  start: {result}")

                tx_receipt_eth_liquid = bera.w3.eth.wait_for_transaction_receipt(result)

                logger.debug(f"[Bex]bex_add_liquidity weth_address success: {tx_receipt_eth_liquid}")
            except Exception as e:
                print(f"发生错误: {e}")
                time.sleep(10)  # 休眠10秒
                continue

if __name__ == "__main__":
    bexTaskDex()
