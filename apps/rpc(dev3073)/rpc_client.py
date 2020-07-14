# -*- coding: utf-8 -*_

import rpyc
import json
import jsonify
from collections import OrderedDict

if __name__ == "__main__":

    con = rpyc.connect('127.0.0.1', 18262, config={"allow_all_attrs": True})
    con.ping()

    dic = {'a': 1, 'b': 2}

    c = con.root.test(dic)
    print type(c)
    print c.get('a')