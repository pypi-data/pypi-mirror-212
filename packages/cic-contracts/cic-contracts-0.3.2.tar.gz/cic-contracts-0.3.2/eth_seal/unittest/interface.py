# external imports
from chainlib.eth.tx import receipt

# local imports
from eth_seal import EthSeal


class TestEthSealInterface:

    def __init__(self):
        self.set_method = None
        self.max_seal_state = 0


    def test_supply(self):
        if self.max_seal_state == 0:
            return
        c = EthSeal(self.chain_spec)
        o = c.max_seal_state(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.max_seal_state, int(r, 16))
