# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import requests
import web3.utils
from functools import wraps
import json
import time
import sys
import os
import uuid
import subprocess
from bs4 import BeautifulSoup
from eth_utils import encode_hex
from flask_sqlalchemy import SQLAlchemy
from database import *
from models import *
import hashlib
from datetime import datetime, timedelta

script_path = sys.argv[1]

node = conf.get("eth", "node")

class Gate():
    unlock = False
    def __init__(self,  _address, _password):
        self.address = _address
        self.password= _password
        self.web3 = Web3(HTTPProvider(node))
        self.unlock = self.web3.personal.unlockAccount(_address, _password, 10000)
        #self.web3.account.encrypt('0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef','123')



    def deployContract(self, abi_raw, bytecode, params, value=0):
        abi = json.loads(abi_raw)
        self.tokenContract = self.web3.eth.contract(abi, bytecode=bytecode)
        tx_deploy_hash = self.tokenContract.deploy(transaction={"from": self.address, "value": int(value)},args=params)
        txn_receipt = self.web3.eth.getTransactionReceipt(tx_deploy_hash)
        while txn_receipt is None:
            time.sleep(1)
            print('Waiting when transaction will be mined')
            txn_receipt = self.web3.eth.getTransactionReceipt(tx_deploy_hash)
        self.contract_address = txn_receipt['contractAddress']
        self.contract = self.web3.eth.contract(abi=abi, address=self.contract_address)
        return self.contract_address


    def getter(self, abi_raw, contract_address, var_name, params):
        self.contract = self.web3.eth.contract(abi=json.loads(abi_raw), address=contract_address)
        result = eval('self.contract.call().' + var_name + '(' + params + ')')
        return str(result)


    def setter(self, abi_raw, contract_address, value, var_name, params):
        self.contract = self.web3.eth.contract(abi=json.loads(abi_raw), address=contract_address)
        result = eval("self.contract.transact({'from': '" + self.address + "', 'value': " + value + "})." + var_name + "(" + params + ")")
        return str(result)


    def transact(self, address, value):
        return self.web3.eth.sendTransaction({'to': address, 'from': self.address, 'value': int(value), 'data':''})


    @staticmethod
    def verify_contract(address, name, compiler, source, params_encode, network):
        time.sleep(30)
        data = {}
        if params_encode is not None:
            abi_encoded = subprocess.check_output(['bash', '-c','cd ' + script_path + ' &&' + params_encode])
            abi_encoded = str(abi_encoded).replace("\n",'')
            abi_encoded = abi_encoded[4:-3]
            data['ctl00$ContentPlaceHolder1$txtConstructorArguements'] = str(abi_encoded)
        else:
            data['ctl00$ContentPlaceHolder1$txtConstructorArguements'] = ''
        data['ctl00$ContentPlaceHolder1$txtContractAddress'] = address
        data['ctl00$ContentPlaceHolder1$txtContractName'] = name
        data['ctl00$ContentPlaceHolder1$ddlCompilerVersions'] = compiler
        data['ctl00$ContentPlaceHolder1$txtSourceCode'] = source
        data['ctl00$ContentPlaceHolder1$ddlOptimization'] = 1
        data['ctl00$ContentPlaceHolder1$txtLibraryName1'] = ''
        data['ctl00$ContentPlaceHolder1$txtLibraryAddress1'] = '0x'
        data['ctl00$ContentPlaceHolder1$txtLibraryName2'] = ''
        data['ctl00$ContentPlaceHolder1$txtLibraryAddress2'] = '0x'
        data['ctl00$ContentPlaceHolder1$txtLibraryName3'] = ''
        data['ctl00$ContentPlaceHolder1$txtLibraryAddress3'] = '0x'
        data['ctl00$ContentPlaceHolder1$txtLibraryName4'] = ''
        data['ctl00$ContentPlaceHolder1$txtLibraryAddress4'] = '0x'
        data['ctl00$ContentPlaceHolder1$txtLibraryName5'] = ''
        data['ctl00$ContentPlaceHolder1$txtLibraryAddress5'] = '0x'
        data['ctl00$ContentPlaceHolder1$btnSubmit'] = 'Verify And Publish'
        data['ctl00$ContentPlaceHolder1$txtGithubGist'] = ''
        data['ctl00$ContentPlaceHolder1$hdnSelectedTab'] = 'bytecode'
        data['ctl00$ContentPlaceHolder1$libcounter'] = 1

        page = requests.get('https://' + network + 'etherscan.io/verifyContract?a='+ str(address)).content
        soup = BeautifulSoup(page)
        data["__EVENTTARGET"] = ''
        data["__EVENTARGUMENT"] = ''
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
        requests.post('https://' + network + 'etherscan.io/verifyContract', data=data)
        return 'OK'










def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('-----'+ str(f.__name__))
        request_token = request.headers['Authorization']
        signature = request.form['signature']
        token = Token.query.filter(Token.token == request_token).first()
        if token is None:
            return 'Token is invalid!'
        user = token.user
        hash = hashlib.md5(":".join((token.token, user.secret, str(user.nonce))).encode('utf-8')).hexdigest()
        if hash != signature:
            return 'Signature is invalid!'
        if datetime.now() > token.exp:
            db_session.delete(token)
            db_session.commit()
            return 'Token has expired!'
        user.nonce += 1
        token.exp += timedelta(minutes=token_update_time)
        db_session.commit()
        return f(*args, **kwargs)

    return decorated





def compile(source_code, contract_name):
    data = {}
    random_path = '/tmp/' + str(uuid.uuid4()) + '/'
    os.makedirs(random_path)
    file_path = random_path + contract_name + '.sol'
    file = open(file_path,"w")
    file.write(source_code)
    file.close()
    abi_file = random_path + contract_name + '.abi'
    bin_file = random_path + contract_name + '.bin'
    subprocess.check_output(['bash', '-c', 'solc --abi --bin --optimize -o ' + random_path + ' ' + file_path])
    if not os.path.isfile(file_path):
        data['error'] = 'Compile error'
        return data
    f = open(abi_file)
    data['abi'] = f.read().strip()
    f = open(bin_file)
    data['bin'] = f.read().strip()
    subprocess.check_output(['bash', '-c', 'rm -rf ' + random_path])
    return data





app = Flask(__name__)





@app.route('/ethapi/deploy', methods=['POST'])
#@requires_auth
def deploy():
    account = request.form['account']
    password = request.form['password']
    if 'source_code' in request.form:
        source_code = request.form['source_code']
        contract_name = request.form['contract_name']
        contract_data = compile(source_code, contract_name)
        if 'error' in contract_data:
            return contract_data['error']
        bytecode = contract_data['bin']
        abi_raw = str(contract_data['abi'])
        if 'compiler' in request.form:
            compiler = request.form['compiler']
        else:
            compiler = 'v0.4.18+commit.9cf6e910'

    else:
        bytecode = request.form['bytecode']
        abi_raw = request.form['abi']
        params_for_encode = None
    if 'params[]' in request.form:
        params_for_encode = "node encodeParameters.js '["
        params_list = request.form.getlist('params[]')
        abi_list = json.loads(abi_raw)
        abi_types = {}
        for indx, el in enumerate(abi_list):
            if abi_list[indx]['type'] == 'constructor':
                for ind, e in enumerate(abi_list[indx]['inputs']):
                    abi_types[ind] = e['type']
                    params_for_encode += '"' + e['type'] + '", '
        params_for_encode = params_for_encode[:-2] + "]' '["

        for indx, el in enumerate(params_list):
            if abi_types[indx].find('[]') != -1:
                params_list[indx] = eval(el)
                params_for_encode += el + ', '
            elif abi_types[indx].find('int') != -1 :
                params_list[indx] = int(el)
                params_for_encode += el + ', '
            elif abi_types[indx].find('bytes') != -1:
                params_list[indx] = Web3.toBytes(hexstr=el)
                params_for_encode += '"' + el + '", '
            else:
                params_for_encode += '"' + el + '", '

        params_for_encode = params_for_encode[:-2] + "]'"
        params = tuple(params_list)
    else:
        params = tuple()
    if 'value' not in request.form:
        value=0
    else:
        value = request.form['value']
    GateOnline = Gate(account, password)
    if GateOnline.unlock == False:
        return 'Unlock Account - False'
    address = GateOnline.deployContract(abi_raw, bytecode, params, value)
    if 'verify' in request.form:
        if 'network' in request.form:
            network = request.form['network'] + '.'
        else:
            network = ''
        Gate.verify_contract(address, contract_name, compiler, source_code, params_for_encode, network)
    return str(address)


@app.route('/ethapi/getter', methods=['POST'])
#@requires_auth
def getter():
    account = request.form['account']
    password = request.form['password']
    abi_raw = request.form['abi']
    contract_address = request.form['address']
    var_name = request.form['name']
    if 'params[]' in request.form:
        params_list = request.form.getlist('params[]')
        abi_list = json.loads(abi_raw)
        abi_types = {}
        for indx, el in enumerate(abi_list):
            if abi_list[indx]['type'] == 'constructor':
                for ind, e in enumerate(abi_list[indx]['inputs']):
                    abi_types[ind] = e['type']

        for indx, el in enumerate(params_list):
            if abi_types[indx].find('[]') != -1:
                params_list[indx] = eval(el)
            elif abi_types[indx].find('int') != -1 :
                params_list[indx] = int(el)
            elif abi_types[indx].find('bytes') != -1:
                params_list[indx] = Web3.toBytes(hexstr=el)
        params = str(params_list)[1:-1]
    else:
        params = ''
    GateOnline = Gate(account, password)
    if GateOnline.unlock == False:
        return 'Unlock Account - False'
    return GateOnline.getter(abi_raw, contract_address, var_name, params)


@app.route('/ethapi/setter', methods=['POST'])
#@requires_auth
def setter():
    account = request.form['account']
    password = request.form['password']
    abi_raw = request.form['abi']
    contract_address = request.form['address']
    var_name = request.form['name']
    if 'params[]' in request.form:
        params_list = request.form.getlist('params[]')
        abi_list = json.loads(abi_raw)
        abi_types = {}
        for indx, el in enumerate(abi_list):
            if abi_list[indx]['type'] == 'constructor':
                for ind, e in enumerate(abi_list[indx]['inputs']):
                    abi_types[ind] = e['type']

        for indx, el in enumerate(params_list):
            if abi_types[indx].find('int') != -1:
                params_list[indx] = int(el)
            elif abi_types[indx].find('[]') != -1:
                params_list[indx] = eval(el)
            elif abi_types[indx].find('bytes') != -1:
                params_list[indx] = Web3.toBytes(hexstr=el)
        params = str(params_list)[1:-1]
    else:
        params = ''
    if 'value' not in request.form:
        value = '0'
    else:
        value = request.form['value']
    GateOnline = Gate(account, password)
    if GateOnline.unlock == False:
        return 'Unlock Account - False'
    return GateOnline.setter(abi_raw, contract_address, value, var_name, params)


@app.route('/ethapi/transact', methods=['POST'])
#@requires_auth
def transact():
    account = request.form['account']
    password = request.form['password']
    contract_address = request.form['address']
    if 'value' not in request.form:
        return 'value - 0'
    else:
        value = request.form['value']
    GateOnline = Gate(account, password)
    if GateOnline.unlock == False:
        return 'Unlock Account - False'
    return GateOnline.transact(contract_address, value)


@app.route('/ethapi/verify', methods=['POST'])
#@requires_auth
def verify():
    source_code = request.form['source_code']
    contract_name = request.form['contract_name']
    abi_raw = request.form['abi']
    if 'compiler' in request.form:
        compiler = request.form['compiler']
    else:
        compiler = 'v0.4.18+commit.9cf6e910'
        source_code = request.form['source_code']
    params_for_encode = None
    if 'params[]' in request.form:
        params_for_encode = "node encodeParameters.js '["
        params_list = request.form.getlist('params[]')
        abi_list = json.loads(abi_raw)
        abi_types = {}
        for indx, el in enumerate(abi_list):
            if abi_list[indx]['type'] == 'constructor':
                for ind, e in enumerate(abi_list[indx]['inputs']):
                    abi_types[ind] = e['type']
                    params_for_encode += '"' + e['type'] + '", '
        params_for_encode = params_for_encode[:-2] + "]' '["

        for indx, el in enumerate(params_list):
            if abi_types[indx].find('[]') != -1:
                params_list[indx] = eval(el)
                params_for_encode += el + ', '
            elif abi_types[indx].find('int') != -1 :
                params_list[indx] = int(el)
                params_for_encode += el + ', '
            elif abi_types[indx].find('bytes') != -1:
                params_list[indx] = Web3.toBytes(hexstr=el)
                params_for_encode += '"' + el + '", '
            else:
                params_for_encode += '"' + el + '", '

        params_for_encode = params_for_encode[:-2] + "]'"

    if 'network' in request.form:
        network = request.form['network'] + '.'
    else:
        network = ''
    address = request.form['address']
    return Gate.verify_contract(address, contract_name, compiler, source_code, params_for_encode, network)


@app.route('/ethapi/auth', methods=['POST'])
def auth():
    login = request.form['login']
    password = request.form['password']
    signature = request.form['signature']
    user = User.query.filter(User.login == login).first()
    if user is None:
        return 'User does not exists!'
    secret = user.secret
    hash = hashlib.md5(":".join((login, password, secret, str(user.nonce))).encode('utf-8')).hexdigest()
    if signature == hash:
        token = Token.query.filter(Token.user_id == user.id).first()
        if token is not None:
            db_session.delete(token)
            db_session.commit()
        token = Token(user.id)
        db_session.add(token)
        user.nonce += 1
        db_session.commit()
        return str(token)
    else:
        return 'Auth error!'


@app.route('/ethapi/logout', methods=['POST'])
def logout():
    signature = request.form['signature']
    request_token = request.headers['Authorization']
    token = Token.query.filter(Token.token == request_token).first()
    if token is None:
        return 'Token is invalid!'
    user = token.user
    hash = hashlib.md5(":".join((token.token, user.secret, str(user.nonce))).encode('utf-8')).hexdigest()
    if hash != signature:
        return 'Signature is invalide!'
    user.nonce += 1
    db_session.delete(token)
    db_session.commit()
    return 'OK'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)