from hypothesis import (
    strategies as st,
    given,
)
import random


def pad_with_transactions(w3):
    accounts = w3.eth.accounts
    while True:
        transact = yield
        tx_hash = transact()
        for tx_count in range(random.randint(0, 10)):
            _from = accounts[random.randint(0, len(accounts) - 1)]
            _to = accounts[random.randint(0, len(accounts) - 1)]
            value = 50 + tx_count
            w3.eth.sendTransaction({'from': _from, 'to': _to, 'value': value})
        yield tx_hash


def single_transaction(w3):
    accounts = w3.eth.accounts
    while True:
        _from = accounts[random.randint(0, len(accounts) - 1)]
        _to = accounts[random.randint(0, len(accounts) - 1)]
        value = 50
        tx_hash = w3.eth.sendTransaction({'from': _from, 'to': _to, 'value': value})
        yield tx_hash


@given(seed=st.integers())
def test_event_filter_new_events(
        web3,
        emitter,
        Emitter,
        wait_for_transaction,
        emitter_event_ids,
        create_filter,
        seed):

    random.seed(seed)

    matching_transact = emitter.functions.logNoArgs(
        which=1).transact
    non_matching_transact = emitter.functions.logNoArgs(
        which=0).transact

    event_filter = emitter.events.LogNoArguments().createFilter(fromBlock='latest')

    expected_match_counter = 0

    tx_padder = pad_with_transactions(web3)
    tx_padder.send(None)
    while web3.eth.blockNumber < 50:
        is_match = bool(random.randint(0, 1))
        if is_match:
            expected_match_counter += 1
            tx_padder.send(matching_transact)
            next(tx_padder)
            continue
        tx_padder.send(non_matching_transact)
        next(tx_padder)

    assert len(event_filter.get_new_entries()) == expected_match_counter


@given(
    target_block_count=st.integers(min_value=1, max_value=100),
    seed=st.integers())
def test_block_filter(
        web3,
        target_block_count,
        seed):

    random.seed(seed)
    block_filter = web3.eth.filter("latest")

    target_block = random.randint(30, 55)
    tx_padder = pad_with_transactions(web3)
    tx_padder.send(None)
    while web3.eth.blockNumber < target_block:
        tx_padder.send(lambda: "ok")
        next(tx_padder)

    assert len(block_filter.get_new_entries()) == web3.eth.blockNumber


@given(target_tx_count=st.integers(min_value=1, max_value=100))
def test_transaction_filter_with_mining(
        web3,
        target_tx_count):

    transaction_filter = web3.eth.filter("pending")

    transaction_counter = 0

    transact_once = single_transaction(web3)
    while transaction_counter < target_tx_count:
        next(transact_once)
        transaction_counter += 1

    assert len(transaction_filter.get_new_entries()) == transaction_counter


@given(target_tx_count=st.integers(min_value=1, max_value=100))
def test_transaction_filter_without_mining(
        web3,
        target_tx_count):

    web3.providers[0].ethereum_tester.auto_mine_transactions = False
    transaction_filter = web3.eth.filter("pending")

    transaction_counter = 0

    transact_once = single_transaction(web3)
    while transaction_counter < target_tx_count:
        next(transact_once)
        transaction_counter += 1

    assert len(transaction_filter.get_new_entries()) == transaction_counter
