
from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools

account = Account.create()
logger.debug(f'address:{account.address}')
logger.debug(f'key:{account.key.hex()}')
# TODO 填写你的 YesCaptcha client key 或者2Captcha API Key 或者 ez-captcha ClientKey
client_key = 'd5bef70c94be797fb54dfd645a5900a1a9b2a4d035135'
# 使用yescaptcha solver googlev3
bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
# 使用2captcha solver googlev3
# bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='2captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
# 使用ez-captcha solver googlev3
# bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='ez-captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')

# 不使用代理
result = bera.claim_bera()
# 使用代理


# result = bera.claim_bera(proxies={'http':"http://127.0.0.1:8888","https":"http://127.0.0.1:8888"})

# result = bera.claim_bera(proxies={'http':"http://cynwqogi:GIoQcmRWZn2CNXvs@proxy.proxy-cheap.com:31112"})
logger.debug(result.text)
