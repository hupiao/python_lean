# -*-coding: utf-8 -*-

import time
import logging

from elasticsearch import helpers, Elasticsearch
from elasticsearch_dsl import Search, Q
import elasticsearch.exceptions as es_exceptions

log = logging.getLogger('seg_search')


def retry_es_connect(es_con):
    def inner(obj, *args):
        try:
            return es_con(obj, *args)
            # logging.info(kwargs)
        except es_exceptions.TransportError as e:
            logging.warn("ES connect error(%s), reconnect...", e)
            obj.es_connect()
            return es_con(obj, *args)

    return inner


class SegMailSearch(object):
    # index = 'mtas-mail-*'
    doc_type = 'mtas-mail'
    default_data = {"hits": [], "total": 0}

    def __init__(self, host='127.0.0.1', port=9200, logger=None, timeout=300, index='mtas-mail-*'):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.index = index
        self.logger = logger or log
        self.es_connect()

    def es_connect(self):
        count = 0
        while count < 3:
            try:
                self.using = Elasticsearch([{'host': self.host, 'port': self.port}])
                self.es_search = Search(using=self.using, index=self.index, doc_type=self.doc_type)
                return
            except Exception as err:
                logging.error('Failed to connect es: %s ' % err)
                time.sleep(1)
                count += 1

    def query_mail_by_esid(self, search_index, search_type, search_id):
        # 依据index type id查询单条邮件记录
        logging.info("%s-%s-%s" % (search_index, search_type, search_id))
        search = Search(using=self.using, index=search_index, doc_type=search_type)
        search = search.params(ignore_unavailable=True)
        if search_id is not None:
            search = search.query(Q('match', _id=search_id))
        resp = search.execute()
        return resp.to_dict()['hits']['hits']

    def _update(self, meta, body):
        try:
            data = self.using.update(
                index=meta.index,
                doc_type=meta.doc_type,
                id=meta.id,
                body=body
            )
            self.logger.info('update success, index: {}, doc_type: {}, id: {}, body: {}'.format(
                meta.index, meta.doc_type, meta.id, body
            ))
            return data
        except Exception as e:  # noqa
            self.logger.exception('update failure, index: {}, doc_type: {}, id: {}, body: {}'.format(
                meta.index, meta.doc_type, meta.id, body
            ))
            return None

    def update_mail_by_mid(self, mid, **kwargs):
        """
        更新邮件属性和威胁级别等属性
        """
        ret = self.es_search.filter(Q('term', mid=mid)).execute()
        if len(ret.hits) == 0:
            self.logger.info('mail not found, mid: {}'.format(mid))
            return False
        hit = ret.hits[0]
        if 'group_id' in kwargs:
            attachments = ret.hits.hits[0]['_source'].get('attachment', [])
            for index, attach in enumerate(attachments):
                if kwargs.get('group_id', '') == attach.get('group_id', ''):
                    if kwargs.get('is_update_malattach', False):
                        attachments[index]['is_malicious'] = True
                        kwargs['malattach_cnt'] = ret.hits.hits[0]['_source'].get('malattach_cnt', 0) + 1
                    if kwargs.get('malscore', 0):
                        attachments[index]['malscore'] = kwargs.pop('malscore', 0)
            kwargs.pop('group_id', '')
            kwargs.pop('is_update_malattach', '')
            kwargs['attachment'] = attachments
        self.logger.info("begin update mail, mid: {}, params: {}".format(mid, kwargs))
        return self._update(hit.meta, body={"doc": kwargs})

    @retry_es_connect
    def bulk_save_mail(self, data):
        return helpers.bulk(self.using, actions=data, refresh=True, request_timeout=300)

    def search(self,
               query_str=None,
               query_fields=None,
               filter_dict=None,
               start_time=None,
               end_time=None,
               offset=0,
               limit=20,
               order="desc",
               sort='access_time',
               range_time='access_time',
               includes=None,
               excludes=None):
        s = self.es_search
        # 指定返回的字段/排除某些字段
        if includes:
            s = s.source(includes=includes)
        if excludes:
            s = s.source(excludes=excludes)

        s = s.params(ignore_unavailable=True)
        query_fields = query_fields or []
        if query_str:
            # 前端转义 query_str = 'subject:(*cve\\ attach\\=\\=\\=\\=\\=\\=\\=\\=\\>1565857589\\.94*)'
            s = s.query(Q("query_string", query=query_str, fields=query_fields))

        filter_dict = filter_dict or {}
        must_array = filter_dict.get("must", [])
        must_not_array = filter_dict.get("must_not", [])
        should_array = filter_dict.get("should", [])
        if should_array:
            s = s.query(
                Q('bool',
                  must=must_array,
                  must_not=must_not_array,
                  should=should_array,
                  minimum_should_match=1
                  )
            )
        else:
            s = s.query(
                Q('bool',
                  must=must_array,
                  must_not=must_not_array,
                  should=should_array
                  )
            )
        # if sort:
        #     s = s.sort({sort: {"order": order}})
        timestamp_dict = {}
        if start_time:
            timestamp_dict['gte'] = start_time
        if end_time:
            timestamp_dict['lte'] = end_time
        if timestamp_dict:
            s = s.filter('range', **{range_time: timestamp_dict})
        # if limit > 0:
        #     s = s[offset:offset + limit]
        # print("search query %s", % s.to_dict())
        return s


if __name__ == "__main__":
    es = SegMailSearch(index='mtas-mail-2020.07.16')
    # filter_dict = {
    #     "must": [
    #         {"term": {'analysis_status': 1}}]
    # }
    s = es.search()
    # 分组并返回组内相应数据
    group_count = 30  # 分组数目
    order = {"_count": "desc"}  # 分组排序
    show_count = 1  # 每个组展示多少条数据
    # s.aggs.bucket('cat_from', 'terms', field="from", size=group_count, order={"_count": "desc"}).bucket('top_score_hits', 'top_hits', _source=["eml_path"], size=show_count)
    # s.aggs.bucket('cat_eml', 'terms', field="eml_path").metric('mid_count', 'value_count', field="eml_path")
    s.aggs.bucket('group_day', 'date_histogram', field="access_time", interval="hour", format="yyyy-MM-dd HH").metric('from_sum', 'value_count', field="eml_path")
    s.aggs.bucket('group_count', 'stats_bucket', buckets_path="group_day.from_sum")
    print(s.to_dict())
    result = s.execute()
    print(result.hits.hits[0].to_dict().keys())
    print(result['aggregations'].to_dict().keys())
    print(result['aggregations']["group_count"].to_dict())
    # print(result['aggregations']['cat_from']['buckets'])
    print(result['aggregations']['group_day']['buckets'][0].to_dict())
