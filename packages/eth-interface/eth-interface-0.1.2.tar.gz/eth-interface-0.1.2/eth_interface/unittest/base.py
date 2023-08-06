# standard imports
import logging

# local imports
from eth_interface import ERC165

logg = logging.getLogger(__name__)
       

class TestERC165:

    erc165_ifcs = []

    @classmethod
    def flush_interface_check(cls):
        cls.erc165_ifcs = []


    @classmethod
    def add_interface_check(cls, ifc):
        assert len(bytes.fromhex(ifc)) == 4
        cls.erc165_ifcs.append(ifc)


    def test_erc165_interfaces(self):
        c = ERC165(self.chain_spec)
        logg.info('will check interfaces: {}'.format(self.erc165_ifcs))
        for ifc in self.erc165_ifcs + ['01ffc9a7']:
            logg.debug('checking ifc {}'.format(ifc))
            o = c.supports_interface(self.address, ifc, sender_address=self.accounts[0])
            r = self.rpc.do(o)
            self.assertEqual(int(r, 16), 1)
