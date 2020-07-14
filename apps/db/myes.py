#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class MyEs(object):
    def __init__(self, host, http_auth, port=9200):
        try:
            self.es = Elasticsearch(
                host,
                http_auth=http_auth,
                port=port)
        except Exception:
            print("Failed to connect ES. Exception is ",
                  traceback.print_exc())
            # store exception info to log file
            # f = open("D:\\Pyproject\\log.txt", 'a')
            # traceback.print_exc(file=f)
            # f.flush()
            # f.close()

    def create_index(self, index, doc_type, mapping):
        self.es.indices.create(index)
        self.es.indices.put_mapping(
            index=index,
            doc_type=doc_type,
            body=mapping)

    def del_index(self, index):
        self.es.indices.delete(index=index)


if __name__ == "__main__":
    # pe = MyEs(['192.168.217.133'],
    #           http_auth=('elsearch', 'elasticsearch'),
    #           port=9200)
    # print(type(pe.es.get(index='pcap_index',doc_type='pcap', id='BZeZnWUBCMNRbyKUAii0')['_type']))
    client = Elasticsearch(hosts='10.91.3.84:9200')
    indexs = client.indices.get('*')
    indexnames = indexs.keys()

    index = indexnames[0]
    # print(index)
    tables = indexs[index]['mappings'].keys
    # print(indexs[index])
    # print(tables)
    s = Search().using(client).query("match", mid='002601d470c8$be6b4c20$3b41e460$@lssisc.info')
    response = s.execute()

    print(response)
    # result = []
    # for row in response.hits:
    #     result.append(row.to_dict())
    #
    # for i in result:
    #     print(i.get('dport'))
