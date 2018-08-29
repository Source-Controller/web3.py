import functools
import json
import pytest

from eth_utils import (
    apply_key_map,
    encode_hex,
    event_signature_to_log_topic,
)

from web3 import Web3
from web3.providers.eth_tester import (
    EthereumTesterProvider,
)


@pytest.fixture()
def web3(request):
    provider = EthereumTesterProvider()
    w3 = Web3(provider)

    return w3


@pytest.fixture(autouse=True)
def wait_for_mining_start(web3, wait_for_block):
    wait_for_block(web3)


CONTRACT_EMITTER_CODE = "608060405234801561001057600080fd5b50610e10806100206000396000f300608060405260043610610099576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806317c0c1801461009e57806320f0256e146100ce57806390b41d8b14610126578063966b50e01461016a5780639c37705314610213578063aa6fd82214610261578063acabb9ed1461029b578063b2ddc4491461034a578063f82ef69e146103ad575b600080fd5b3480156100aa57600080fd5b506100cc600480360381019080803560ff169060200190929190505050610410565b005b3480156100da57600080fd5b50610124600480360381019080803560ff16906020019092919080359060200190929190803590602001909291908035906020019092919080359060200190929190505050610527565b005b34801561013257600080fd5b50610168600480360381019080803560ff169060200190929190803590602001909291908035906020019092919050505061069b565b005b34801561017657600080fd5b506102116004803603810190808035906020019082018035906020019080806020026020016040519081016040528093929190818152602001838360200280828437820191505050505050919291929080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290505050610830565b005b34801561021f57600080fd5b5061025f600480360381019080803560ff1690602001909291908035906020019092919080359060200190929190803590602001909291905050506108ef565b005b34801561026d57600080fd5b50610299600480360381019080803560ff16906020019092919080359060200190929190505050610a52565b005b3480156102a757600080fd5b50610348600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610bc8565b005b34801561035657600080fd5b506103ab600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610ccb565b005b3480156103b957600080fd5b5061040e600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610d49565b005b6001601081111561041d57fe5b81601081111561042957fe5b1415610460577f1e86022f78f8d04f8e3dfd13a2bdb280403e6632877c0dbee5e4eeb259908a5c60405160405180910390a1610524565b6000601081111561046d57fe5b81601081111561047957fe5b141561048f5760405160405180910390a0610523565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b50565b6005601081111561053457fe5b85601081111561054057fe5b141561059a577ff039d147f23fe975a4254bdf6b1502b8c79132ae1833986b7ccef2638e73fdf9848484846040518085815260200184815260200183815260200182815260200194505050505060405180910390a1610694565b600b60108111156105a757fe5b8560108111156105b357fe5b14156105ff5780827fa30ece802b64cd2b7e57dabf4010aabf5df26d1556977affb07b98a77ad955b58686604051808381526020018281526020019250505060405180910390a3610693565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5050505050565b600360108111156106a857fe5b8360108111156106b457fe5b14156106fe577fdf0cb1dea99afceb3ea698d62e705b736f1345a7eee9eb07e63d1f8f556c1bc58282604051808381526020018281526020019250505060405180910390a161082b565b6009601081111561070b57fe5b83601081111561071757fe5b141561075a57807f057bc32826fbe161da1c110afcdcae7c109a8b69149f727fc37a603c60ef94ca836040518082815260200191505060405180910390a261082a565b6008601081111561076757fe5b83601081111561077357fe5b14156107955780826040518082815260200191505060405180910390a1610829565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b505050565b8160405180828051906020019060200280838360005b83811015610861578082015181840152602081019050610846565b5050505090500191505060405180910390207fdbc4c1d1d2f0d84e58d36ca767ec9ba2ec2f933c055e50e5ccdd57697f7b58b0826040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156108d85780820151818401526020810190506108bd565b505050509050019250505060405180910390a25050565b600460108111156108fc57fe5b84601081111561090857fe5b141561095a577f4a25b279c7c585f25eda9788ac9420ebadae78ca6b206a0e6ab488fd81f5506283838360405180848152602001838152602001828152602001935050505060405180910390a1610a4c565b600a601081111561096757fe5b84601081111561097357fe5b14156109b75780827ff16c999b533366ca5138d78e85da51611089cd05749f098d6c225d4cd42ee6ec856040518082815260200191505060405180910390a3610a4b565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b50505050565b60026010811115610a5f57fe5b826010811115610a6b57fe5b1415610aad577f56d2ef3c5228bf5d88573621e325a4672ab50e033749a601e4f4a5e1dce905d4816040518082815260200191505060405180910390a1610bc4565b60076010811115610aba57fe5b826010811115610ac657fe5b1415610afe57807ff70fe689e290d8ce2b2a388ac28db36fbb0e16a6d89c6804c461f65a1b40bb1560405160405180910390a2610bc3565b60066010811115610b0b57fe5b826010811115610b1757fe5b1415610b2e578060405160405180910390a1610bc2565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b5050565b816040518082805190602001908083835b602083101515610bfe5780518252602082019150602081019050602083039250610bd9565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405180910390207fe77cf33df73da7bc2e253a2dae617e6f15e4e337eaa462a108903af4643d1b75826040518080602001828103825283818151815260200191508051906020019080838360005b83811015610c8d578082015181840152602081019050610c72565b50505050905090810190601f168015610cba5780820380516001836020036101000a031916815260200191505b509250505060405180910390a25050565b8173ffffffffffffffffffffffffffffffffffffffff167ff922c215689548d72c3d2fe4ea8dafb2a30c43312c9b43fe5d10f713181f991c82604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390a25050565b7f06029e18f16caae06a69281f35b00ed3fcf47950e6c99dafa1bdd8c4b93479a08282604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019250505060405180910390a150505600a165627a7a723058206b3490a28a048def91b89411c0c79f38d5763996fb4dc8e14e0ee0a965d482830029"  # noqa: E501

CONTRACT_EMITTER_RUNTIME = "608060405260043610610099576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806317c0c1801461009e57806320f0256e146100ce57806390b41d8b14610126578063966b50e01461016a5780639c37705314610213578063aa6fd82214610261578063acabb9ed1461029b578063b2ddc4491461034a578063f82ef69e146103ad575b600080fd5b3480156100aa57600080fd5b506100cc600480360381019080803560ff169060200190929190505050610410565b005b3480156100da57600080fd5b50610124600480360381019080803560ff16906020019092919080359060200190929190803590602001909291908035906020019092919080359060200190929190505050610527565b005b34801561013257600080fd5b50610168600480360381019080803560ff169060200190929190803590602001909291908035906020019092919050505061069b565b005b34801561017657600080fd5b506102116004803603810190808035906020019082018035906020019080806020026020016040519081016040528093929190818152602001838360200280828437820191505050505050919291929080359060200190820180359060200190808060200260200160405190810160405280939291908181526020018383602002808284378201915050505050509192919290505050610830565b005b34801561021f57600080fd5b5061025f600480360381019080803560ff1690602001909291908035906020019092919080359060200190929190803590602001909291905050506108ef565b005b34801561026d57600080fd5b50610299600480360381019080803560ff16906020019092919080359060200190929190505050610a52565b005b3480156102a757600080fd5b50610348600480360381019080803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610bc8565b005b34801561035657600080fd5b506103ab600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610ccb565b005b3480156103b957600080fd5b5061040e600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610d49565b005b6001601081111561041d57fe5b81601081111561042957fe5b1415610460577f1e86022f78f8d04f8e3dfd13a2bdb280403e6632877c0dbee5e4eeb259908a5c60405160405180910390a1610524565b6000601081111561046d57fe5b81601081111561047957fe5b141561048f5760405160405180910390a0610523565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b50565b6005601081111561053457fe5b85601081111561054057fe5b141561059a577ff039d147f23fe975a4254bdf6b1502b8c79132ae1833986b7ccef2638e73fdf9848484846040518085815260200184815260200183815260200182815260200194505050505060405180910390a1610694565b600b60108111156105a757fe5b8560108111156105b357fe5b14156105ff5780827fa30ece802b64cd2b7e57dabf4010aabf5df26d1556977affb07b98a77ad955b58686604051808381526020018281526020019250505060405180910390a3610693565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5050505050565b600360108111156106a857fe5b8360108111156106b457fe5b14156106fe577fdf0cb1dea99afceb3ea698d62e705b736f1345a7eee9eb07e63d1f8f556c1bc58282604051808381526020018281526020019250505060405180910390a161082b565b6009601081111561070b57fe5b83601081111561071757fe5b141561075a57807f057bc32826fbe161da1c110afcdcae7c109a8b69149f727fc37a603c60ef94ca836040518082815260200191505060405180910390a261082a565b6008601081111561076757fe5b83601081111561077357fe5b14156107955780826040518082815260200191505060405180910390a1610829565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b505050565b8160405180828051906020019060200280838360005b83811015610861578082015181840152602081019050610846565b5050505090500191505060405180910390207fdbc4c1d1d2f0d84e58d36ca767ec9ba2ec2f933c055e50e5ccdd57697f7b58b0826040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156108d85780820151818401526020810190506108bd565b505050509050019250505060405180910390a25050565b600460108111156108fc57fe5b84601081111561090857fe5b141561095a577f4a25b279c7c585f25eda9788ac9420ebadae78ca6b206a0e6ab488fd81f5506283838360405180848152602001838152602001828152602001935050505060405180910390a1610a4c565b600a601081111561096757fe5b84601081111561097357fe5b14156109b75780827ff16c999b533366ca5138d78e85da51611089cd05749f098d6c225d4cd42ee6ec856040518082815260200191505060405180910390a3610a4b565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b50505050565b60026010811115610a5f57fe5b826010811115610a6b57fe5b1415610aad577f56d2ef3c5228bf5d88573621e325a4672ab50e033749a601e4f4a5e1dce905d4816040518082815260200191505060405180910390a1610bc4565b60076010811115610aba57fe5b826010811115610ac657fe5b1415610afe57807ff70fe689e290d8ce2b2a388ac28db36fbb0e16a6d89c6804c461f65a1b40bb1560405160405180910390a2610bc3565b60066010811115610b0b57fe5b826010811115610b1757fe5b1415610b2e578060405160405180910390a1610bc2565b6040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260268152602001807f4469646e2774206d6174636820616e7920616c6c6f7761626c65206576656e7481526020017f20696e646578000000000000000000000000000000000000000000000000000081525060400191505060405180910390fd5b5b5b5050565b816040518082805190602001908083835b602083101515610bfe5780518252602082019150602081019050602083039250610bd9565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405180910390207fe77cf33df73da7bc2e253a2dae617e6f15e4e337eaa462a108903af4643d1b75826040518080602001828103825283818151815260200191508051906020019080838360005b83811015610c8d578082015181840152602081019050610c72565b50505050905090810190601f168015610cba5780820380516001836020036101000a031916815260200191505b509250505060405180910390a25050565b8173ffffffffffffffffffffffffffffffffffffffff167ff922c215689548d72c3d2fe4ea8dafb2a30c43312c9b43fe5d10f713181f991c82604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390a25050565b7f06029e18f16caae06a69281f35b00ed3fcf47950e6c99dafa1bdd8c4b93479a08282604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019250505060405180910390a150505600a165627a7a723058206b3490a28a048def91b89411c0c79f38d5763996fb4dc8e14e0ee0a965d482830029"  # noqa: E501

CONTRACT_EMITTER_ABI = json.loads('[{"constant":false,"inputs":[{"name":"which","type":"uint8"}],"name":"logNoArgs","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"which","type":"uint8"},{"name":"arg0","type":"uint256"},{"name":"arg1","type":"uint256"},{"name":"arg2","type":"uint256"},{"name":"arg3","type":"uint256"}],"name":"logQuadruple","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"which","type":"uint8"},{"name":"arg0","type":"uint256"},{"name":"arg1","type":"uint256"}],"name":"logDouble","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"arg0","type":"bytes2[]"},{"name":"arg1","type":"bytes2[]"}],"name":"logListArgs","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"which","type":"uint8"},{"name":"arg0","type":"uint256"},{"name":"arg1","type":"uint256"},{"name":"arg2","type":"uint256"}],"name":"logTriple","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"which","type":"uint8"},{"name":"arg0","type":"uint256"}],"name":"logSingle","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"arg0","type":"string"},{"name":"arg1","type":"string"}],"name":"logDynamicArgs","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"name":"logAddressIndexedArgs","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"name":"logAddressNotIndexedArgs","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":true,"inputs":[],"name":"LogAnonymous","type":"event"},{"anonymous":false,"inputs":[],"name":"LogNoArguments","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"}],"name":"LogSingleArg","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":false,"name":"arg1","type":"uint256"}],"name":"LogDoubleArg","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":false,"name":"arg1","type":"uint256"},{"indexed":false,"name":"arg2","type":"uint256"}],"name":"LogTripleArg","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":false,"name":"arg1","type":"uint256"},{"indexed":false,"name":"arg2","type":"uint256"},{"indexed":false,"name":"arg3","type":"uint256"}],"name":"LogQuadrupleArg","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"v","type":"string"}],"name":"LogString","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"v","type":"bytes"}],"name":"LogBytes","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"arg0","type":"uint256"}],"name":"LogSingleWithIndex","type":"event"},{"anonymous":true,"inputs":[{"indexed":true,"name":"arg0","type":"uint256"}],"name":"LogSingleAnonymous","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":true,"name":"arg1","type":"uint256"}],"name":"LogDoubleWithIndex","type":"event"},{"anonymous":true,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":true,"name":"arg1","type":"uint256"}],"name":"LogDoubleAnonymous","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":true,"name":"arg1","type":"uint256"},{"indexed":true,"name":"arg2","type":"uint256"}],"name":"LogTripleWithIndex","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"uint256"},{"indexed":false,"name":"arg1","type":"uint256"},{"indexed":true,"name":"arg2","type":"uint256"},{"indexed":true,"name":"arg3","type":"uint256"}],"name":"LogQuadrupleWithIndex","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"arg0","type":"string"},{"indexed":false,"name":"arg1","type":"string"}],"name":"LogDynamicArgs","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"arg0","type":"bytes2[]"},{"indexed":false,"name":"arg1","type":"bytes2[]"}],"name":"LogListArgs","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"arg0","type":"address"},{"indexed":false,"name":"arg1","type":"address"}],"name":"LogAddressIndexed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"arg0","type":"address"},{"indexed":false,"name":"arg1","type":"address"}],"name":"LogAddressNotIndexed","type":"event"}]')  # noqa: E501


@pytest.fixture()
def EMITTER_CODE():
    return CONTRACT_EMITTER_CODE


@pytest.fixture()
def EMITTER_RUNTIME():
    return CONTRACT_EMITTER_RUNTIME


@pytest.fixture()
def EMITTER_ABI():
    return CONTRACT_EMITTER_ABI


@pytest.fixture()
def EMITTER(EMITTER_CODE,
            EMITTER_RUNTIME,
            EMITTER_ABI):
    return {
        'bytecode': EMITTER_CODE,
        'bytecode_runtime': EMITTER_RUNTIME,
        'abi': EMITTER_ABI,
    }


@pytest.fixture()
def Emitter(web3, EMITTER):
    return web3.eth.contract(**EMITTER)


@pytest.fixture()
def emitter(web3, Emitter, wait_for_transaction, wait_for_block, address_conversion_func):
    wait_for_block(web3)
    deploy_txn_hash = Emitter.constructor().transact({'from': web3.eth.coinbase, 'gas': 1000000})
    deploy_receipt = wait_for_transaction(web3, deploy_txn_hash)
    contract_address = address_conversion_func(deploy_receipt['contractAddress'])

    bytecode = web3.eth.getCode(contract_address)
    assert bytecode == Emitter.bytecode_runtime
    _emitter = Emitter(address=contract_address)
    assert _emitter.address == contract_address
    return _emitter


class LogFunctions:
    LogAnonymous = 0
    LogNoArguments = 1
    LogSingleArg = 2
    LogDoubleArg = 3
    LogTripleArg = 4
    LogQuadrupleArg = 5
    LogSingleAnonymous = 6
    LogSingleWithIndex = 7
    LogDoubleAnonymous = 8
    LogDoubleWithIndex = 9
    LogTripleWithIndex = 10
    LogQuadrupleWithIndex = 11
    LogBytes = 12
    LogString = 13
    LogDynamicArgs = 14
    LogListArgs = 15
    LogAddressIndexed = 16
    LogAddressNotIndexed = 17


@pytest.fixture()
def emitter_event_ids():
    return LogFunctions


class LogTopics:
    LogAnonymous = encode_hex(event_signature_to_log_topic("LogAnonymous()"))
    LogNoArguments = encode_hex(event_signature_to_log_topic("LogNoArguments()"))
    LogSingleArg = encode_hex(event_signature_to_log_topic("LogSingleArg(uint256)"))
    LogSingleAnonymous = encode_hex(event_signature_to_log_topic("LogSingleAnonymous(uint256)"))
    LogSingleWithIndex = encode_hex(event_signature_to_log_topic("LogSingleWithIndex(uint256)"))
    LogDoubleArg = encode_hex(event_signature_to_log_topic("LogDoubleArg(uint256,uint256)"))
    LogDoubleAnonymous = encode_hex(event_signature_to_log_topic("LogDoubleAnonymous(uint256,uint256)"))  # noqa: E501
    LogDoubleWithIndex = encode_hex(event_signature_to_log_topic("LogDoubleWithIndex(uint256,uint256)"))  # noqa: E501
    LogTripleArg = encode_hex(event_signature_to_log_topic("LogTripleArg(uint256,uint256,uint256)"))
    LogTripleWithIndex = encode_hex(event_signature_to_log_topic("LogTripleWithIndex(uint256,uint256,uint256)"))  # noqa: E501
    LogQuadrupleArg = encode_hex(event_signature_to_log_topic("LogQuadrupleArg(uint256,uint256,uint256,uint256)"))  # noqa: E501
    LogQuadrupleWithIndex = encode_hex(event_signature_to_log_topic("LogQuadrupleWithIndex(uint256,uint256,uint256,uint256)"))  # noqa: E501
    LogBytes = encode_hex(event_signature_to_log_topic("LogBytes(bytes)"))
    LogString = encode_hex(event_signature_to_log_topic("LogString(string)"))
    LogDynamicArgs = encode_hex(event_signature_to_log_topic("LogDynamicArgs(string,string)"))
    LogListArgs = encode_hex(event_signature_to_log_topic("LogListArgs(bytes2[],bytes2[])"))
    LogAddressIndexed = encode_hex(event_signature_to_log_topic(
        "LogAddressIndexed(address,address)"))
    LogAddressNotIndexed = encode_hex(event_signature_to_log_topic(
        "LogAddressNotIndexed(address,address)"))


@pytest.fixture()
def emitter_log_topics():
    return LogTopics


def return_filter_by_api(
        api_style=None,
        contract=None,
        args=[]):
    if api_style == 'v4':
        event_name = args[0]
        kwargs = apply_key_map({'filter': 'argument_filters'}, args[1])
        if 'fromBlock' not in kwargs:
            kwargs['fromBlock'] = 'latest'
        return contract.events[event_name].createFilter(**kwargs)
    else:
        raise ValueError("api_style must be 'v3 or v4'")


@pytest.fixture(params=['v3', 'v4'])
def create_filter(request):
    return functools.partial(return_filter_by_api, request.param)
