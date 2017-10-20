from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import time



abi_raw = '''[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_user","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferToken_toBalance","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_user","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferToken_toInvestBalance","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"add_tokens","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"investBalances","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"inputs":[],"payable":false,"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]'''
bytecode = '60606040526005805460a060020a60ff02191674020000000000000000000000000000000000000000179055341561003657600080fd5b5b60058054600160a060020a03191633600160a060020a039081169190911791829055633b9aca00600481905591166000908152600160205260409020555b5b610952806100856000396000f300606060405236156100e35763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166306fdde0381146100e8578063095ea7b31461017357806318160ddd146101a95780631feb3569146101ce57806323b872dd146101f257806327e235e31461022e578063313ce5671461025f57806370a08231146102885780638da5cb5b146102b957806395d89b41146102e8578063a9059cbb14610373578063ab430d49146103a9578063b556861a146103cd578063d915cdbd146103f1578063dd62ed3e14610422578063f2fde38b14610459575b600080fd5b34156100f357600080fd5b6100fb61047a565b60405160208082528190810183818151815260200191508051906020019080838360005b838110156101385780820151818401525b60200161011f565b50505050905090810190601f1680156101655780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561017e57600080fd5b610195600160a060020a03600435166024356104b1565b604051901515815260200160405180910390f35b34156101b457600080fd5b6101bc61051e565b60405190815260200160405180910390f35b34156101d957600080fd5b6101f0600160a060020a0360043516602435610524565b005b34156101fd57600080fd5b610195600160a060020a0360043581169060243516604435610574565b604051901515815260200160405180910390f35b341561023957600080fd5b6101bc600160a060020a036004351661066f565b60405190815260200160405180910390f35b341561026a57600080fd5b610272610681565b60405160ff909116815260200160405180910390f35b341561029357600080fd5b6101bc600160a060020a03600435166106a2565b60405190815260200160405180910390f35b34156102c457600080fd5b6102cc6106c1565b604051600160a060020a03909116815260200160405180910390f35b34156102f357600080fd5b6100fb6106d0565b60405160208082528190810183818151815260200191508051906020019080838360005b838110156101385780820151818401525b60200161011f565b50505050905090810190601f1680156101655780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561037e57600080fd5b610195600160a060020a0360043516602435610707565b604051901515815260200160405180910390f35b34156103b457600080fd5b6101f0600160a060020a03600435166024356107b3565b005b34156103d857600080fd5b6101f0600160a060020a0360043516602435610803565b005b34156103fc57600080fd5b6101bc600160a060020a036004351661085a565b60405190815260200160405180910390f35b341561042d57600080fd5b6101bc600160a060020a036004358116906024351661086c565b60405190815260200160405180910390f35b341561046457600080fd5b6101f0600160a060020a0360043516610899565b005b60408051908101604052600f81527f4e616d65206f6620436f6d70616e790000000000000000000000000000000000602082015281565b600160a060020a03338116600081815260036020908152604080832094871680845294909152808220859055909291907f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b9259085905190815260200160405180910390a35060015b92915050565b60045481565b60055433600160a060020a0390811691161461053f57600080fd5b600160a060020a038216600090815260026020908152604080832080548590039055600190915290208054820190555b5b5050565b600160a060020a038084166000908152600360209081526040808320339094168352929052908120548211156105a957600080fd5b600160a060020a0384166000908152600160205260409020548290108015906105d25750600082115b1561066357600160a060020a03808516600081815260016020908152604080832080548890039055878516808452818420805489019055848452600383528184203390961684529490915290819020805486900390557fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9085905190815260200160405180910390a3506001610667565b5060005b5b9392505050565b60016020526000908152604090205481565b60055474010000000000000000000000000000000000000000900460ff1681565b600160a060020a0381166000908152600160205260409020545b919050565b600554600160a060020a031681565b60408051908101604052600381527f4c4c4c0000000000000000000000000000000000000000000000000000000000602082015281565b6000600160a060020a038316151561071e57600080fd5b600160a060020a0333166000908152600160205260409020548290101561074457600080fd5b600160a060020a033381166000818152600160205260408082208054879003905592861680825290839020805486019055917fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9085905190815260200160405180910390a35060015b92915050565b60055433600160a060020a039081169116146107ce57600080fd5b600160a060020a038216600090815260016020908152604080832080548590039055600290915290208054820190555b5b5050565b60055433600160a060020a0390811691161461081e57600080fd5b600554600160a060020a03908116600090815260016020908152604080832080548690039055928516825260029052208054820190555b5b5050565b60026020526000908152604090205481565b600160a060020a038083166000908152600360209081526040808320938516835292905220545b92915050565b60055433600160a060020a039081169116146108b457600080fd5b600554600160a060020a03828116911614156108cf57600080fd5b60058054600160a060020a03908116600090815260016020526040808220548584168084528284209190915584549093168252812055815473ffffffffffffffffffffffffffffffffffffffff19161790555b5b505600a165627a7a7230582072e00f8babb8728478006017e50be0014bf3b24da29d1d770ae75a378661c0770029'

class MMS():

    def __init__(self,  _address, _password):
        self.address = _address
        self.password= _password
        self.web3 = Web3(HTTPProvider('http://localhost:8545'))
        self.web3.personal.unlockAccount(self.address, self.password, 10000)
        #print('Last block is ' + str(self.web3.eth.blockNumber))
        #print('Accounts: ' + str(self.web3.eth.accounts))

    def deployContract(self, abi_raw, bytecode):
        abi = json.loads(abi_raw)
        self.tokenContract = self.web3.eth.contract(abi, bytecode=bytecode)
        tx_deploy_hash = self.tokenContract.deploy(transaction={"from": self.address})
        txn_receipt = self.web3.eth.getTransactionReceipt(tx_deploy_hash)
        while txn_receipt is None:
            time.sleep(1)
            print('Waiting when transaction will be mined')
            txn_receipt = self.web3.eth.getTransactionReceipt(tx_deploy_hash)
        self.contract_address = txn_receipt['contractAddress']
        self.contract = self.web3.eth.contract(abi=abi, address=self.contract_address)
        return self.contract_address

    # Проверка баланса счета, с которого можно торговать
    def balanceOf(self,_address):
        return self.contract.call().balanceOf(_address)

    # Проверка баланса счета, на который начисляются дивиденды
    def investBalances(self, _address):
        return self.contract.call().investBalances(_address)

    # Передача прав владения контрактом другому адресу - и баланс тоже ему переходит
    def transferOwnership(self, _address):
        return self.contract.transact({'from': self.address}).transferOwnership(_address)

    # Передача токенов с торгового счета владельца контракта на торговый счет другому адресу
    # Для передачи одного токена нужно в amount передавать 100
    def transfer(self, _to, _amount):
        return self.contract.transact({'from': self.address}).transfer(_to, _amount)

    # Перенос токена инвестора с торгового счета на дивидендовый
    def transferToken_toInvestBalance(self, _address, _amount):
        return self.contract.transact({'from': self.address}).transferToken_toInvestBalance(_address, _amount)

    # Начисляем дивиденды инвестору на инвесторский счет с торгового счета админа
    def add_tokens(self, _to, _amount):
        return self.contract.transact({'from': self.address}).add_tokens(_to, _amount)

    # Переводим токены инвестора с дивиденового счета на торговый его же
    def transferToken_toBalance(self, _address, _amount):
        return self.contract.transact({'from': self.address}).transferToken_toBalance(_address, _amount)

    # Полное имя токена
    def getName(self):
        return self.contract.call().name()

    # Символ токена - используется на биржах
    def getSymbol(self):
        return self.contract.call().symbol()

owner_address = '0xe4eeec77c89434c83cdbc12e2ead1b099fda69d6' # eth.accounts[0] например...
token = MMS(owner_address, '123')
contract_address = token.deployContract(abi_raw, bytecode)
print('Contract address - ' + contract_address)
print('Баланс админа (счет для торговли) - '  + str(token.balanceOf(owner_address)))
print('Баланс админа (дивидендовый) - ' + str(token.investBalances(owner_address)))
#print('Передача прав вдаления контракту другому адресу. Хеш транзакции -  ' + str(token.transferOwnership('0x9999999999899999999999999999999999999999')))
print('Пеерводим с админского торгового счета 1 токен на торговый счет другому адресу.А передаем в функцию 100, потому что у нас 2 знака после запятой Хеш - ' + token.transfer('0x9999999999899999999999999999999999999999',100))
print('А теперь подождем секунд 10, пока транзакция смайнится ')
time.sleep(10)
print('Смотрим торговый баланс адреса 0x9999999999899999999999999999999999999999 - ' + str(token.balanceOf('0x9999999999899999999999999999999999999999')))
print('Переведем токены инвестора 0x9999999999899999999999999999999999999999 c торгового счета на дипозитный. Подождем 10 сек')
print(str(token.transferToken_toInvestBalance('0x9999999999899999999999999999999999999999', 100)))
time.sleep(10)
print('Баланс 0x9999999999899999999999999999999999999999 (счет для торговли) - '  + str(token.balanceOf('0x9999999999899999999999999999999999999999')))
print('Баланс 0x9999999999899999999999999999999999999999 (дивидендовый) - ' + str(token.investBalances('0x9999999999899999999999999999999999999999')))
print('Начислим дивидендов инвестору 0x9999999999899999999999999999999999999999')
token.add_tokens('0x9999999999899999999999999999999999999999',300)
time.sleep(10)
print('Баланс 0x9999999999899999999999999999999999999999 (счет для торговли) - '  + str(token.balanceOf('0x9999999999899999999999999999999999999999')))
print('Баланс 0x9999999999899999999999999999999999999999 (дивидендовый) - ' + str(token.investBalances('0x9999999999899999999999999999999999999999')))
print('Баланс админа (счет для торговли) - '  + str(token.balanceOf(owner_address)))
print('Баланс админа (дивидендовый) - ' + str(token.investBalances(owner_address)))
time.sleep(10)
print('А теперь переведем все токены инвестора 0x9999999999899999999999999999999999999999 на торговый счет его')
token.transferToken_toBalance('0x9999999999899999999999999999999999999999',token.investBalances('0x9999999999899999999999999999999999999999'))
time.sleep(10)
print('Баланс 0x9999999999899999999999999999999999999999 (счет для торговли) - '  + str(token.balanceOf('0x9999999999899999999999999999999999999999')))
print('Баланс 0x9999999999899999999999999999999999999999 (дивидендовый) - ' + str(token.investBalances('0x9999999999899999999999999999999999999999')))
print('Полное имя токена - ' + token.getName())
print('Символ токена - ' + token.getSymbol())
