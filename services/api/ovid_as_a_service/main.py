import logging
import elasticsearch
from elasticsearch_dsl import Search, Q, connections

class OvidAsAService():
    def __init__(self):
        self._init_es()

    # INT FUNCTIONS
    def _init_es(self):
        _es = connections.create_connection(alias='default', hosts=['elasticsearch:9200'])
        if _es.ping():
            logging.info('connected to es!')
        else:
            logging.info('not connected to es!')
        return _es

    def _get_results(self, query, fields):
        q = Q("multi_match", query=query, fields=fields)
        res = Search(using='default').query(q)
        len = res.count()
        if len <= 0:
            return {'message': 'no results!'}
        return [hit.to_dict() for hit in res[0:len].sort('line')]

    # EXT FUNCTIONS
    def query_text(self, query: str):
        fields_to_search = ['chapter_name', 'text']

        return self._get_results(query, fields_to_search)

    def query_book(self, query: int):
        fields_to_search = ['book']

        return self._get_results(query, fields_to_search)
