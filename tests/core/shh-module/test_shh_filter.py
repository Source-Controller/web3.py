import time


def test_shh_sync_filter(web3, skip_if_testrpc):
    skip_if_testrpc(web3)

    sender = web3.shh.newKeyPair()
    sender_pub = web3.shh.getPublicKey(sender)

    receiver = web3.shh.newKeyPair()
    receiver_pub = web3.shh.getPublicKey(receiver)

    payloads = [web3.toHex(text="test message :)"), web3.toHex(text="2nd test message")]
    shh_filter = web3.shh.filter({'privateKeyID': receiver, 'sig': sender_pub})

    web3.shh.post({'ttl': 7, 'sig': sender, 'powTarget': 2.5, 'powTime': 2, 'payload': payloads[0], 'pubKey': receiver_pub})
    time.sleep(1)

    web3.shh.post({'ttl': 7, 'sig': sender, 'powTarget': 2.5, 'powTime': 2, 'payload': payloads[1], 'pubKey': receiver_pub})
    time.sleep(1)

    received_messages = shh_filter.get_new_entries()
    assert len(received_messages) > 1

    for message in received_messages:
        assert message["payload"] in payloads


def test_shh_async_filter(web3, skip_if_testrpc):
    skip_if_testrpc(web3)
    received_messages = []

    sender = web3.shh.newKeyPair()
    sender_pub = web3.shh.getPublicKey(sender)

    receiver = web3.shh.newKeyPair()
    receiver_pub = web3.shh.getPublicKey(receiver)

    payloads = [web3.toHex(text="test message :)"), web3.toHex(text="2nd test message")]
    shh_filter = web3.shh.filter({'privateKeyID': receiver, 'sig': sender_pub})
    watcher = shh_filter.watch(received_messages.extend)

    web3.shh.post({'ttl': 7, 'sig': sender, 'powTarget': 2.5, 'powTime': 2, 'payload': payloads[0], 'pubKey': receiver_pub})
    time.sleep(1)

    web3.shh.post({'ttl': 7, 'sig': sender, 'powTarget': 2.5, 'powTime': 2, 'payload': payloads[1], 'pubKey': receiver_pub})
    time.sleep(1)

    assert len(received_messages) > 1

    for message in received_messages:
        assert message["payload"] in payloads

    watcher.stop()
