import time
import schedule
from eth_account import Account
from loguru import logger
from bera_tools import BeraChainTools
from dotenv import dotenv_values
from dotenv import dotenv_values, set_key


def run_logic():
    config = dotenv_values(".env")
    client_key = config['CLIENT_KEY']
    account = Account.create()
    logger.debug(f'address:{account.address}')
    logger.debug(f'key:{account.key.hex()}')

    bera = BeraChainTools(private_key=account.key, client_key=client_key, solver_provider='yescaptcha', rpc_url='https://rpc.ankr.com/berachain_testnet')

    result = bera.claim_bera()
    logger.debug(result.text)
    new_key = account.key.hex()
    existing_key_list = config.get('KEY_LIST', '')
    updated_key_list = ','.join([existing_key_list, new_key]) if existing_key_list else new_key
    set_key('.env', 'KEY_LIST', updated_key_list)
def main():
    # Run the logic immediately
    run_logic()

    # Schedule the logic to run every 8 hours
    schedule.every(9).hours.do(run_logic)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()