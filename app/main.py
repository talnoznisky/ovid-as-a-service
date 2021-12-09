from fastapi import FastAPI
from elasticsearch_dsl import Search, Q, connections

app = FastAPI()

es = connections.create_connection(hosts=['localhost:9200'])


#############################
#                           #                          
#   search for all lines    #
#  matching a string input  #
#                           #
#############################

@app.get("/lines")
def query_text(query: str):
    # TODO: data type handling
    q = Q("multi_match", query=query, fields=['chapter_name', 'text'])
    res = Search().query(q)
    len = res.count()

    return [hit.to_dict() for hit in res[0:len].sort('line')]


#############################
#                           #
#   search by book number   #
#                           #
#############################

@app.get("/books")
def get_book(query: int):
    q = Q("multi_match", query=query, fields=['book'])
    res = Search().query(q).sort('line')
    len = res.count()

    return [hit.to_dict() for hit in res[0:len].sort('line')]
