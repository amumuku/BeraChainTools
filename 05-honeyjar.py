

from eth_account import Account
from loguru import logger
import time

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address
from bera_tools import BeraChainTools
from config.address_config import bend_address, weth_address, honey_address, bend_pool_address
from dotenv import dotenv_values


config = dotenv_values(".env")

token_address_list_str = config['KEY_LIST']
token_address_list = token_address_list_str.split(',')

def honeyTaskjar():
    while True:
        for token_address in token_address_list:
            try:
                account = Account.from_key(token_address)
                bera = BeraChainTools(private_key=account.key, solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')


                # https://faucet.0xhoneyjar.xyz/mint
                # 授权
                approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
                if approve_result != True:
                    honey_jar_mint_approve = bera.w3.eth.wait_for_transaction_receipt(approve_result)
                    logger.debug(f"[honeyjar] honey_jar_mint approve_token success {honey_jar_mint_approve}")
                # 花费4.2 honey mint
                result = bera.honey_jar_mint()
                logger.debug(f"[honeyjar]  honey_jar_mint start  {result}")

                honey_jar_mint_result = bera.w3.eth.wait_for_transaction_receipt(result)

                logger.debug(f"[honeyjar]  honey_jar  success {honey_jar_mint_result}")
            except Exception as e:
                    print(f"[honeyjar] 发生错误: {e}")
                    time.sleep(10)  # 休眠10秒
                    continue
            

if __name__ == "__main__":
    honeyTaskjar()
