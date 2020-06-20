import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from cspnd import CSPNDaemon
from cspn_config import CSPNConfig


def test_cspnd():
    config_text = CSPNConfig.slurp_config_file(config.cspn_conf)
    network = 'mainnet'
    chain = 'main'
    genesis_hash = u'0000098e30a3d29ee06c8f371e9e1fc516c8218b1be2615b7b0ec31649ed12e3'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            chain = 'test'
            genesis_hash = u'00000546a6b03a54ae05f94119e37c55202e90a953058c35364d112d41ded06a'

    creds = CSPNConfig.get_rpc_creds(config_text, network)
    cspnd = CSPNDaemon(**creds)
    assert cspnd.rpc_command is not None

    assert hasattr(cspnd, 'rpc_connection')

    # CSPN testnet block 0 hash == 00000546a6b03a54ae05f94119e37c55202e90a953058c35364d112d41ded06a
    # test commands without arguments
    info = cspnd.rpc_command('getblockchaininfo')
    info_keys = [
        'chain',
        'blocks',
        'headers',
        'bestblockhash',
        'difficulty',
        'mediantime',
    ]
    for key in info_keys:
        assert key in info
    assert info['chain'] is chain

    # test commands with args
    assert cspnd.rpc_command('getblockhash', 0) == genesis_hash
