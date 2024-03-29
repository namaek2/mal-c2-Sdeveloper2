from web3 import Web3
from pprint import pprint
from money import account
from money import txid

# Ropsten 테스트넷에 접속합니다. 이는 Infura 또는 다른 서비스를 통해 접속할 수 있습니다.
# 여기서는 예시로 Infura를 사용하며, 자신의 프로젝트 ID로 대체해야 합니다.
infura_url = 'https://rpc.sepolia.org'
web3 = Web3(Web3.HTTPProvider(infura_url))

# 잔액을 확인하고자 하는 계좌 주소를 설정합니다.

# 계좌의 잔액을 조회합니다.
balance = web3.eth.get_balance(account)

# txid에 대한 결과를 반환
transaction = web3.eth.get_transaction(txid)

# Wei 단위의 잔액을 Ether로 변환하여 출력합니다.
print(f'Account balance: {balance} wei')
print(f'Account balance: {web3.from_wei(balance, "ether")} ETH')

pprint(dict(transaction))