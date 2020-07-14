# -*- coding: utf-8 -*-

import rpyc
import json
import logging
from rpyc.utils.server import ThreadedServer
from collections import OrderedDict

class Test_rpc(rpyc.Service):

    def exposed_test(self, dic):
        print dic.get('a')
        print 'dic type: ', type(dic)
        return OrderedDict({'a': 1, 'b': 2})


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    logger.info('Rpc server is starting......')
    server = ThreadedServer(Test_rpc, port=18262, protocol_config={"allow_all_attrs": True})
    server.start()

    # , protocol_config = {"allow_public_attrs": True}
