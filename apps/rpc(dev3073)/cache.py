# -*-coding: utf-8 -*-

import rpyc
import time
import logging


class GuishRpcClient():
    def __init__(self, host, port):

        self.host = host
        self.port = port
        self._connect()

    def _connect(self):
        count = 0
        while count < 10:
            try:
                self.client = rpyc.connect(self.host, self.port, config={"allow_all_attrs": True}, keepalive=1)
                self.client.ping()
                return
            except Exception as err:
                logging.error('Faild to connect guish_rpyc_server: %s ' % err, exc_info=True)
                time.sleep(1)
                count += 1

    def close_guish_rpc(self):
        self.client.close()

    @retry
    def get_manager_interface(self, param={}):
        """
        Get manager interfaces
        :param param: eg:{'ifname':'etho'}
        :return:
        """
        return self.client.root.NMProxy().interface_mgt_show(param)

    @retry
    def set_manager_interface(self, param):
        """
        Set manager interface
        :param param:
        :return:
        """
        return self.client.root.NMProxy().interface_mgt_set(param)

    @retry
    def get_dns_addr(self):
        return self.client.root.NMProxy().dns_addr_show()

    @retry
    def set_dns_addr(self, param):
        return self.client.root.NMProxy().dns_addr_set(param)

    @retry
    def get_router(self):
        return self.client.root.NMProxy().static_route_show()

    @retry
    def set_router(self, param):
        return self.client.root.NMProxy().static_route_set(param)

    @retry
    def device_poweroff(self):
        return self.client.root.DeviceMgt().deviceop_set({'operation': 0})

    @retry
    def device_reboot(self):
        return self.client.root.DeviceMgt().deviceop_set({'operation': 1})

    @retry
    def service_restart(self):
        return self.client.root.DeviceMgt().deviceop_set({'operation': 2})

    @retry
    def dove_process_restart(self):
        return self.client.root.DeviceMgt().dove_process_restart()

    @retry
    def peer_process_restart(self, param):
        return self.client.root.DeviceMgt().peer_process_restart(param)