from elasticsearch import Elasticsearch
import logging
import json

file = 'data/metamorphoses.json'

with open(file, 'r') as f:
    data = json.load(f)

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host':'localhost','port': 9200}])
    if _es.ping():
        print('connected!')
    else:
        print('not connected!')

    return _es
    # if __name__ == '__main__':
    #     logging.basicConfig(level=logging.ERROR)        

def create_index(es_object, index_name='metamorphoses'):
    created = False
    settings = {
        "settings":{
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "book": {"type": "integer"},
                "chapter": {"type": "text"},
                "text": {"type": "text"}
            }
        }
    }
    
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            print('created index!')
            created = True
    except Exception as e:
        print(str(e))
    finally:
        return created

def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


es = connect_elasticsearch()
create_index(es)

for line in data:
    store_record(es, "metamorphoses", line)