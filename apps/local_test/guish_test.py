import rpyc
import logging
try:
    conn = rpyc.connect('127.0.0.1', 18861, config={"allow_all_attrs": True})
    param = {'gw': '192.168.0.1', 'admin': '1', 'ssh_allow': '1', 'ipaddr': u'192.168.0.3',
             'mask': '255.255.255.0', 'autoneg': '1', 'gw_ipv6': '', 'http_allow': '1',
             'if_type': '0', 'ifname': 'eth2', 'speed': 'unknown', 'ipv6addr': '234e:0:4567::3d/64',
             'https_allow': '1'}
    conn.root.NMProxy().interface_mgt_set(param)
    conn.root.NMProxy().dns_addr_set({'prior': '114.114.114.114', 'secondary': ''})
except Exception as err:
    logging.error("{}".format(err), exc_info=1)
    print err
