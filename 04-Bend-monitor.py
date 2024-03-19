

from eth_account import Account
from loguru import logger
import time

from bera_tools import BeraChainTools
from config.address_config import bend_address, weth_address, honey_address, bend_pool_address
from dotenv import dotenv_values


#config = dotenv_values(".env")

#token_address_list_str = config['KEY_LIST']
#token_address_list = token_address_list_str.split(',')

def taskBend():
    while True:
        config = dotenv_values(".env")
        token_address_list_str = config['KEY_LIST']
        token_address_list = token_address_list_str.split(',')
        for token_address in token_address_list:
            try:
                account = Account.from_key(token_address)
                bera = BeraChainTools(private_key=account.key, solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
               
                #授权
                approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), weth_address)
                if approve_result != True:
                    tx_receipt_usdc_swap_approve = bera.w3.eth.wait_for_transaction_receipt(approve_result)
                    logger.debug(f"[Bend] bend_deposit approve_token success {tx_receipt_usdc_swap_approve}")
                # deposit
                weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
                logger.debug(f"[Bend]approve_result weth_balance success:{weth_balance}")
                result = bera.bend_deposit(int(weth_balance), weth_address)
                logger.debug(f"[Bend]bend_deposit start {result}")

                tx_receipt_bend_deposit = bera.w3.eth.wait_for_transaction_receipt(result)

                logger.debug(f"[Bend]bend_deposit result {tx_receipt_bend_deposit}")

                #borrow
                balance = bera.bend_contract.functions.getUserAccountData(account.address).call()[2]
                logger.debug(f"[Bend]getUserAccountData {balance}")
                result = bera.bend_borrow(int(balance * 0.4 * 1e10), honey_address)
                logger.debug(f"[Bend]bend_borrow start {result}")
                bend_borrow_result = bera.w3.eth.wait_for_transaction_receipt(result)
                logger.debug(f"[Bend]bend_borrow success {bend_borrow_result}")


                # 授权
                approve_result_borrow = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), honey_address)
                if approve_result_borrow != True:
                    tx_receipt_usdc_swap_approve_pay = bera.w3.eth.wait_for_transaction_receipt(approve_result_borrow)
                    logger.debug(f"[Bend] bend_repay approve_token success {tx_receipt_usdc_swap_approve_pay}")
                # 查询数量 
                call_result = bera.bend_borrows_contract.functions.getUserReservesData(bend_pool_address, bera.account.address).call()
                repay_amount = call_result[0][0][4]
                logger.debug(f"[Bend] bend_repay getUserReservesData  {repay_amount}")
                # repay
                result = bera.bend_repay(int(repay_amount * 0.9), honey_address)
                logger.debug(f"[Bend] bend_repay {result}")
                time.sleep(10)  # 休眠10秒
            except Exception as e:
                    print(f"[Bend] 发生错误: {e}")
                    time.sleep(1000)  # 休眠10秒
                    continue

if __name__ == "__main__":
    taskBend()