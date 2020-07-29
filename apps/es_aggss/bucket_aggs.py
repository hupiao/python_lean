import elasticsearch
import random
import uuid
from elasticsearch import helpers, Elasticsearch
from elasticsearch_dsl import Search, Q


using = Elasticsearch(hosts='127.0.0.1')
es_search = Search(using=using, index='mtas-mail-2020.07.18', doc_type='mtas-mail')
insert_list = []
a = ['a@qq.com', 'b@qq.com', 'c@qq.com', 'd@qq.com', 'e@qq.com', 'f@qq.com', 'g@qq.com']
import datetime
import time
for i in range(5):
    nt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_list.append({
                        '_op_type': 'create',
                        '_index': 'mtas-mail-2020.07.21',
                        '_type': 'mtas-mail',
                        '_id': str(uuid.uuid1()).upper(),
                        '_source': {
                            "mid": i,
                            "from": a[random.randint(0, len(a)-1)],
                            'eml_path': 'a',
                            'analysis_status': 1,
                            'access_time': nt
                        }
                    })
    time.sleep(2)
print(helpers.bulk(using, actions=insert_list))
# es_search.query

